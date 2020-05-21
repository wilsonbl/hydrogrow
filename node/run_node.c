// File: run_node.c 
// Author: Sarah Eastwood
// Last revised: 3/13/20

#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

#include "uart_functions.h"

#define F_CPU 16000000

// For actuating the valve
#define OPEN 0
#define CLOSE 1
#define BRAKE 2

#define SEL0 2
#define SEL1 3
#define SEL2 4
#define MUX_O 5
#define HB1 6
#define HB2 7
#define EN_12V 1
#define HB_CONN 0

volatile char previous_value = '!';
volatile uint8_t seconds = 0;
volatile uint8_t valve_clock = 0;
volatile uint8_t received_char = 0;
volatile char char_received = '!';

//******************************************************************************
//                          init
// Initializing GPIO pins
//******************************************************************************
void init(){
  DDRB = (1 << EN_12V); // Make 12V enable output
  DDRC = (0 << HB_CONN) | (1 << PC3) | (1 << PC2) | (1 << PC1); // Input for H-bridge/valve voltage sensing, PC1 and PC2 output for valve debugging
  DDRD = (1 << SEL2) | (1 << SEL1) | (1 << SEL0) | (1 << HB2) | (1 << HB1); // Make MUX selects and H-bridge  outputs
  
  PORTD = 0; // Select input 0 from mux and do not change the state of the valve
} // init

 
//******************************************************************************
//                          valve_clock_init
// Initialize the 16-bit counter used for timing the valves
// 16Mhz/256 = 62500 hz
// Tick = 1/62500 = 16us
// 2^16 ticks = 65536
// ISR called every 16us * 65536 ~= 1.05s
//******************************************************************************
void valve_clock_init(){
  TCCR1A = 0; // Normal port operation, not connected to pin
  TCCR1B = 0; // Stop clock for now, but when started later, will set prescale of 256
  TIMSK1 |= (1 << TOIE1); // enable interrupt
} // valve_clock_init

//******************************************************************************
//                          adc_init
// Initialize the 8-bit ADC for checking if the valve is connected
//******************************************************************************
void adc_init(){/
  ADMUX |= (1 << REFS1) | (1 << REFS0);  // Using 1.1V internal reference, right adjusted, ADC0 selected
  ADCSRA |= (1 << ADEN)  | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); // ADC enabled, no ADC auto-triggering, no interrupt, ADC clock prescaler of 128
} // adc_init

//******************************************************************************
//                          get_water_level
// Provided an integer 0-7 representing the water level sensor, returns 1 if water is high and 0 if water is low
//*****************************************************************************
uint8_t get_water_level(uint8_t sensor_select){
  // Set the select bits on the MUX to choose which sensor to poll 
  switch(sensor_select){
    case 0:
        PORTD &= ~(1 << SEL2 | 1 << SEL1 | 1 << SEL0); break;
    case 1:
        PORTD |= (1 << SEL0);
        PORTD &= ~(1 << SEL2 | 1 << SEL1); break;
    case 2:
        PORTD |= (1 << SEL1);
        PORTD &= ~(1 << SEL2 | 1 << SEL0); break;
    case 3: 
        PORTD |= (1 << SEL1) | (1 << SEL0);
        PORTD &= ~(1 << SEL2); break;
    case 4:
        PORTD |= (1 << SEL2);
        PORTD &= ~(1 << SEL1 | 1 << SEL0); break;
    case 5: 
        PORTD |= (1 << SEL2) | (1 << SEL0);
        PORTD &= ~(1 << SEL1); break;
    case 6:
        PORTD |= (1 << SEL2) | (1 << SEL1);
        PORTD &= ~(1 << SEL0); break;
    case 7:
        PORTD |= (1 << SEL2) | (1 << SEL1) | (1 << SEL0); break;
    default:
        PORTD &= ~(1 << SEL2 | 1 << SEL1 | 1 << SEL0); 

  } // switch

  _delay_ms(1); // give the MUX a millisecond to settle
  
  uint8_t water_low = (PIND & (1 << MUX_O)) >> MUX_O; // Isolating the bit that represents the output of the MUX (don't care about the other inputs to PORTD)
  // If the sensor is 1, then the water is low.  If the sensor is 0, the water is high
  if(water_low)
    return 0;
  return 1; 

} // sensor_select


//******************************************************************************
//                          actuate_valve
// Provided OPEN, CLOSE, or BRAKE, change the inputs to the H-Bridge to open/close/brake the valve
//*****************************************************************************
void actuate_valve(uint8_t direction){
  switch(direction){
    case CLOSE:
      PORTD |= (1 << HB1);
      PORTD &= ~(1 << HB2); break;
    case OPEN:
      PORTD |= (1 << HB2);
      PORTD &= ~(1 << HB1); break;
    default: // Brake valve
      PORTD &= ~(1 << HB2 | 1 << HB1); 
  }
} // actuate_valve


//******************************************************************************
//                          get_valve_status
// Gives the valve 5 seconds to determine if it has successfully opened/closed/braked
// If it succeeded, returns character 's', otherwise 'f'
//*****************************************************************************
char get_valve_status(){
    char valve_status = 'f'; // Assume the valve failed to actuate until it is proven that it succeeded
    TCNT1 = 0; // Reset clock
    seconds = 0;
    uint16_t adc_result;
    TCCR1B |= (1 << CS12); // Start clock with set prescale of 256
	
	// Give the valve ~5 seconds to determine if it has successfully actuated
    while(seconds < 5){
      ADCSRA |= (1 << ADSC); // Start ADC conversion
      while(bit_is_clear(ADCSRA, ADIF)){} // Spin while waiting for conversion to finish
      ADCSRA |= (1 << ADIF); // Clear ADIF flag
      adc_result = ADC;
      if(adc_result > 10){  // If the ADC reads above 10mV, then the valve opened/closed/braked successfully
        valve_status = 's';
		PORTC |= (1 << PC1) // For debugging on PORTC
      }
    }
    TCCR1B &= ~(1 << CS12); // Stop clock
    return valve_status;

} // get_valve_status


//******************************************************************************
//                        Timer 1 Overflow ISR
// Interrupt produced every 1.05s to increment the seconds counter used for timing the valve
//*****************************************************************************
ISR(TIMER1_OVF_vect){
  seconds++;

  // For debugging on PORTC
  if(valve_clock == 0){
    PORTC |= (1 << PC2);
    valve_clock = 1;
  }
  else if(valve_clock == 1){
    PORTC &= ~(1 << PC2);
    valve_clock = 0;
  }
} // ISR for Timer1 (16 bit)


//******************************************************************************
//                          UART Receive ISR
// Interrupt produced whenever UART has received a character.  Store that character and then
// raise flag that a character has been recieved
//*****************************************************************************
ISR(USART_RX_vect){
  // Get character from USART
  char_received = UDR0;
  received_char = 1;
  PORTC |= (1 << PC3); // For debugging on PORTC
} // ISR for UART receive

int main(){
  init();
  uart_init();
  adc_init();
  valve_clock_init();

  sei();

  char valve_status;
  uint8_t i;
  uint8_t water_level_data;

  while(1){

    if(received_char){

      // Poll water level sensors
      if(char_received == 'w'){
        water_level_data = 0;
        for(i = 0; i < 8; i++)
          water_level_data |= get_water_level(i) << i;
        uart_putc((char)water_level_data); 
        previous_value = (char)water_level_data;
      }

      // Open valve   
      else if(char_received == 'o'){
        valve_status = 'f';
        actuate_valve(OPEN);
        valve_status = get_valve_status();
        uart_putc(valve_status);
        previous_value = valve_status;
        actuate_valve(BRAKE);
      }

      // Close valve
      else if(char_received == 'c'){
        valve_status = 'f';
        actuate_valve(CLOSE);
        valve_status = get_valve_status();
        uart_putc(valve_status);
        previous_value = valve_status;
        actuate_valve(BRAKE);
      }

      // Handshake
      else if(char_received == 'h'){
        uart_putc('h');
        previous_value = 'h';
      }

      // Resend value
      else if(char_received == 'r'){
        uart_putc(previous_value);
      }

      received_char = 0;
    }

  }

} // main

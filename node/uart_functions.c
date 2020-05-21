// File: UART Functions 
// Author: Roger Traylor, Modified by: Sarah Eastwood
// Last revised: 2/12/20 
//For controlling the UART and sending debug data to a terminal
//as an aid in debugging.

#include <avr/io.h>
#include <stdlib.h>

#define USART_BAUDRATE 9600  
// Compute baudvalue at compile time from USART_BAUDRATE and F_CPU
// For asynchronous normal mode 
#define BAUDVALUE  ((F_CPU/(USART_BAUDRATE * 16UL)) - 1 )

#include <string.h>

char uart_tx_buf[40];      //holds string to send to crt
char uart_rx_buf[40];      //holds string that recieves data from uart

//******************************************************************
//                        uart_putc
//
// Takes a character and sends it to USART0
//
void uart_putc(char data) {
    while (!(UCSR0A&(1<<UDRE0)));    // Wait for previous transmissions
    UDR0 = data;    // Send data byte
    while (!(UCSR0A&(1<<UDRE0)));    // Wait for previous transmissions
}
//******************************************************************

//******************************************************************
//                        uart_puts
// Takes a string and sends each charater to be sent to USART0
//void uart_puts(unsigned char *str) {
void uart_puts(char *str) {
    int i = 0;
    while(str[i] != '\0') { // Loop through string, sending each character
        uart_putc(str[i]);
        i++;
    }
}
//******************************************************************

//******************************************************************

//******************************************************************
//                            uart_init
//
void uart_init(){
//rx and tx enable, receive interrupt enabled, 8 bit characters
  UCSR0B |= (1<<RXEN0) | (1<<TXEN0) | (1<<RXCIE0);

//async operation, no parity,  one stop bit, 8-bit characters
UCSR0C |= (1<<UCSZ01) | (1<<UCSZ00);

// Setting baud
UBRR0H = (BAUDVALUE >> 8 ); //load upper byte of the baud rate into UBRR 
UBRR0L =  BAUDVALUE;       //load lower byte of the baud rate into UBRR 

}
//******************************************************************

//******************************************************************
//                             uart_getc
//Modified to not block indefinately in the case of a lost byte
//
char uart_getc(void) {
  uint16_t timer = 0;

  while (!(UCSR0A & (1<<RXC0))) {
  timer++;
  if(timer >= 16000){ return(0);}
  //what should we return if nothing comes in?
  //return the data into a global variable
  //give uart_getc the address of the variable
  //return a -1 if no data comes back.
  } // Wait for byte to arrive
  return(UDR0); //return the received data
}
//******************************************************************
// Usage examples:
//uart_puts(".");
//uart_puts("   ");
//uart_puts("strength = ");
//itoa((int)strength, str, 10);
//uart_puts(str);
//uart_puts("   ");
//uart_init();
//uart_putc('\n');
//uart_puts("*****************\n");
//uart_puts("wrote first byte: ");
//uart_puts(str);
//uart_putc('\n');
  

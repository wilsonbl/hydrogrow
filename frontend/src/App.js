import React, {Component} from 'react';
import './App.css';
import Button from '@material-ui/core/Button';
import LiquidFillGauge from 'react-liquid-gauge';
import { color } from 'd3-color';

class App extends Component {
  state = {values: 0}

  fetchData = () => {
    fetch('/sensors')
      .then(res => res.json())
      .then(res => JSON.parse(res))
      .then(values => this.setState({ values }));
  }

  componentDidMount(){
    this.fetchData()
    this.timer = setInterval(() => this.fetchData(), 5000);
  }

  render(){
    const radius = 200;
    const fillColor = '#6495ed';
    return(
      <div className="App">
        <h1>Sensor Data</h1>
        <h2>{this.state.values}</h2>
        <LiquidFillGauge
          style={{ margin: '0 auto' }}
          width={radius * 2}
          height={radius * 2}
          value={this.state.values}
          percent="%"
          textSize={1}
          textOffsetX={0}
          textOffsetY={0}
          textRenderer={(props) => {
              const value = Math.round(props.value);
              const radius = Math.min(props.height / 2, props.width / 2);
              const textPixels = (props.textSize * radius / 2);
              const valueStyle = {
                  fontSize: textPixels
              };
              const percentStyle = {
                  fontSize: textPixels * 0.6
              };

              return (
                  <tspan>
                      <tspan className="value" style={valueStyle}>{value}</tspan>
                      <tspan style={percentStyle}>{props.percent}</tspan>
                  </tspan>
              );
          }}
          riseAnimation
          waveAnimation
          waveFrequency={2}
          waveAmplitude={1}
          circleStyle={{
              fill: fillColor
          }}
          waveStyle={{
              fill: fillColor
          }}
          textStyle={{
              fill: color('#444').toString(),
              fontFamily: 'Arial'
          }}
          waveTextStyle={{
              fill: color('#fff').toString(),
              fontFamily: 'Arial'
          }}
      />
      </div>
    )
  }
}

export default App;

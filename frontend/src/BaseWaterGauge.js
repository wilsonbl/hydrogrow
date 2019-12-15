import React, {Component} from 'react';
import LiquidFillGauge from 'react-liquid-gauge';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import { color } from 'd3-color';

export class BaseWaterGauge extends Component{
    constructor(){
        super();

        this.state = {
            level: 0
        };
    }

    fetchData = () => {
        const that = this;
      fetch('/base_water/?num=1')
        .then(res => res.json())
        .then(res => JSON.parse(res))
        .then(function(data){
            that.setState({
                level: data[0].base_water
            })
        })
    }
  
    componentDidMount(){
      this.fetchData()
      this.timer = setInterval(() => this.fetchData(), 5000);
    }

    render(){
        const radius = 200;
        const fillColor = '#6495ed';
        return(
            <Paper>
                <Typography>Base Station Water Level</Typography>
                <LiquidFillGauge
                    style={{ margin: '0 auto' }}
                    width={radius * 2}
                    height={radius * 2}
                    value={this.state.level}
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
            </Paper>
        );
    }
}
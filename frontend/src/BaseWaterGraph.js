import React, {Component} from 'react';
import Chart from "react-apexcharts";
import Button from "@material-ui/core/Button"
import Typography from '@material-ui/core/Typography';

export class BaseWaterGraph extends Component {
    constructor(){
        super();

        this.state = {
            options: {
                chart: {
                    type: "line",
                    animations: {
                        enabled: true
                    },
                    zoom: {
                        enabled: true,
                        type: 'x',
                        autoScaleYaxis: true
                    },
                    toolbar: {
                        autoSelected: 'zoom'
                    }
                },
                xaxis: {
                    type: 'datetime'
                },
                tooltip: {
                    x: {
                      format: 'HH:mm dd MMM yyyy'
                    }
                  },
            },
            series: [
                {
                    name: "base_water",
                    data: []
                }
            ]
        };
    }

    fetchData = () => {
        const that = this;
        fetch('/base_water/?num=100')
        .then(res => res.json())
        .then(res => JSON.parse(res))
        .then(function(data){
            let items = data.map(item => [item.time, item.base_water]);
            that.setState({
                series: [
                    {
                        data: items
                    }
                ]
            })
        })
    }
    
    componentDidMount(){
        this.fetchData()
        this.timer = setInterval(() => this.fetchData(), 1000);
    } 

    /*resetData(){
        fetch('/base_water', { 
            method: 'post', 
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command: 'reset'})
        })
    }*/

    render(){
        return (
            <div>
                <Typography>Base Station Water Level</Typography>
                <div className="app">
                    <div className="row">
                        <div className="mixed-chart">
                            <Chart
                            options={this.state.options}
                            series={this.state.series}
                            type="line"
                            width="100%"
                            />
                        </div>
                    </div>
                </div>
            </div>
            
        );
    }
}

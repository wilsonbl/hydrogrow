import React, {Component} from 'react';
import Chart from "react-apexcharts";
import Button from "@material-ui/core/Button"
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';

export class BaseWaterGraph extends Component {
    constructor(){
        super();

        this.state = {
            options: {
                chart: {
                    id: "line",
                    animations: {
                        enabled: false
                    },
                    zoom: {
                        enabled: true,
                        type: 'x'
                    }
                },
                xaxis: {
                    categories: []
                },
                yaxis: {
                    floating: false,
                }
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
        fetch('/base_water/?num=10')
        .then(res => res.json())
        .then(res => JSON.parse(res))
        .then(function(data){
            let times = data.map(item => item.time);
            let base_waters = data.map(item => item.base_water)
            that.setState({
                options : {
                    xaxis: {
                        categories: times,
                        title: {
                            text: 'Time'
                        }
                    },
                    yaxis: {
                        title: {
                            text: 'Distance (cm)'
                        }
                    }
                },
                series: [
                    {
                        data: base_waters
                    }
                ]
            })
        })
    }
    
    componentDidMount(){
        this.fetchData()
        this.timer = setInterval(() => this.fetchData(), 1000);
    } 

    resetData(){
        fetch('/base_water', { 
            method: 'post', 
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command: 'reset'})
        })
    }

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
                    <Button variant="contained" color="primary" onClick={this.resetData}>
                        Reset
                    </Button>   
                </div>
            </div>
            
        );
    }
}

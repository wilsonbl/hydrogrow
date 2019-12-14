import React, {Component} from 'react';
import Chart from "react-apexcharts";
import Button from "@material-ui/core/Button"

export class BaseWater extends Component {
    constructor(){
        super();

        this.state = {
            options: {
                chart: {
                    id: "line",
                    animations: {
                        enabled: false
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
        fetch('/base_water')
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

    render(){
        return (
            <div className="app">
                <div className="row">
                    <div className="mixed-chart">
                        <Chart
                        options={this.state.options}
                        series={this.state.series}
                        type="line"
                        width="1500"
                        />
                    </div>
                </div>
            </div>
            
        );
        //return <h1>Hello! {this.state.options.xaxis.categories}</h1>
    }
}

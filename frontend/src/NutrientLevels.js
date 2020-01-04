import React, {Component} from 'react';
import Chart from "react-apexcharts";
import Typography from '@material-ui/core/Typography';

export class NutrientLevels extends Component {
    constructor(){
        super();

        this.state = {
            series: [100, 5, 36, 75],
            options: {
                chart: {
                    type: 'radialBar'
                },
                plotOptions: {
                    radialBar: {
                        dataLabels: {
                            name: {
                                fontSize: '22px',
                            },
                            value: {
                                fontSize: '16px',
                            },
                            total: {
                                show: true,
                                label: 'Total',
                                formatter: function (w) {
                                // By default this function returns the average of all series. The below is just an example to show the use of custom formatter function
                                    return 249
                                }
                            }
                        }
                    }
                },
                labels: ['N1', 'N2', 'N3', 'N4'],
            }
        };
    }

    /*fetchData = () => {
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
    }*/

    render(){
        return (
            <div>
                <Typography>Nutrient Levels</Typography>
                <div id="chart">
                    <Chart options={this.state.options} series={this.state.series} type="radialBar" height={350} />
                </div>
            </div>
            
        );
    }
}

import React, {Component} from 'react';
import Chart from "react-apexcharts";
import Typography from '@material-ui/core/Typography';

export class NutrientLevels extends Component {
    constructor(){
        super();

        this.state = {
            series: [0, 0, 0, 0],
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
                                show: false,
                            }
                        }
                    }
                },
                labels: ['N1', 'N2', 'N3', 'N4'],
            }
        };
    }

    fetchData = () => {
        const that = this;
        fetch('/nutrients/?num=1')
        .then(res => res.json())
        .then(res => JSON.parse(res))
        .then(function(data){
            let nutrients = [data[0].N1, data[0].N2, data[0].N3, data[0].N4]
            that.setState({
                series: nutrients
            })
        })
    }
    
    componentDidMount(){
        this.fetchData()
        this.timer = setInterval(() => this.fetchData(), 10000);
    }

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

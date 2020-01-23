import React, {Component} from 'react';
import Chart from "react-apexcharts";
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';

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
        fetch('/nutrients/?num=1', { method: 'get' })
        .then(res => res.json())
        .then(res => JSON.parse(res))
        .then(function(data){
            console.log("NUTRIENT LEVEL DATA GET")
            console.log(data)
            let nutrients = [data.N1, data.N2, data.N3, data.N4]
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
                <Typography variant='h6'>
                    <Box fontWeight="fontWeightBold">
                        Nutrient Levels
                    </Box>
                </Typography>
                <div id="chart">
                    <Chart options={this.state.options} series={this.state.series} type="radialBar" height={350} />
                </div>
            </div>
            
        );
    }
}

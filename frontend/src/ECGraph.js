import React, {Component} from 'react';
import Chart from "react-apexcharts";
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';

export class ECGraph extends Component {
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
                    name: "EC",
                    data: []
                }
            ]
        };
    }

    fetchData = () => {
        const that = this;
        fetch('/EC/?num=100')
        .then(res => res.json())
        .then(res => JSON.parse(res))
        .then(function(data){
            let items = data.map(item => [item.time, item.EC]);
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
        this.timer = setInterval(() => this.fetchData(), 10000);
    } 

    render(){
        return (
            <div>
                <Typography variant='h6'>
                    <Box fontWeight="fontWeightBold">
                        Electrical Conductivity Level
                    </Box>
                </Typography>
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

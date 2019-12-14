import React, {Component} from 'react';
import './App.css';
import LiquidFillGauge from 'react-liquid-gauge';
import { color } from 'd3-color';
import {BaseWater} from "./BaseWater";

class App extends Component {
  state = {values: 0}

  /*fetchData = () => {
    fetch('/sensors')
      .then(res => res.json())
      .then(res => JSON.parse(res))
      .then(values => this.setState({ values }));
  }

  componentDidMount(){
    this.fetchData()
    this.timer = setInterval(() => this.fetchData(), 1000);
  }*/

  render(){
    const radius = 200;
    const fillColor = '#6495ed';
    return(
      <div className="App">
      <BaseWater/>
      </div>
    )
  }
}

export default App;

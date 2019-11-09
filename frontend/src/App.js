import React, {Component} from 'react';
import './App.css';

class App extends Component {
  state = {values: []}

  componentDidMount(){
    fetch('/sensors')
      .then(res => res.json())
      .then(values => this.setState({ values }));
  }

  render(){
    return(
      <div className="App">
        <h1>Sensor Data</h1>
        <h2>{this.state.values}</h2>
      </div>
    )
  }
}

export default App;

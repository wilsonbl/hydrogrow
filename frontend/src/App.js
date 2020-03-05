import React, {Component} from 'react';
import './App.css';
import CssBaseline from '@material-ui/core/CssBaseline';
import DashLayout from './DashLayout'

class App extends Component {
  render(){
    return(
      <div className="App">
        <CssBaseline />
        <DashLayout />
      </div>
    );
  }
}

export default App;

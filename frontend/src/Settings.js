import React, {Component} from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import DashLayout from './DashLayout'

class Settings extends Component {
  render(){
    return(
      <div>
        <CssBaseline />
        <DashLayout />
        <hi>
          Settings
        </hi>
      </div>
    );
  }
}

export default Settings;

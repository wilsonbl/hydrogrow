<<<<<<< HEAD
import React, {useEffect} from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import EmailIcon from '@material-ui/icons/Email';
import ListItemText from '@material-ui/core/ListItemText';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';

/*
Email address
Disable/enable notifications
Color theme
Dark/Light

*/
=======
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
>>>>>>> f9310ba728a9059ed143e7a81ecfd6d4bbdb18e0

export default function Settings(){
    const [emailAddress, setEmailAddress] = React.useState("");
    const [newEmailAddress, setNewEmailAddress] = React.useState("");
    const [emailOpen, setEmailOpen] = React.useState(false);
    const handleEmailOpen = () => {
        setEmailOpen(true);
    };
    const handleEmailClose = () => {
        setEmailOpen(false);
    };
    const handleUpdateEmail = () => {
        console.log("POST sending email: " + newEmailAddress);
    };
    const handleSetEmail = event => setNewEmailAddress(event.target.value)

    useEffect(() => {
        fetch('/config')
        .then(res => res.json())
        .then(res => JSON.parse(res))
        .then(function(data){
            setEmailAddress(data[0].email)
        })
    }, []);

    return (
        <div>
            <List>
                <ListItem button onClick={handleEmailOpen}>
                    <ListItemIcon>
                        <EmailIcon />
                    </ListItemIcon>
                    <ListItemText primary="Set Notification Email" secondary={emailAddress}/>
                </ListItem>
            </List>
            <Dialog open={emailOpen} onClose={handleEmailClose} aria-labelledby="form-dialog-title">
                <DialogTitle id="form-dialog-title">Set Email</DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="email"
                        label="Email Address"
                        type="email"
                        fullWidth
                        onChange={handleSetEmail}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleEmailClose} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={handleUpdateEmail} color="primary">
                        Save
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}
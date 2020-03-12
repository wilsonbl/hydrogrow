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
import Filter1Icon from '@material-ui/icons/Filter1';
import Filter2Icon from '@material-ui/icons/Filter2';

/*
Email address
Disable/enable notifications
Color theme
Dark/Light
Node 1 # of trays
Node 2 # of trays
*/

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
        setEmailAddress(newEmailAddress);
        console.log("POST sending email: " + newEmailAddress);
        fetch('/config', { 
            method: 'post', 
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command: 'email_update', email: newEmailAddress})
        })
        handleEmailClose();
    };
    const handleSetNewEmail = event => setNewEmailAddress(event.target.value)


    const [node1NumTrays, setNode1NumTrays] = React.useState(0);
    const [newNode1NumTrays, setNewNode1NumTrays] = React.useState("");
    const [node1TraysOpen, setNode1TraysOpen] = React.useState(false);
    const handleNode1TraysOpen = () => {
        setNode1TraysOpen(true);
    };
    const handleNode1TraysClose = () => {
        setNode1TraysOpen(false);
    };
    const handleUpdateNode1Trays = () => {
        setNode1NumTrays(newNode1NumTrays);
        console.log("POST sending node 1 num trays: " + newNode1NumTrays);
        fetch('/config', { 
            method: 'post', 
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command: 'node1_trays_update', trays: newNode1NumTrays})
        })
        handleNode1TraysClose();
    };
    const handleSetNewNode1NumTrays = event => setNewNode1NumTrays(event.target.value)


    const [node2NumTrays, setNode2NumTrays] = React.useState(0);
    const [newNode2NumTrays, setNewNode2NumTrays] = React.useState("");
    const [node2TraysOpen, setNode2TraysOpen] = React.useState(false);
    const handleNode2TraysOpen = () => {
        setNode2TraysOpen(true);
    };
    const handleNode2TraysClose = () => {
        setNode2TraysOpen(false);
    };
    const handleUpdateNode2Trays = () => {
        setNode2NumTrays(newNode2NumTrays);
        console.log("POST sending node 2 num trays: " + newNode2NumTrays);
        fetch('/config', { 
            method: 'post', 
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command: 'node2_trays_update', trays: newNode2NumTrays})
        })
        handleNode2TraysClose();
    };
    const handleSetNewNode2NumTrays = event => setNewNode2NumTrays(event.target.value)


    useEffect(() => {
        fetch('/config')
        .then(res => res.json())
        .then(res => JSON.parse(res))
        .then(function(data){
            console.log(data[0])
            setEmailAddress(data[0].email)
            setNode1NumTrays(data[0].node1_num_trays)
            setNode2NumTrays(data[0].node2_num_trays)
        })
    }, []);

    return (
        <div>
            <List>
                <ListItem button onClick={handleEmailOpen}>
                    <ListItemIcon>
                        <EmailIcon />
                    </ListItemIcon>
                    <ListItemText primary="Notification Email" secondary={emailAddress}/>
                </ListItem>
                <ListItem button onClick={handleNode1TraysOpen}>
                    <ListItemIcon>
                        <Filter1Icon />
                    </ListItemIcon>
                    <ListItemText primary="Number of Trays (Node 1)" secondary={node1NumTrays}/>
                </ListItem>
                <ListItem button onClick={handleNode2TraysOpen}>
                    <ListItemIcon>
                        <Filter2Icon />
                    </ListItemIcon>
                    <ListItemText primary="Number of Trays (Node 2)" secondary={node2NumTrays}/>
                </ListItem>
            </List>
            <Dialog open={emailOpen} onClose={handleEmailClose} aria-labelledby="form-dialog-title">
                <DialogTitle id="form-dialog-title">Set Notification Email</DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="email"
                        label="Email Address"
                        type="email"
                        fullWidth
                        onChange={handleSetNewEmail}
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
            <Dialog open={node1TraysOpen} onClose={handleNode1TraysClose} aria-labelledby="form-dialog-title">
                <DialogTitle id="form-dialog-title">Set Number of Trays (Node 1)</DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        margin="dense"
                        label="Trays"
                        type="number"
                        fullWidth
                        onChange={handleSetNewNode1NumTrays}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleNode1TraysClose} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={handleUpdateNode1Trays} color="primary">
                        Save
                    </Button>
                </DialogActions>
            </Dialog>
            <Dialog open={node2TraysOpen} onClose={handleNode2TraysClose} aria-labelledby="form-dialog-title">
                <DialogTitle id="form-dialog-title">Set Number of Trays (Node 2)</DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        margin="dense"
                        label="Trays"
                        type="number"
                        fullWidth
                        onChange={handleSetNewNode2NumTrays}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleNode2TraysClose} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={handleUpdateNode2Trays} color="primary">
                        Save
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}
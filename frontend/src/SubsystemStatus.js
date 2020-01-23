import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import CheckIcon from '@material-ui/icons/Check';
import ErrorIcon from '@material-ui/icons/Error';
import Box from '@material-ui/core/Box';

const useStyles = makeStyles(theme => ({
    typography: {
        margin: theme.spacing(1)
    },
}));


export default function SubsystemStatus() {
    const classes = useStyles();
    const [pump1, handlePump1Change] = useState(2)
    const [pump2, handlePump2Change] = useState(2)
    const [node1, handleNode1Change] = useState(2)
    const [node2, handleNode2Change] = useState(2)
    
    useEffect(() => {
        const interval = setInterval(() => {
            fetch('/subsystem_status', { method: 'get' })
            .then(res => res.json())
            .then(res => JSON.parse(res))
            .then(function(data){
                console.log("SUBSYSTEM STATUS DATA GET")
                console.log(data)
                handlePump1Change(data.pump1);
                handlePump2Change(data.pump2);
                handleNode1Change(data.node1);
                handleNode2Change(data.node2);  
            })
        }, 10000);

        return () => clearInterval(interval);
    }, []);

    
    return(
        <div>
            <Typography className={classes.typography} variant='h6'>
                <Box fontWeight="fontWeightBold">
                    Subsystem Status
                </Box>
                
            </Typography>
            <Grid container spacing={2}>
                <Grid item>
                    <Typography className={classes.typography}>
                        Pump 1
                    </Typography>
                    {pump1 == 1 && <CheckIcon />}
                    {pump1 == 0 && <ErrorIcon />}
                </Grid>
                <Grid item>
                    <Typography className={classes.typography}>
                        Pump 2
                    </Typography>
                    {pump2 == 1 && <CheckIcon />}
                    {pump2 == 0 && <ErrorIcon />}
                </Grid>
                <Grid item>
                    <Typography className={classes.typography}>
                        Node1
                    </Typography>
                    {node1 == 1 && <CheckIcon />}
                    {node1 == 0 && <ErrorIcon />}
                </Grid>
                <Grid item>
                    <Typography className={classes.typography}>
                        Node2
                    </Typography>
                    {node2 == 1 && <CheckIcon />}
                    {node2 == 0 && <ErrorIcon />}
                </Grid>
            </Grid>
        </div>
    );
}
import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import InputAdornment from '@material-ui/core/InputAdornment';
import DateFnsUtils from '@date-io/date-fns';
import { DateTimePicker, MuiPickersUtilsProvider } from '@material-ui/pickers';
import Button from '@material-ui/core/Button';
import Box from '@material-ui/core/Box';

const useStyles = makeStyles(theme => ({
    textField: {
        width: 100,
        margin: theme.spacing(1)
    },
    dateTimePicker: {
        margin: theme.spacing(1)
    },
    button: {
        margin: theme.spacing(1)
    },
    title: {
        margin: theme.spacing(1)
    }
}));


export default function Node1WaterFreq() {
    const classes = useStyles();
    const [selectedDateTime, handleDateTimeChange] = useState(new Date());
    const [selectedHr, handleHrChange] = useState(0);
    const [selectedMin, handleMinChange] = useState(0);

    const sendDateTime = () => {
        console.log("POST sending node 1 hr: " + selectedHr + " min: " + selectedMin + " date/time: " + selectedDateTime )
        fetch('/node1_water_freq', { 
            method: 'post', 
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command: 'freq_update', hr: selectedHr, min: selectedMin, start: selectedDateTime})
        })
    }

    const updateHr = event => handleHrChange(event.target.value)
    const updateMin = event => handleMinChange(event.target.value);

    
    useEffect(() => {
        fetch('/node1_water_freq')
        .then(res => res.json())
        .then(res => JSON.parse(res))
        .then(function(data){
            handleHrChange(data[0].hr);
            handleMinChange(data[0].min);
            handleDateTimeChange(data[0].start);
        })
    }, []);
    
    return(
        <div>
            <Typography variant='h6' className={classes.title}>
                <Box fontWeight="fontWeightBold">
                    Node 1 Watering Schedule
                </Box>
            </Typography>
            <br />
            <Typography>
                Watering will occur every 
            </Typography>
            <TextField
                className={classes.textField}
                type="number"
                size="small"
                InputLabelProps={{
                    shrink: true,
                }}
                variant="outlined"
                margin="dense"
                value={selectedHr}
                InputProps={{
                    endAdornment: <InputAdornment position="end">hr</InputAdornment>,
                }}
                onChange={updateHr}
            />
            <TextField
                className={classes.textField}
                type="number"
                size="small"
                InputLabelProps={{
                    shrink: true,
                }}
                variant="outlined"
                margin="dense"
                value={selectedMin}
                InputProps={{
                    endAdornment: <InputAdornment position="end">min</InputAdornment>,
                }}
                onChange={updateMin}
            />
            <Typography>
                starting
            </Typography>
            <MuiPickersUtilsProvider utils={DateFnsUtils}>
                <DateTimePicker
                    className={classes.dateTimePicker}
                    value={selectedDateTime}
                    disablePast
                    onChange={handleDateTimeChange}
                    showTodayButton
                    inputVariant="outlined"
                    minDateMessage=""
                />
            </MuiPickersUtilsProvider>
            <br />
            <Button
                variant="contained"
                color="primary"
                className={classes.button}
                onClick={sendDateTime}
            >
                Update
            </Button>
        </div>
    );
}
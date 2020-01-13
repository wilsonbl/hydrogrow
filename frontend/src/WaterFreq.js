import React, { Component, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import InputAdornment from '@material-ui/core/InputAdornment';
import DateFnsUtils from '@date-io/date-fns';
import { DateTimePicker, MuiPickersUtilsProvider } from '@material-ui/pickers';
import Button from '@material-ui/core/Button';

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
}));


export default function WaterFreq() {
    const classes = useStyles();
    const [selectedDateTime, handleDateTimeChange] = useState(new Date());
    const [selectedHr, handleHrChange] = useState(0);
    const [selectedMin, handleMinChange] = useState(0);

    const sendDateTime = () => {
        fetch('/water_freq', { 
            method: 'post', 
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command: 'freq_update', hr: selectedHr, min: selectedMin, start: selectedDateTime})
        })
        console.log(selectedHr, selectedMin, selectedDateTime)
    }

    const updateHr = event => handleHrChange(event.target.value)
    const updateMin = event => handleMinChange(event.target.value);
    
    return(
        <div>
            <Typography>
                Watering will occur every 
            </Typography>
            <TextField
                className={classes.textField}
                type="hours"
                size="small"
                InputLabelProps={{
                    shrink: true,
                }}
                variant="outlined"
                margin="dense"
                defaultValue={selectedHr}
                InputProps={{
                    endAdornment: <InputAdornment position="end">hr</InputAdornment>,
                }}
                onChange={updateHr}
            />
            <TextField
                className={classes.textField}
                type="mins"
                size="small"
                InputLabelProps={{
                    shrink: true,
                }}
                variant="outlined"
                margin="dense"
                defaultValue={selectedMin}
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
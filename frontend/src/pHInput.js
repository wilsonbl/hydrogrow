import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import Slider from '@material-ui/core/Slider';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles(theme => ({
    textField: {
        width: 100,
        margin: theme.spacing(1)
    },
    title: {
        margin: theme.spacing(1)
    },
    button: {
        margin: theme.spacing(1)
    },
    slider: {
        width: 300,
        margin: theme.spacing(1)
    }
}));

export default function PHInput() {
    const classes = useStyles();
    const [selectedPH, handlePHChange] = useState(7)

    const sendPH = () => {
        console.log("POST sending pH: " + selectedPH)
        fetch('/desired_pH', { 
            method: 'post', 
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command: 'pH_update', pH: selectedPH})
        })
    }

    useEffect(() => {
        fetch('/desired_pH')
        .then(res => res.json())
        .then(res => JSON.parse(res))
        .then(function(data){
            handlePHChange(data[0].pH)
        })
    }, []);

    return(
        <div>
            <Typography variant='h6' className={classes.title}>
                <Box fontWeight="fontWeightBold">
                    Desired pH Level
                </Box>
            </Typography>
            <br />
            <br />
            <Slider
                className={classes.slider}
                defaultValue={7}
                valueLabelDisplay="on"
                step={0.1}
                min={4}
                max={10}
                onChange={(event, value) => handlePHChange(value)}
                value={selectedPH}
            />
            <br />
            <Button
                variant="contained"
                color="primary"
                className={classes.button}
                onClick={sendPH}
            >
                Update
            </Button>
        </div>
    )
}
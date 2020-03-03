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

export default function ECInput() {
    const classes = useStyles();
    const [selectedEC, handleECChange] = useState(6)

    const sendEC = () => {
        console.log("POST sending EC: " + selectedEC)
        fetch('/desired_EC', { 
            method: 'post', 
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command: 'EC_update', EC: selectedEC})
        })
    }

    useEffect(() => {
        fetch('/desired_EC')
        .then(res => res.json())
        .then(res => JSON.parse(res))
        .then(function(data){
            handleECChange(data[0].EC)
        })
    }, []);

    return(
        <div>
            <Typography variant='h6' className={classes.title}>
                <Box fontWeight="fontWeightBold">
                    Desired EC Level
                </Box>
            </Typography>
            <br />
            <br />
            <Slider
                className={classes.slider}
                defaultValue={6}
                valueLabelDisplay="on"
                step={0.05}
                min={0.75}
                max={2.5}
                onChange={(event, value) => handleECChange(value)}
                value={selectedEC}
            />
            <br />
            <Button
                variant="contained"
                color="primary"
                className={classes.button}
                onClick={sendEC}
            >
                Update
            </Button>
        </div>
    )
}
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import {BaseWaterGraph} from "./BaseWaterGraph";
import {NutrientLevels} from "./NutrientLevels";
import Node1WaterFreq from "./Node1WaterFreq";
import Node2WaterFreq from "./Node2WaterFreq";
import SubsystemStatus from "./SubsystemStatus";
import {PHGraph} from "./pHGraph";
import {ECGraph} from "./ECGraph";
import PHInput from "./pHInput";
import ECInput from "./ECInput";

const useStyles = makeStyles(theme => ({
    root: {
      flexGrow: 1,
    },
    inputs: {
        height: "100%"
    },
}));

export default function CardGrid(){
    const classes = useStyles();

    return(
        <div className = {classes.root}>
            <Grid container spacing={2} alignItems="stretch">
                <Grid item xs >
                    <Paper>
                        <BaseWaterGraph />
                    </Paper>
                </Grid>
                <Grid item xs >
                    <Paper>
                        <PHGraph />
                    </Paper>
                </Grid>
                <Grid item xs>
                    <Paper>
                        <ECGraph />
                    </Paper>
                </Grid>
            </Grid>
            <Grid container spacing={2} alignItems="stretch" >
                <Grid item xs >
                    <Paper>
                        <Node1WaterFreq className={classes.inputs}/>
                    </Paper>
                </Grid>
                <Grid item xs >
                    <Paper>
                        <Node2WaterFreq />
                    </Paper>
                </Grid>
                <Grid item xs>
                    <Paper>
                        <PHInput />
                    </Paper>
                    <Paper>
                        <ECInput />
                    </Paper>
                </Grid>
                <Grid item xs>
                    <Paper>
                        <NutrientLevels />
                    </Paper>
                </Grid>
            </Grid>
            <Grid container spacing={2} alignItems="stretch" justify="center" >
                <Grid item xs={10}>
                    <Paper>
                        <SubsystemStatus />
                    </Paper>
                </Grid>
            </Grid>
        </div>
    );
}
import React from 'react';
import clsx from 'clsx';
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

const useStyles = makeStyles(theme => ({
    root: {
      flexGrow: 1
    },
    paper: {
        padding: theme.spacing(2)
    }
}));

export default function CardGrid(){
    const classes = useStyles();
    const graphHeightPaper = clsx(classes.paper, classes.graphHeight)

    return(
        <div className = {classes.root}>
            <Grid container spacing={2} >
                <Grid item xs={4} sm={4} md={4} lg={4} xl={4}>
                    <Paper>
                        <BaseWaterGraph />
                    </Paper>
                </Grid>
                <Grid item xs={4} sm={4} md={4} lg={4} xl={4}>
                    <Paper>
                        <PHGraph />
                    </Paper>
                </Grid>
                <Grid item xs={4} sm={4} md={4} lg={4} xl={4}>
                    <Paper>
                        <NutrientLevels />
                    </Paper>
                </Grid>
                <Grid item xs={4} sm={4} md={4} lg={4} xl={4}>
                    <Paper>
                        <Node1WaterFreq />
                    </Paper>
                </Grid>
                <Grid item xs={4} sm={4} md={4} lg={4} xl={4}>
                    <Paper>
                        <Node2WaterFreq />
                    </Paper>
                </Grid>
                <Grid item xs={4} sm={4} md={4} lg={4} xl={4}>
                    <Paper>
                        <SubsystemStatus />
                    </Paper>
                </Grid>
                <Grid item xs={4} sm={4} md={4} lg={4} xl={4}>
                    <Paper>
                        <PHInput />
                    </Paper>
                </Grid>
            </Grid>
        </div>
    );
}
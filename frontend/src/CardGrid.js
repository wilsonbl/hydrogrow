import React from 'react';
import clsx from 'clsx';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import {BaseWaterGraph} from "./BaseWaterGraph";
import {BaseWaterGauge} from "./BaseWaterGauge";
import { makeStyles } from '@material-ui/core/styles';

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
            <Grid container spacing={2}>
                <Grid item xs={4} sm={4} md={4} lg={4} xl={4}>
                    <Paper>
                        <BaseWaterGraph />
                    </Paper>
                </Grid>
            </Grid>
        </div>
    );
}
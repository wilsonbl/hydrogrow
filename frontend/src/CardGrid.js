import React, {Component} from 'react';
import Grid from '@material-ui/core/Grid';
import {BaseWaterGraph} from "./BaseWaterGraph";
import {BaseWaterGauge} from "./BaseWaterGauge";
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({
    root: {
      flexGrow: 1,
    },
    paper: {
      padding: theme.spacing(5),
      textAlign: 'center',
      color: theme.palette.text.secondary,
    },
  }));

export default function CardGrid(){
    const classes = useStyles();

    return(
        <div className = {classes.root}>
            <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
                    <BaseWaterGraph />
                </Grid>
                <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
                    <BaseWaterGauge />
                </Grid>
            </Grid>
        </div>
    );
}
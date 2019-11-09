var express = require('express');
var router = express.Router();

var sqlite = require('better-sqlite3');

/* Sensor data */
router.get('/', function(req, res, next) {
    var db = new sqlite("./database/sensorDatabase.db");
    var rows = db.prepare("SELECT state FROM readings").all();
    db.close()

    sensorData = JSON.stringify(rows.map(row => row.state));
    
    res.json(sensorData);
});

module.exports = router;

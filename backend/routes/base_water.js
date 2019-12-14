var express = require('express');
var router = express.Router();

var sqlite = require('better-sqlite3');

/* Sensor data */
router.get('/', function(req, res, next) {
    var db = new sqlite("./database/HydroDatabase.db");
    var rows = db.prepare("SELECT time, base_water FROM timed ORDER BY time ASC LIMIT 100").all();
    //rows = rows.reverse();
    db.close()

    sensorData = JSON.stringify(rows);

    res.json(sensorData);
});

module.exports = router;

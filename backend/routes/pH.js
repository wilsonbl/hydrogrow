var express = require('express');
var router = express.Router();

var sqlite = require('better-sqlite3');

/* pH data */
router.get('/', (req, res) => {
    var db = new sqlite("./database/HydroDatabase.db");
    var rows = db.prepare("SELECT time, pH FROM PH ORDER BY time DESC LIMIT " + req.query.num).all();
    rows.reverse()
    db.close()

    sensorData = JSON.stringify(rows);
    res.json(sensorData);
});

module.exports = router;

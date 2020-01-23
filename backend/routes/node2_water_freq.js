var express = require('express');
var router = express.Router();

var sqlite = require('better-sqlite3');

router.post('/', (req) => {
    if (req.body.command == 'freq_update') {
        var db = new sqlite("./database/HydroDatabase.db");
        const update = db.prepare("UPDATE NODE2_WATER_FREQ SET hr = '" + req.body.hr + "', min = '" + req.body.min + "', start = '" + req.body.start + "'");
        update.run()
        db.close()
    }
});
router.get('/', (req, res) => {
    var db = new sqlite("./database/HydroDatabase.db");
    var rows = db.prepare("SELECT hr, min, start FROM NODE2_WATER_FREQ").all();
    db.close()

    sensorData = JSON.stringify(rows);
    res.json(sensorData);
});

module.exports = router;

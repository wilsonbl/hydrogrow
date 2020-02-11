var express = require('express');
var router = express.Router();

var sqlite = require('better-sqlite3');

router.get('/', (req, res) => {
    var db = new sqlite("./database/HydroDatabase.db");
    var rows = db.prepare("SELECT time, base_water FROM BASE_WATER ORDER BY time DESC LIMIT " + req.query.num).all();
    rows.reverse()
    db.close()

    sensorData = JSON.stringify(rows);
    res.json(sensorData);
});

router.post('/', (req) => {
    if (req.body.command == 'reset') {
        console.log("Resetting :D")
        var db = new sqlite("./database/HydroDatabase.db");
        const del = db.prepare("DELETE FROM BASE_WATER");
        del.run()
        db.close()
    }
});

module.exports = router;

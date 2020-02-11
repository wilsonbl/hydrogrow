var express = require('express');
var router = express.Router();

var sqlite = require('better-sqlite3');

router.post('/', (req) => {
    if (req.body.command == 'freq_update') {
        console.log("POST received hr = " + req.body.hr + "', min = '" + req.body.min + "', start = '" + req.body.start + "\n Inserting into database.");
        var db = new sqlite("./database/HydroDatabase.db");
        const update = db.prepare("UPDATE NODE1_WATER_FREQ SET hr = '" + req.body.hr + "', min = '" + req.body.min + "', start = '" + req.body.start + "'");
        update.run()
        db.close()
    }
});
router.get('/', (req, res) => {
    var db = new sqlite("./database/HydroDatabase.db");
    var rows = db.prepare("SELECT hr, min, start FROM NODE1_WATER_FREQ").all();
    db.close()
    console.log("Retrieved " + rows + " from database.")

    data = JSON.stringify(rows);
    console.log("Sending " + data + " to web interface")
    res.json(data);
});

module.exports = router;

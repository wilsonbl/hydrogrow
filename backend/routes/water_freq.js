var express = require('express');
var router = express.Router();

var sqlite = require('better-sqlite3');

router.post('/', (req) => {
    if (req.body.command == 'freq_update') {
        var db = new sqlite("./database/HydroDatabase.db");
        const update = db.prepare("UPDATE WATER_FREQ SET hr = '" + req.body.hr + "', min = '" + req.body.min + "', start = '" + req.body.start + "'");
        update.run()
        db.close()
    }
});

module.exports = router;

var express = require('express');
var router = express.Router();

var sqlite = require('better-sqlite3');

router.get('/', (req, res) => {
    var db = new sqlite("./database/HydroDatabase.db");
    var rows = db.prepare("SELECT node1, node2, pump1, pump2, node1Leak, node2Leak, pH, EC, valve1, valve2 FROM SUBSYSTEM_STATUS").all();
    db.close()

    res.json(JSON.stringify(rows[0]));
});

module.exports = router;

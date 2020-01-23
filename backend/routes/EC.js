var express = require('express');
var router = express.Router();

var sqlite = require('better-sqlite3');

/* EC data */
router.get('/', (req, res) => {
    var db = new sqlite("./database/HydroDatabase.db");
    var rows = db.prepare("SELECT time, EC FROM EC ORDER BY time DESC LIMIT " + req.query.num).all();
    rows.reverse()
    db.close()
    
    res.json(JSON.stringify(rows));
});

module.exports = router;

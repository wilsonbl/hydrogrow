var express = require('express');
var router = express.Router();

var sqlite = require('better-sqlite3');

router.get('/', (req, res) => {
    var db = new sqlite("./database/HydroDatabase.db");
    var rows = db.prepare("SELECT EC FROM DESIRED_EC").all();
    db.close()

    res.json(JSON.stringify(rows));
});
router.post('/', (req) => {
    if (req.body.command == 'EC_update') {
        console.log("POST received EC " + req.body.EC);
        var db = new sqlite("./database/HydroDatabase.db");
        const update = db.prepare("UPDATE DESIRED_EC SET EC = '" + req.body.EC + "'");
        update.run()
        db.close()
    }
});

module.exports = router;

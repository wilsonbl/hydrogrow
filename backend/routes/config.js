var express = require('express');
var router = express.Router();

var sqlite = require('better-sqlite3');

router.get('/', (req, res) => {
    var db = new sqlite("./database/HydroDatabase.db");
    var rows = db.prepare("SELECT * FROM CONFIG").all();
    db.close()

    res.json(JSON.stringify(rows));
});
router.post('/', (req) => {
    if (req.body.command == 'email_update') {
        console.log("POST received email " + req.body.EC);
        var db = new sqlite("./database/HydroDatabase.db");
        const update = db.prepare("UPDATE DESIRED_EC SET EC = '" + req.body.EC + "'");
        update.run()
        db.close()
    }
});

module.exports = router;

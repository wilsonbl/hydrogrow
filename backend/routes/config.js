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
        console.log(req.body)
        console.log("POST received email " + req.body.email);
        var db = new sqlite("./database/HydroDatabase.db");
        const update = db.prepare("UPDATE CONFIG SET email = '" + req.body.email + "'");
        update.run()
        db.close()
    }
    else if (req.body.command == 'node1_trays_update') {
        console.log(req.body)
        console.log("POST received node1 num trays " + req.body.trays);
        var db = new sqlite("./database/HydroDatabase.db");
        const update = db.prepare("UPDATE CONFIG SET node1_num_trays = '" + req.body.trays + "'");
        update.run()
        db.close()
    }
    else if (req.body.command == 'node2_trays_update') {
        console.log(req.body)
        console.log("POST received node2 num trays " + req.body.trays);
        var db = new sqlite("./database/HydroDatabase.db");
        const update = db.prepare("UPDATE CONFIG SET node2_num_trays = '" + req.body.trays + "'");
        update.run()
        db.close()
    }
});

module.exports = router;

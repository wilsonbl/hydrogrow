var express = require('express');
var router = express.Router();

var sqlite = require('better-sqlite3');

router.get('/', (req, res) => {
    var db = new sqlite("./database/HydroDatabase.db");
    var rows = db.prepare("SELECT pH FROM DESIRED_PH").all();
    db.close()

    res.json(JSON.stringify(rows));
});
router.post('/', (req) => {
    if (req.body.command == 'pH_update') {
        console.log("POST received pH " + req.body.pH);
        var db = new sqlite("./database/HydroDatabase.db");
        const update = db.prepare("UPDATE DESIRED_PH SET pH = '" + req.body.pH + "'");
        update.run()
        db.close()
    }
});

module.exports = router;

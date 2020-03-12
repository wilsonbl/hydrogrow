var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var base_waterRouter = require('./routes/base_water');
var pHRouter = require('./routes/pH');
var ECRouter = require('./routes/EC');
var nutrientsRouter = require('./routes/nutrients');
var node1_water_freqRouter = require('./routes/node1_water_freq');
var node2_water_freqRouter = require('./routes/node2_water_freq');
var subsystem_statusRouter = require('./routes/subsystem_status');
var desired_pHRouter = require('./routes/desired_pH');
var desired_ECRouter = require('./routes/desired_EC');
var configRouter = require('./routes/config');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/base_water', base_waterRouter)
app.use('/pH', pHRouter)
app.use('/EC', ECRouter)
app.use('/nutrients', nutrientsRouter)
app.use('/node1_water_freq', node1_water_freqRouter)
app.use('/node2_water_freq', node2_water_freqRouter)
app.use('/subsystem_status', subsystem_statusRouter)
app.use('/desired_pH', desired_pHRouter)
app.use('/desired_EC', desired_ECRouter)
app.use('/config', configRouter)

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;

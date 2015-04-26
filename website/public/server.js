// Core modules
var express = require('express');
var path = require('path');
var bodyParser = require('body-parser');
var app = express();
var port = process.env.PORT || 3000;

// Environment variables
app.use(bodyParser.urlencoded());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, './client')));

// Database connection and models loading
require('./server/config/mongoose');

// Routes
require('./server/config/routes')(app);

// Listen to port
var server = app.listen(port, function() {
	console.log("listening on port "+port);
});

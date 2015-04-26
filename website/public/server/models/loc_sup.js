// require mongoose
var mongoose = require('mongoose');

// create our schema
var locationSchema = new mongoose.Schema({
	location: String
});

// turn the schema into a model
mongoose.model('Loc_sup', locationSchema);

// we don't need to export anything because require runs the code!!! see the mongoose.js file in the config folder
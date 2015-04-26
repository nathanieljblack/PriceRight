// require mongoose
var mongoose = require('mongoose');

// create our schema
var productSchema = new mongoose.Schema({
	product: String
});

// turn the schema into a model
mongoose.model('Prod_unsup', productSchema);

// we don't need to export anything because require runs the code!!! see the mongoose.js file in the config folder
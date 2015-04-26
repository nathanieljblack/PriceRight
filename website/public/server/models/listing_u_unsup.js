// require mongoose
var mongoose = require('mongoose');

// create our schema
var listingSchema = new mongoose.Schema({
	city : String,
	product : String,
	title : String,
	url : String,
	created_at : Date,
	price : Number
});

// turn the schema into a model
mongoose.model('Listing_u_unsup', listingSchema);

// we don't need to export anything because require runs the code!!! see the mongoose.js file in the config folder


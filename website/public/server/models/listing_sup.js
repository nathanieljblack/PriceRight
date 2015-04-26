// require mongoose
var mongoose = require('mongoose');

// create our schema
var listingSchema = new mongoose.Schema({
	city : String,
	product : String,
	title : String,
	url : String,
	scraped_at : Date,	
	created_at : Date,
	c3Date : String,
	price : Number
});

// turn the schema into a model
mongoose.model('Listing_sup', listingSchema);

// we don't need to export anything because require runs the code!!! see the mongoose.js file in the config folder


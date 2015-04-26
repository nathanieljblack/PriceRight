// require mongoose and load the model that we are going to use
var mongoose = require('mongoose');
// var Product = mongoose.model('Product');
// var Loc = mongoose.model('Location');
// var Listing = mongoose.model('Listing');
var Product = mongoose.model('Prod_sup');
var Loc = mongoose.model('Loc_sup'); 
var Listing = mongoose.model('Listing_sup');
var Listing_u = mongoose.model('Listing_u_sup');
var Prod_sup = mongoose.model('Prod_sup');
var Prod_unsup = mongoose.model('Prod_unsup');
var Loc_sup = mongoose.model('Loc_sup');
var Loc_unsup = mongoose.model('Loc_unsup');
var Listing = mongoose.model('Listing_sup');
var Listing_sup = mongoose.model('Listing_sup');
var Listing_u_sup = mongoose.model('Listing_u_sup');
var Listing_unsup = mongoose.model('Listing_unsup');
var Listing_u_unsup = mongoose.model('Listing_u_unsup');

// create an object with methods that we are going to export for our routes file to use
var listings = {};

// setup database helper function for deciding database request
function db_helper(req){
	if (req.body.nlp_mode=='supervised'){
		Product = Prod_sup;
		Loc = Loc_sup;
		Listing = Listing_sup;
		Listing_u = Listing_u_sup;
	}
	else if (req.body.nlp_mode=='unsupervised'){
		Product = Prod_unsup;
		Loc = Loc_unsup;
		Listing = Listing_unsup;
		Listing_u = Listing_u_unsup;
	}
}

// setup query helper function for handling http requests
function query_helper(req,date_option){
	var startDateQuery = new Date(req.body.startDate);
	var endDateQuery = new Date(req.body.endDate);
	// endDateQuery = endDateQuery.setSeconds(1);
	if (date_option=="created_at") {
		startDateQuery = {created_at:{$gte:startDateQuery}};
		endDateQuery = {created_at:{$lte:endDateQuery}};
	}
	else if (date_option=="scraped_at") {
		startDateQuery = {scraped_at:{$gte:startDateQuery}};
		endDateQuery = {scraped_at:{$lte:endDateQuery}};
	}

	var query = [];
	if (req.body.product!="All iPhones" && req.body.location!="Throughout U.S."){
		query = [{product:req.body.product}, {city:req.body.location},startDateQuery,endDateQuery];
	}
	else if(req.body.product=="All iPhones" && req.body.location!="Throughout U.S."){
		query = [{city:req.body.location},startDateQuery,endDateQuery];
	}
	else if(req.body.product!="All iPhones" && req.body.location=="Throughout U.S."){
		query = [{product:req.body.product},startDateQuery,endDateQuery];
	}
	else{
		query = [startDateQuery,endDateQuery];
	}
	return query;
} 

listings.getLocations = function(req,res){
	db_helper(req);
	Loc.find({},function(err,data){
		if(err){
			res.send('something went wrong with retrieving locations!');
		}	else {
			res.json(data);
		}
	});
}
listings.getProducts = function(req,res){
	db_helper(req);	
	Product.find({},function(err,data){
		if(err){
			res.send('something went wrong with retrieving products!');
		}	else {
			res.json(data);
		}
	});
}
// listings.getDates = function(req,res){
// 	db_helper(req);
// 	var dates = [];
// 	Listing.find({},{created_at:1}).sort({created_at:1}).limit(1).exec(function(err,data){
// 		if(err){
// 			res.send('something went wrong with retrieving start date!');
// 		} else {
// 			dates.push({startDate:data[0].created_at});
// 			Listing.find({},{created_at:1}).sort({created_at:-1}).limit(1).exec(function(err,data){
// 				if(err){
// 					res.send('something went wrong with retrieving end date!');
// 				} else {
// 					dates.push({endDate:data[0].created_at});
// 					res.json(dates);
// 					// console.log(dates);
// 				}
// 			});
// 		}
// 	});
// }

listings.getNumResults = function(req,res){
	db_helper(req);
	var query=query_helper(req,"scraped_at");
	// console.log(query);

	// if(req.body.nlp_mode=="supervised") Listing = Listing_sup;
	// else if ((req.body.nlp_mode=="unsupervised")) Listing = Listing_unsup;
	Listing.find({$and: query})
	.count()
	.exec(function(err,data){
		if(err){
			res.send('something went wrong with retrieving number of results!');
		}	else {
			res.json(data);
			// console.log(data);
		}
	});	
}

//Get average price in chronologial order
listings.getListings_priceTime = function(req,res){
	db_helper(req);
	var query=query_helper(req,"scraped_at");
	// console.log(query);
	Listing.aggregate([
		{$match : {$and: query}},		
		{
			$group : {
				_id:"$c3Date",
				avg_price: {$avg:"$price"},
				// posts: {$sum:1}
			}
		},
		{$sort : {_id:1}} //by ascending order of date
	],function(err,data){
		if(err){
			res.send('something went wrong with retrieving average price per time period!');
		}	else {
			res.json(data);
			// console.log(data);
		}
	});
}

// Get average price per city in alphabetical order of city
listings.getListings_priceCity = function(req,res){

	db_helper(req);
	var query=[];
	var startDateQuery = {scraped_at: {$gte: new Date(req.body.startDate)}};
	var endDateQuery = {scraped_at: {$lte: new Date(req.body.endDate)}};
	if (req.body.product == "All iPhones"){
		query = {$and:[startDateQuery,endDateQuery]};
		// console.log('i am here');
	}
	else{
		query = {$and:[{product:req.body.product},startDateQuery,endDateQuery]};
	}
	// if(req.body.nlp_mode=="supervised") Listing = Listing_sup;
	// else if ((req.body.nlp_mode=="unsupervised")) Listing = Listing_unsup;
	Listing.aggregate([
		{$match : query},		
		{
			$group : {
				_id:"$city",
				// _id:{city:"$city", product:"$product"}, //group by city and product
				avg_price: {$avg:"$price"},
				// posts: {$sum:1}
			}
		},
		{$sort : {_id:1}} //by alphabetical order of city
	],function(err,data){
		if(err){
			res.send('something went wrong with retrieving average price per city!');
		}	else {
			res.json(data);
			// console.log(data);
		}
	});
}

//Get listings in descending order of price
listings.getListings_allItem = function(req,res){
	db_helper(req);
	var query=query_helper(req,"created_at");
	Listing_u.find(
		{$and: query}
	)
	// .sort({created_at:-1}) //descending order of the posting date
	.limit(2000)
	.exec(function(err,data){
		if(err){
			res.send('something went wrong with retrieving listings!');
		}	else {
			res.json(data);
			// console.log(data);
		}
	});
}

//Get listings in descending order of price
listings.sortListings_allItem = function(req,res){
	db_helper(req);
	var query=query_helper(req,"created_at");
	var sort_method = {};
	if (req.body.order_option==0) sort_method={created_at:-1};
	else if (req.body.order_option==1) sort_method={price:1};
	Listing_u.find(
		{$and: query}
	)
	.sort(sort_method) //descending order of the posting date
	.limit(2000)
	.exec(function(err,data){
		if(err){
			res.send('something went wrong with retrieving listings!');
		}	else {
			res.json(data);
			console.log(sort_method);
			// console.log(data);
		}
	});
}

module.exports = listings;


var listings = require('../controllers/listings');

module.exports = function(app) {
	app.post('/getLocations',function(req,res){
		listings.getLocations(req,res);
	});
	app.post('/getProducts',function(req,res){
		listings.getProducts(req,res);
	});
	app.post('/getDates',function(req,res){
		listings.getDates(req,res);
	});
	app.post('/getListings_priceTime',function(req,res){
		listings.getListings_priceTime(req,res);
	});
	app.post('/getListings_priceCity',function(req,res){
		listings.getListings_priceCity(req,res);
	});
	app.post('/getListings_allItem',function(req,res){
		listings.getListings_allItem(req,res);
	});
	app.post('/sortListings_allItem',function(req,res){
		listings.sortListings_allItem(req,res);
	});
	app.post('/getNumResults',function(req,res){
		listings.getNumResults(req,res);
	});

	// app.get('/getUsers',function(req,res){
	// 	users.getUsers(req,res);
	// });
	// app.post('/addUser',function(req,res){
	// 	console.log('hello_route');
	// 	users.addUser(req,res);
	// });
	// app.post('/removeUser', function(req, res) {
	// 	users.removeUser(req,res);
	// });
	// app.post('/editUser', function(req, res) {
	// 	users.editUser(req, res);
	// });
}
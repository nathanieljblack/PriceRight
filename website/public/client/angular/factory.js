// Creating factory and givint it access to $http to send ajex/api calls
myApp.factory('listingFactory',function($http){
	var products = [];
	var locations = [];
	var listings = [];
	var factory = {};

	factory.getProducts = function(nlp_mode,callback){
		$http.post('/getProducts',{nlp_mode:nlp_mode}).success(function(output){
			products = output;
			for (var index in products){
				products[index]['id'] = parseInt(index);
			}
			callback(products);
		});		
	}
	factory.getLocations = function(nlp_mode,callback){
		$http.post('/getLocations',{nlp_mode:nlp_mode}).success(function(output){
			locations = output;
			for (var index in locations){
				locations[index]['id'] = parseInt(index);
			}
			callback(locations);
		});		
	}

	// factory.getDates = function(nlp_mode,callback){
	// 	$http.post('/getDates',{nlp_mode:nlp_mode}).success(function(output){
	// 		callback(output);
	// 	});
	// }

	// factory.getListings = function(callback){
	// 	$http.get('/getListings').success(function(output){
	// 		listings = output
	// 		callback(listings);
	// 	});		
	// }

	factory.getListings = function(product_index, location_index, startDate, endDate, nlp_mode, callback){
		var query = {
			product:products[product_index]['product'], 
			location:locations[location_index]['location'],
			startDate: startDate,
			endDate: endDate,
			nlp_mode: nlp_mode
		};
		// console.log("factory query",query);
		listings = []
		var listings_priceTime = [];
		var listings_priceCity = [];
		var listings_allItem = [];
		$http.post('/getListings_priceTime',query).success(function(output){
			listings_priceTime = output;
			for (var i=0; i<listings_priceTime.length; i++){
				listings_priceTime[i].avg_price = parseFloat(listings_priceTime[i].avg_price).toFixed(2);
			}
			// console.log("listings_priceTime",listings_priceTime);
			$http.post('/getListings_priceCity',query).success(function(output){
				listings_priceCity = output;
				for (var i=0; i<listings_priceCity.length; i++){
					listings_priceCity[i].avg_price = parseFloat(listings_priceCity[i].avg_price).toFixed(2);
				}
				$http.post('/getListings_allItem',query).success(function(output){
					listings = [
						listings_priceTime,
						listings_priceCity,
						output   //output is listings_allItem
					];
					// console.log(output);
					// console.log(listings);
					callback(listings);
				});
			});
		});		
	}

	factory.sortListings = function(product_index, location_index, startDate, endDate, nlp_mode, order_option, callback){
		var query = {
			product:products[product_index]['product'], 
			location:locations[location_index]['location'],
			startDate: startDate,
			endDate: endDate,
			nlp_mode: nlp_mode,
			order_option: order_option
		};
		$http.post('/sortListings_allItem',query).success(function(output){
			// console.log(output);
			callback(output);
		});
	}

	factory.getNumResults = function(product_index, location_index, startDate, endDate, nlp_mode, callback){
		var query = {
			product:products[product_index]['product'], 
			location:locations[location_index]['location'],
			startDate: startDate,
			endDate: endDate,
			nlp_mode: nlp_mode
		};
		$http.post('/getNumResults',query).success(function(output){
			callback(output);
		});
	}

	// var users = []
	// factory.getUsers = function(callback){
	// 	$http.get('/getUsers').success(function(output){
	// 		users = output;
	// 		callback(users);
	// 	});
	// }
	// factory.addUser = function(newUser,callback){
	// 	$http.post('/addUser',newUser).success(function(output){
	// 		var newUser = output;
	// 		users.push(newUser);
	// 		callback(users);
	// 	});
	// }
	// // factory.addUsersFromSocket = function(usersSocket){
	// // 		users=usersSocket;
	// // }
	// factory.removeUser = function(indexUser,callback){
	// 	var serverUserID=users[indexUser]._id; //find server's user id
	// 	$http.post('/removeUser',{_id:serverUserID}).success(function(output){
	// 		console.log(output.msg); //output is just a success delete message
	// 		users.splice(indexUser,1);
	// 		callback(users);
	// 	});		
	// }
	// factory.getOneUser = function(indexUser,callback){
	// 		callback(users[indexUser]); //find find user without going to database		
	// }
	// factory.editUser = function(user,indexUser,callback){
	// 	user._id=users[indexUser]._id;
	// 	$http.post('/editUser',user).success(function(output){
	// 		var editedUser=output;
	// 		users[indexUser]=editedUser;
	// 		callback(editedUser);
	// 	});
	// }
	return factory;
});

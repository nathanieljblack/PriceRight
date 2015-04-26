myApp.controller('listingCtrl', function($scope,listingFactory){

	$scope.product = 0;
	$scope.location = 0;
	$scope.product_name = "All iPhones";
	$scope.location_name = "Throughout U.S.";
	$scope.products = [];
	$scope.locations = [];
	$scope.listings_allItems = [];
	$scope.listings_priceCity = [];
	$scope.listings_priceTime = [];
	$scope.nlp_mode = "supervised";
	$scope.startDate = "";
	$scope.endDate = "";
	$scope.startDateUTC = "";
	$scope.endDateUTC = "";

	$scope.order_option = 0;
	$scope.order_options = [{id:0,order_option:"Earliest Posting Date"},{id:1,order_option:"Lowest Price"}];

	// text
	$scope.title_results = "Your Results Will be Shown Below...";
	$scope.title_priceLatest = "Latest Average Price is [to be calculated here]";
	$scope.title_priceTime = "Daily Average Price";
	$scope.title_priceCity = "Average Price Per Location";
	$scope.title_allItems = "Listing of cheapest items";

	// $scope.loaded_price_city = "";

	listingFactory.getProducts($scope.nlp_mode, function(data){
		$scope.products = data;
	});
	listingFactory.getLocations($scope.nlp_mode, function(data){
		$scope.locations = data;
	});

	// listingFactory.getDates($scope.nlp_mode, function(data){
	// 	$scope.startDate = data['startDate'];
	// 	$scope.endDate = data['endDate'];
	// });

	showGraphPriceTime([]);
	showGraphPriceCity([]);

	//Convert input time to UTC as we are ignoring time-zone difference
	convertUTC = function(date_local){
		var date = new Date(date_local);
		// console.log(date_local);
		var year_local = date.getFullYear();
		var month_local = date.getMonth()+1;
		var day_local = date.getDate();
		if (month_local < 10) month_local = "0"+month_local;
		if (day_local < 10) day_local = "0"+day_local;
		date = new Date(year_local+"-"+month_local+"-"+day_local+"T00:00:00Z");
		date = date.toISOString();
		return date;
	}

	// set NLP mode after button click
	$scope.setMode = function(mode){
		$scope.nlp_mode = mode;
		// console.log($scope.nlp_mode);
	}

	$scope.getListings = function(){
		// Formate date to UTC
		// console.log($scope.startDate);
		$scope.order_option = 0;
		$scope.startDateUTC = convertUTC($scope.startDate);
		$scope.endDateUTC = convertUTC($scope.endDate);
		// console.log("startDate:",$scope.startDateUTC);
		// console.log("endDate:",$scope.endDateUTC);
		
		// Main query function
		listingFactory.getListings($scope.product, $scope.location,$scope.startDateUTC, $scope.endDateUTC, $scope.nlp_mode, function(data){
			// console.log('getListings',data);

			$scope.listings_priceTime = data[0];
			$scope.listings_priceCity = data[1];
			$scope.listings_allItem = data[2];
			showGraphPriceCity($scope.listings_priceCity);
			showGraphPriceTime($scope.listings_priceTime); 

			var data_latest = $scope.listings_priceTime[$scope.listings_priceTime.length-1]
			// console.log($scope.title_results.substring(0,$scope.title_results.substring-1));
			$scope.title_results = $scope.title_results.substring(0,$scope.title_results.length-18)+ "Data Retrieval Completed";
			$scope.title_priceLatest = "Latest Average Price for "+$scope.product_name+" on ("+data_latest._id+"): $"+data_latest.avg_price;
			$scope.title_priceTime = "Daily Average Price for "
				+$scope.product_name+" ("+$scope.location_name+" from "
				+$scope.startDateUTC.substring(0,10)+" to "+$scope.endDateUTC.substring(0,10)+")";
			$scope.title_priceCity = "Average Price Per Location for "+$scope.product_name+" from "
				+$scope.startDateUTC.substring(0,10)+" to "+$scope.endDateUTC.substring(0,10);
			$scope.title_allItems = "Listing of cheapest items for "+$scope.product_name+" ("+$scope.location_name+" from "
				+$scope.startDateUTC.substring(0,10)+" to "+$scope.endDateUTC.substring(0,10)+")";

			// loadGraphPriceCity($scope.listings_priceCity); 
			// console.log('listings_priceTime',$scope.listings_priceTime);
			// console.log('$scope.listings_allItem',$scope.listings_allItem);

		});
		listingFactory.getNumResults($scope.product, $scope.location, $scope.startDateUTC, $scope.endDateUTC, $scope.nlp_mode, function(data){

			$scope.product_name = $scope.products[$scope.product].product;
			$scope.location_name = $scope.locations[$scope.location].location;
			$scope.title_results = "Your Results Based on "+data+" Listings ("+$scope.nlp_mode+" mode) ... Retrieving data...";
		});
	}

	$scope.sortListings = function(){
		// console.log($scope.order_option);

		listingFactory.sortListings($scope.product, $scope.location,$scope.startDateUTC, $scope.endDateUTC, $scope.nlp_mode, $scope.order_option, function(data){
			// console.log(data);
				$scope.listings_allItem = data;
		});
	}

	// Chart of Average-Price-Per-City
	function showGraphPriceTime(data_array){
		var data_chart = [];
		if (data_array.length == 0){
			data_chart = [
				["x","2015-01-01","2015-12-31"],
				["No Data Selected",0,0]
			];
		}
		else{
			data_chart = [
				["x"],
				[$scope.product_name+" ("+$scope.location_name+")"]
			];
			for (var i=0; i<data_array.length; i++){
				data_chart[0].push(data_array[i]['_id']);
				data_chart[1].push(data_array[i]['avg_price']);
			}
			// console.log('data_chart',data_chart);
			// console.log('data_array',data_array);
		}
		$scope.loaded_price_time = data_chart[0];
		$scope.chart_priceTime = c3.generate({
			bindto: "#chart-price-time",
      data: {
        x: 'x',			//xFormat can be used instead (see below comment)
        columns: data_chart
      },
      axis: {
        x: {
          type: 'timeseries',
          tick: {format: '%Y-%m-%d'}
        }
      }
		});
	}
	// 'xFormat' can be used as custom format of 'x'
	// xFormat: '%Y%m%d', 
	// ['x', '20130101', '20130102', '20130103', '20130104', '20130105', '20130106'],

	function showGraphPriceCity(data_array){
		var data_chart = [];
		if (data_array.length == 0){
			data_chart = [["x",$scope.product_name],["No Data Selected","0"]];
		}
		else{
			data_chart = [["x"],[$scope.product_name]];

			for (var i=0; i<data_array.length; i++){
				data_chart[0].push(data_array[i]['_id']);
				data_chart[1].push(data_array[i]['avg_price']);
			}
			// console.log('data_chart',data_chart);
			// console.log('data_array',data_array);
		}
		$scope.loaded_price_city = data_chart[0];
		$scope.chart_priceCity = c3.generate({
			bindto: "#chart-price-city",
	    data: {
	      x:'x',
	      columns: data_chart,
	      type: 'bar'
	    },
	    bar: {
        width: {ratio: 0.5} // width 50% of length between ticks
	    },
	    axis: {
        x: {type: 'category'}, // needed to load string x value
        rotated: true
	    }
		});
	}
});


	// function loadGraphPriceCity(data_array){
	// 	// console.log($scope.loaded_price_city);
	// 	$scope.chart_priceCity.unload({
	// 		ids: $scope.loaded_price_city
	// 	});
	// 	var data_chart = [$scope.products[$scope.product].product];
	// 	for (var i=0; i<data_array.length; i++){
	// 		data_chart.push(data_array[i]['avg_price']);
	// 	}
	// 	console.log('data_chart',data_chart);

	// 	$scope.chart_priceCity.load({
	// 	  columns: [data_chart]
	// 	});
	// 	$scope.loaded_price_city = data_chart[0];
	// }


// //	CHART EXAMPLE
// 	$scope.chart = null;
// 	$scope.config={};
// 	$scope.config.data1="30, 200, 100, 200, 150, 250";
// 	$scope.config.data2="70, 30, 10, 240, 150, 125";

// 	$scope.typeOptions=["line","bar","spline","step","area","area-step","area-spline"];

// 	$scope.config.type1=$scope.typeOptions[0];
// 	$scope.config.type2=$scope.typeOptions[1];


// 	$scope.showGraph = function() {
// 		var config = {};
// 		config.bindto = '#chart';
// 		config.data = {};
// 		config.data.json = {};
// 		config.data.json.data1 = $scope.config.data1.split(",");
// 		console.log(config.data.json.data1);
// 		console.log($scope.config.data1);

// 		config.data.json.data2 = $scope.config.data2.split(",");
// 		config.axis = {"y":{"label":{"text":"Number of items","position":"outer-middle"}}};
// 		config.data.types={"data1":$scope.config.type2,"data2":$scope.config.type2};
// 		$scope.chart = c3.generate(config);		
// 	}

// 	//DIRECTIVE EXAMPLE
// 	$scope.info = {
// 	  firstName: 'John',
// 	  lastName: 'Doe',
// 	  company: 'Trifork'
// 	};

          // ["x","Atlanta","Austin","Boston","Chicago","Dallas","Denver","Detroit","Houston","Las Vegas","Los Angeles","Miami","Minneapolis","New York","Philadelphia","Phoenix","Portland","Raleigh","Sacramento","San Diego","Seattle"],


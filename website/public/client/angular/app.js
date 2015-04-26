//Setting up the angular app (module)
var myApp = angular.module('myApp',['ngRoute']);

//partial code goes in here:
// config method to setup routing
myApp.config(function($routeProvider,$locationProvider){
	$routeProvider
		.when('/',{
			title: 'Get the right price!',
			templateUrl: 'partials/home.html',
			controller: 'listingCtrl'
		})
		.otherwise({
			redirectTo: '/'
		});

		// use the HTML5 History API
    $locationProvider.html5Mode(true);
});


//TEST DIRECTIVE
myApp.directive('paramlessattribute', function() {
  return {
    template: '{{ info.firstName }} {{ info.lastName }} works at <input type="text" value="{{ info.company }}" ng-model="info.company" />'
  };
});

//change document title when route change between partials is successful
myApp.run(['$location', '$rootScope', function($location, $rootScope) {
    $rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
        $rootScope.title = current.$$route.title;
    });
}]);
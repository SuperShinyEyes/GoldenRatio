'use strict';

console.log("ApartmentService initializing");
class ApartmentService {
    constructor($http) {
        console.log("construct");
        this.$http = $http;
    }
    getAds(maxNumberOfStops, maxWalkingDistance) {
        return this.$http.get('example.json', {
            //cache: true,
            params: {
                maxNumberOfStops,
                maxWalkingDistance
            }
        });
    }
}

ApartmentService.$inject = ['$http'];

export default ApartmentService;

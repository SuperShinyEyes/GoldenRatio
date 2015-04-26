'use strict';

class ApartmentService {
    constructor($http) {
        console.log("construct");
        this.$http = $http;
    }
    getAds(maxNumberOfStops, maxWalkingDistance) {
        return this.$http.get('http://aww.fi:4000', {
            cache: true,
            params: {
                url: 'http://kumartest.cloudapp.net:8080/hackserver-0.1/dataserver.jsp?lat=60.187078&lng=24.815548&maxStop=' + maxNumberOfStops +'&maxWalk=' + maxWalkingDistance + '&callback=claudio'
            }
        });
    }
}

ApartmentService.$inject = ['$http'];

export default ApartmentService;

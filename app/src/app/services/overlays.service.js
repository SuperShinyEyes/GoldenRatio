'use strict';

class OverlayService {
    constructor($http) {
        this.$http = $http;
    }
    getList() {
        return this.$http.get('http://jsonp.afeld.me', {
            cache: true,
            params: {
                url: 'http://app.gradesystem.eu:9090/service/prod/query/listoverlays/results.json'
            }
        });
    }
    get(id) {
        return this.$http.get('http://jsonp.afeld.me', {
            cache: true,
            params: {
                url: 'http://app.gradesystem.eu:9090/service/prod/query/getoverlay/results.json?id=' + id
            }
        });
    }
}

OverlayService.$inject = ['$http'];

export default OverlayService;

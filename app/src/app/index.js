'use strict';

import MainCtrl from './main/main.controller';
import NavbarCtrl from '../app/components/navbar/navbar.controller';
import ApartmentService from '../app/services/apartments.service.js';
import OverlayService from '../app/services/overlays.service.js';

angular.module('goldenratio', ['ngAnimate', 'ngCookies', 'ngTouch', 'ngSanitize', 'ngResource', 'ui.router', 'ui.bootstrap', 'ui.bootstrap.tooltip', 'ui.bootstrap-slider', 'uiGmapgoogle-maps', 'leaflet-directive'])
  .controller('MainCtrl', MainCtrl)
  .controller('NavbarCtrl', NavbarCtrl)
  .service('ApartmentService', ApartmentService)
  .service('OverlayService', OverlayService)
  .config(function(uiGmapGoogleMapApiProvider) {
      uiGmapGoogleMapApiProvider.configure({
          key: 'AIzaSyC3K_IVjZkGYxqybUCbWa9t0heG8ZHjt5s',
          v: '3.17',
          libraries: 'weather,geometry,visualization'
      });
  })
  .config(function ($stateProvider, $urlRouterProvider) {
    $stateProvider
      .state('home', {
        url: '/',
        templateUrl: 'app/main/main.html',
        controller: 'MainCtrl'
      });

    $urlRouterProvider.otherwise('/');
  })
;

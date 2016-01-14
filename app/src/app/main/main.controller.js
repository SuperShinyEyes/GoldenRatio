'use strict';

class MainCtrl {
  constructor ($scope, ApartmentService, OverlayService, uiGmapGoogleMapApi, $timeout) {
    $scope.maxNumberOfStops = 10;
    $scope.maxWalkingDistance = 500;
    $scope.apartments = null;
    $scope.overlays = null;
    $scope.heatmaps = {};
    angular.extend($scope, {
      map: {
        center: {
          lat: 60.186255,
          lng: 24.82843,
          zoom: 16
        },
        markers: {},
        layers: {
          baselayers: {
              mapbox_light: {
                  name: 'Mapbox Light',
                  url: 'http://api.tiles.mapbox.com/v4/{mapid}/{z}/{x}/{y}.png?access_token={apikey}',
                  type: 'xyz',
                  layerOptions: {
                      apikey: 'pk.eyJ1IjoiYnVmYW51dm9scyIsImEiOiJLSURpX0pnIn0.2_9NrLz1U9bpwMQBhVk97Q',
                      mapid: 'bufanuvols.lia22g09'
                  }
              }
          },
          overlays: {}
        }
      }
    });
    /*
    $timeout(function(){
      $scope.map.layers.overlays = {
          heat: {
              name: 'Heat Map',
              type: 'heat',
              data: [
                [60.186255, 24.82843],
                [60.186265, 24.82843],
                [60.186285, 24.82843],
                [37.782745, -122.444586],
                [37.782842, -122.443688],
                [37.782919, -122.442815],
                [37.782992, -122.442112],
                [37.783100, -122.441461],
                [37.783206, -122.440829],
                [37.783273, -122.440324],
                [37.783316, -122.440023],
                [37.783357, -122.439794]
              ],
              layerOptions: {
                  radius: 20,
                  blur: 10
              },
              visible: true
          }
      };
    }, 4000);
*/
    /*
    uiGmapGoogleMapApi.then(function(maps){
      $scope.$apply(function(){
        $scope.taxiData = [
          {
            location: new maps.LatLng(60.186255, 24.82843),
            weight: 1000
          },
          {
            location: new maps.LatLng(60.187255, 24.82843),
            weight: 100
          },
          {
            location: new maps.LatLng(60.189255, 24.82843),
            weight: 10
          },
          {
            location: new maps.LatLng(60.184205, 24.82843),
            weight: 10
          },
        ];
        console.log('Loaded', $scope.taxiData);
      });
    });
    */
    /*$scope.$on('mapInitialized', function(event, evtMap) {
      //bb
    });*/
    $scope.activateOverlays = [];
    $scope.activateOverlay = function(id){
      if (_.include($scope.activateOverlays, id)) {
        $scope.activateOverlays = _.without($scope.activateOverlays, id);
      } else {
        $scope.activateOverlays.push(id);
      }
    };
    OverlayService.getList().then(function(response){
      $scope.overlays = _.map(
        response.data.results.bindings,
        function(x){ return {id: x.overlay_id.value, label: x.overlay_label.value}; }
      );
    });



    /*[
      {
        ''
      }
    ];*/

    $scope.$watchGroup(['maxNumberOfStops', 'maxWalkingDistance'], function(newValues, oldValues, scope) {
      ApartmentService.getAds($scope.maxNumberOfStops, $scope.maxWalkingDistance).then(function(response){
        $scope.apartments = _.uniq(response.data, 'url');
      });
    });
    $scope.$watch('apartments', function(){
      $scope.map.markers = {};
      _.forEach($scope.apartments, function(x){
        $scope.map.markers['marker'+_.last(x.url.split('/'))] = {
          lat: parseFloat(x.lat),
          lng: parseFloat(x.lng),
          message: x.address + ' (bus '+x.bus_line.slice(1)+')'
        };
      });
    }, true);


    $scope.$watch('activateOverlays', function(newValues, oldValues) {
      $scope.heatmaps = {};
      $.each($scope.activateOverlays, function(i, id){
        OverlayService.get(id).then(function(response){
          var processed = _.map(
            response.data.results.bindings,
            function(x){ return [
                parseFloat(x.location.value.split(',')[0]),
                parseFloat(x.location.value.split(',')[1]),
              ]; }
          );
          $scope.heatmaps[id] = processed;
        });
      });
    }, true);

    $scope.$watch('heatmaps', function(){
      var all = [];
      for (var key in $scope.heatmaps) {
        all = all.concat($scope.heatmaps[key]);
      }
      if (all.length === 0) {
        delete $scope.map.layers.overlays.heat;
      } else {
        /*all = [
          [60.186255, 24.82843],
          [60.186265, 24.82843],
          [60.186285, 24.82843],
        ];*/
        $scope.map.layers.overlays.heat = {
              name: 'Heat Map',
              type: 'heat',
              data: all,
              layerOptions: {
                  minOpacity: 0.4,
                  radius: 20,
                  blur: 10
              },
              visible: true
        };
      }
    }, true);
    /*ApartmentService.getAds($scope.maxNumberOfStops, $scope.maxWalkingDistance).then(function(response){
      $scope.apartments = response.data;
      console.log("Apartments are saved as ", $scope.apartments);
    });*/
/*
    $scope.map = {
      center: {
        latitude: 60.186255,
        longitude: 24.82843
      },
      zoom: 16
    };
    */
  }
}

MainCtrl.$inject = ['$scope', 'ApartmentService', 'OverlayService', 'uiGmapGoogleMapApi', '$timeout'];

export default MainCtrl;

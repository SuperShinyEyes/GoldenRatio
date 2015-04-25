'use strict';

var gulp = require('gulp');

var $ = require('gulp-load-plugins')();

var wiredep = require('wiredep').stream;

module.exports = function(options) {
  gulp.task('inject', ['scripts', 'styles'], function () {
    var injectStyles = gulp.src([
      options.tmp + '/serve/app/**/*.css',
      'bower_components/seiyria-bootstrap-slider/dist/css/bootstrap-slider.css',
      'bower_components/leaflet/dist/leaflet.css',
      'bower_components/leaflet.markercluster/dist/MarkerCluster.css',
      'bower_components/leaflet.markercluster/dist/MarkerCluster.Default.css',
      '!' + options.tmp + '/serve/app/vendor.css'
    ], { read: false });


    /*

    <script src="../bower_components/leaflet/dist/leaflet.js"></script>
    <script src="../dist/angular-leaflet-directive.min.js"></script>
    <link rel="stylesheet" href="../bower_components/leaflet/dist/leaflet.css" />
    */
    var injectScripts = gulp.src([
      options.tmp + '/serve/app/**/*.js',
      'bower_components/bootstrap/dist/js/bootstrap.js',
      'bower_components/seiyria-bootstrap-slider/js/bootstrap-slider.js',
      'bower_components/angular-bootstrap-slider/slider.js',
      'bower_components/lodash/dist/lodash.js',
      'bower_components/angular-google-maps/dist/angular-google-maps.js',
      'bower_components/leaflet/dist/leaflet.js',
      'bower_components/Leaflet.heat/dist/leaflet-heat.js',
      'bower_components/leaflet.markercluster/dist/leaflet.markercluster.js',
      'bower_components/angular-leaflet/dist/angular-leaflet-directive.js',
      '!' + options.src + '/app/**/*.spec.js',
      '!' + options.src + '/app/**/*.mock.js'
    ], { read: false });

    var injectOptions = {
      ignorePath: [options.src, options.tmp + '/serve'],
      addRootSlash: false
    };

    return gulp.src(options.src + '/*.html')
      .pipe($.inject(injectStyles, injectOptions))
      .pipe($.inject(injectScripts, injectOptions))
      .pipe(wiredep(options.wiredep))
      .pipe(gulp.dest(options.tmp + '/serve'));

  });
};

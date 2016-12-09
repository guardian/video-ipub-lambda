var gulp = require('gulp');
var yaml = require('gulp-yaml');
var zip = require('gulp-zip');
var path = require('path');
var file = require('gulp-file');
var riffraff = require('node-riffraff-artefact');
var babel = require('gulp-babel');
var exec  = require('exec-chainable');
process.env.VERBOSE = "true"
process.env.ARTEFACT_PATH = __dirname;


gulp.task('riffraff-deploy', function () {
  return gulp.src('riff-raff.yaml')
    .pipe(yaml({ space: 4 }))
    .pipe(gulp.dest('tmp'));
});

gulp.task('riffraff-archive', [
  'riffraff-deploy',
], function () {
  return gulp.src(['**/video-ipub-lambda.zip','riff-raff.yaml'])
    .pipe(zip('artifacts.zip'))
    .pipe(gulp.dest('tmp'));
});

gulp.task('deploy', ['riffraff-archive'], function (cb) {
  riffraff.settings.leadDir = path.join(__dirname, 'tmp');
  riffraff.s3Upload().then(function () {
    console.log('uploaded!')
    cb();
  }).catch(function (error) {
    cb(error);
  });

});
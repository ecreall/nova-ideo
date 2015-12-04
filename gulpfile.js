var gulp = require('gulp');
var webserver = require("gulp-webserver")
var babelify = require('babelify');
var browserify = require('browserify');
var through2 = require('through2');
var del = require('del');
var runSequence = require('run-sequence');
var merge = require('merge-stream');
var envify = require('loose-envify/custom');

// http://nadikun.com/how-to-add-autoprefixer-to-work-with-bootstrap-using-less/
var less = require('gulp-less');
var autoprefixer = require('gulp-autoprefixer');
var minifyCSS = require('gulp-minify-css');
var gutil = require('gulp-util');
var sourcemaps = require('gulp-sourcemaps');

var outputDir = 'novaideo/static';
var mapFile = 'main.map.json';
var mapOutput = outputDir + '/js/' + mapFile;
var env = process.env.NODE_ENV || 'development';


gulp.task('clean', function (cb) {
  del([
    outputDir+'/main.*',
  ], cb);
});

gulp.task('browserify', function() {
    return gulp.src('./novaideo/js/main.js')
        .pipe(through2.obj(function (file, enc, next) {
            var bundler = browserify(file.path, {debug: true})
                .transform(babelify);
            bundler.transform(envify({ NODE_ENV: env }))
            if (env === 'production') {
                bundler.plugin('minifyify', {map: mapFile, output: mapOutput});
            }
            bundler.bundle(function (err, res) {
                if (err) { return next(err); }
                file.contents = res;
                next(null, file);
            });
        }))
        .on('error', function (error) {
            console.log(error.stack);
            this.emit('end');
        })
        .pipe(gulp.dest(outputDir + '/js'));
});

// https://github.com/twbs/bootstrap/blob/master/grunt/configBridge.json#L21
var autoprefixers = [
      "Android 2.3",
      "Android >= 4",
      "Chrome >= 20",
      "Firefox >= 24",
      "Explorer >= 8",
      "iOS >= 6",
      "Opera >= 12",
      "Safari >= 6"];
gulp.task('less', function() {
    return gulp.src('./novaideo/static/less/bootstrap*.less')
        .pipe(sourcemaps.init())
          .pipe(less().on('error', gutil.log))
          .pipe(autoprefixer(autoprefixers))
          .pipe(minifyCSS())
        .pipe(sourcemaps.write('../maps'))
        .pipe(gulp.dest('./novaideo/static/css/'));
});

// Async task with multiple gulp.src https://github.com/gulpjs/gulp/issues/82
gulp.task('copy', function() {
    return merge(
        gulp.src('node_modules/bootstrap/fonts/*')
            .pipe(gulp.dest('novaideo/static/fonts/'))
    );
});

gulp.task('build', function(callback) {
    runSequence('clean', ['browserify', 'less', 'copy'], callback);
});

gulp.task('webserver', function() {
    return gulp.src(outputDir)
        .pipe(webserver({
            livereload: false,
            open: false
        }));
});

gulp.task('watch', function() {
    gulp.watch('novaideo/js/**/*.js', ['browserify']);
    gulp.watch('novaideo/static/less/**/*.less', ['less']);
});

gulp.task('default', function(callback) {
    runSequence('build', 'webserver', 'watch', callback);
});

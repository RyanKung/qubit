const gulp = require('gulp');
const react = require('gulp-react');
const babel = require('gulp-babel');
const webpack = require('webpack-stream');
const run = require('run-sequence')
const rename = require('gulp-rename')
const uglify = require('gulp-uglify');
const sass = require('gulp-sass');
const cleanCSS = require('gulp-clean-css');


const paths = {
    es6_src: ['src/js/**/*.es6'],
    jsx_src: ['src/js/**/*.jsx'],
    scss_src: ['src/css/**/*.sass'],
}

gulp.task('default', function (done) {
    return run('js', 'css', done);
});

gulp.task('js', function(done) {
    return run('babel', 'pack_js', done);
})

gulp.task('css', function(done) {
    return run('sass', 'minify-css', done);
})

gulp.task('babel', function () {
    return gulp.src(paths.es6_src)
        .pipe(babel({
            presets: ['es2015', 'react']
        }))
        .pipe(gulp.dest('compiled/js'))
});


gulp.task('sass', function () {
    return gulp.src('src/css/main.sass')
        .pipe(sass().on('error', sass.logError))
        .pipe(rename({basename: 'qubit', extname: '.css'}))
        .pipe(gulp.dest('./dist/css'));
});


gulp.task('minify-css', function() {
  return gulp.src('dist/css/main.css')
        .pipe(cleanCSS({compatibility: 'ie8'}))
        .pipe(rename({basename: 'qubit', extname: '.min.css'}))
        .pipe(gulp.dest('dist/css'));
});

gulp.task('watch', function () {
    gulp.watch(paths.es6_src, ['js']);
    gulp.watch(paths.scss_src, ['css']);

});


gulp.task('pack_js', function (done) {
  return gulp.src('compiled/js/main.js')
        .pipe(webpack({
            resolve: {
                root: [
                    process.cwd() + '/src/js',
                    process.cwd() + '/compiled/js'
                ]
            }
        }))
        .pipe(rename({basename: 'qubit', extname: '.js'}))
        .pipe(gulp.dest('./dist/js'))
        // .pipe(uglify())
        // .pipe(rename({basename:'qubit', extname: '.min.js'}))
        // .pipe(gulp.dest('./dist/js'));
});

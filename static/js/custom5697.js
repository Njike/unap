/************************************
    File Name: custom.js
    Template Name: Awards
    Created By: Similar Icons
    Envato Profile: http://themeforest.net/user/similaricons
    Website: https://similaricons.com
    Version: 1.0
************************************/

(function($) {
    "use strict";

    //Navigation Menu Slider
    $(document).ready(function() {
        $('#nav-expander').on('click', function(e) {
            e.preventDefault();
            $('body').toggleClass('nav-expanded');
        });
        $('#nav-close').on('click', function(e) {
            e.preventDefault();
            $('body').removeClass('nav-expanded');
        });

        // Initialize navgoco with default options
        $(".main-menu").navgoco({
            caret: '<span class="caret"></span>',
            accordion: false,
            openClass: 'open',
            save: true,
            cookie: {
                name: 'navgoco',
                expires: false,
                path: '/'
            },
            slide: {
                duration: 300,
                easing: 'swing'
            }
        });
    });

    $(window).load(function() {
        $("#preloader").on(500).fadeOut();
        $(".preloader").on(600).fadeOut("slow");
    });

    $('select').selectpicker();
    $('[data-toggle="tooltip"]').tooltip();

})(jQuery);
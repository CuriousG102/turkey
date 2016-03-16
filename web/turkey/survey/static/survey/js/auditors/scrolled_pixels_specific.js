var AuditorScrolledPixelsSpecific = {
    scrolled_pixels_specific: [],
    previous_position_h: 0,
    previous_position_v: 0,
    setup: function() {
        this.previous_position_h = $(window).scrollLeft();
        this.previous_position_v = $(window).scrollTop();

        // https://github.com/cowboy/jquery-throttle-debounce
        (function(b,c){var $=b.jQuery||b.Cowboy||(b.Cowboy={}),a;$.throttle=a=function(e,f,j,i){var h,d=0;if(typeof f!=="boolean"){i=j;j=f;f=c}function g(){var o=this,m=+new Date()-d,n=arguments;function l(){d=+new Date();j.apply(o,n)}function k(){h=c}if(i&&!h){l()}h&&clearTimeout(h);if(i===c&&m>e){l()}else{if(f!==true){h=setTimeout(i?k:l,i===c?e-m:e)}}}if($.guid){g.guid=j.guid=j.guid||$.guid++}return g};$.debounce=function(d,e,f){return f===c?a(d,e,false):a(d,f,e!==false)}})(this);
    }
    log_scroll_specific: function () {
        // horizontal
        var current_position_h = $(window).scrollLeft();
        var raw_amount_h = current_position_h - previous_position_h;
        var horizontal = { 'position' : current_position_h, 'change' : raw_amount_h };
        previous_position_h = current_position_h;

        // vertical
        var current_position_v = $(window).scrollTop();
        var raw_amount_v = current_position_v - previous_position_v;
        var vertical = { 'position' : current_position_v, 'change' : raw_amount_v };
        previous_position_v = current_position_v;

        this.scrolled_pixels_specific.push(
            {
                'horizontal'    : horizontal,
                'vertical'      : vertical
            }
        );
    },
    submit_callable: function () {
        return this.scrolled_pixels_specific;
    }
};

var auditor_scrolled_pixels_specific = Object.create(AuditorScrolledPixelsSpecific);
auditor_scrolled_pixels_specific.setup();

$(window).scroll(
    $.debounce(250, function(e) { 
        auditor_scrolled_pixels_specific
            .log_scroll_specific
            .bind(auditor_scrolled_pixels_specific);
    });
);

overlord.register_auditor('scrolled_pixels_specific',
                          auditor_scrolled_pixels_specific
                            .submit_callable
                            .bind(auditor_scrolled_pixels_specific));
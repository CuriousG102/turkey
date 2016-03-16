var AuditorScrolledPixelsTotal = {
    scrolled_pixels_total_h: 0,
    previous_position_h: 0,
    scrolled_pixels_total_v: 0,
    previous_position_v: 0,
    setup: function() {
        this.previous_position_h = $(window).scrollLeft();
        this.previous_position_v = $(window).scrollTop();

        // https://github.com/cowboy/jquery-throttle-debounce
        (function(b,c){var $=b.jQuery||b.Cowboy||(b.Cowboy={}),a;$.throttle=a=function(e,f,j,i){var h,d=0;if(typeof f!=="boolean"){i=j;j=f;f=c}function g(){var o=this,m=+new Date()-d,n=arguments;function l(){d=+new Date();j.apply(o,n)}function k(){h=c}if(i&&!h){l()}h&&clearTimeout(h);if(i===c&&m>e){l()}else{if(f!==true){h=setTimeout(i?k:l,i===c?e-m:e)}}}if($.guid){g.guid=j.guid=j.guid||$.guid++}return g};$.debounce=function(d,e,f){return f===c?a(d,e,false):a(d,f,e!==false)}})(this);
    },
    log_scroll_event: function () {
        // horizontal
        var current_position_h = $(window).scrollLeft();
        if(current_position_h != previous_position_h) {
            var raw_amount_h = current_position_h - previous_position_h;
            var amount_h = Math.abs(raw_amount_h);
            this.scrolled_pixels_total_h += amount_h;
            previous_position_h = current_position_h;
        }

        // vertical
        var current_position_v = $(window).scrollTop();
        if(current_position_v != previous_position_v) {
            var raw_amount_v = current_position_v - previous_position_v;
            var amount_v = Math.abs(raw_amount_v);
            this.scrolled_pixels_total_v += amount_v;
            previous_position_v = current_position_v;
        }
    },
    submit_callable: function () {
        return {
            'horizontal': this.scrolled_pixels_total_h,
            'vertical'  : this.scrolled_pixels_total_v
        };
    }
};

var auditor_scrolled_pixels_total = Object.create(AuditorScrolledPixelsTotal);
auditor_scrolled_pixels_total.setup();

$(window).scroll(
    $(window).scroll(auditor_scrolled_pixels_total
        .log_scroll_event
        .bind(auditor_scrolled_pixels_total);
    });
);

overlord.register_auditor('scrolled_pixels_total',
                          auditor_scrolled_pixels_total
                            .submit_callable
                            .bind(auditor_scrolled_pixels_total));
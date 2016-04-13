var AuditorScrolledPixelsSpecific = {
    scrolled_pixels_specific: [],
    previous_position_h: 0,
    previous_position_v: 0,
    setup: function() {
        this.previous_position_h = $(window).scrollLeft();
        this.previous_position_v = $(window).scrollTop();
    },
    log_scroll_specific: function () {
        // horizontal
        var current_position_h = $(window).scrollLeft();
        var raw_amount_h = current_position_h - this.previous_position_h;
        // var horizontal = { 'position_h' : current_position_h, 'change_h' : raw_amount_h };
        this.previous_position_h = current_position_h;

        // vertical
        var current_position_v = $(window).scrollTop();
        var raw_amount_v = current_position_v - this.previous_position_v;
        // var vertical = { 'position_v' : current_position_v, 'change_v' : raw_amount_v };
        this.previous_position_v = current_position_v;

        this.scrolled_pixels_specific.push(
            {
                // 'horizontal'    : horizontal,
                // 'vertical'      : vertical
                'position_h': current_position_h,
                'change_h'  : raw_amount_h,
                'position_v': current_position_v,
                'change_v'  : raw_amount_v
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
            .bind(auditor_scrolled_pixels_specific)();
    })
);

overlord.register_auditor('scrolled_pixels_specific',
                          auditor_scrolled_pixels_specific
                            .submit_callable
                            .bind(auditor_scrolled_pixels_specific));
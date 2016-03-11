var AuditorScrolledVerticalPixelsSpecific = {
    // start_date: new Date(),
    scrolled_vertical_pixels_specific: [],
    previous_position: 0,
    log_vscroll_specific: function (e) {
        var current_position = $(window).scrollTop();
        // var timestamp = ((new Date()).getTime() - start_date.getTime()) / 1000.0;

        var rawAmount = current_position - previous_position;
        
        if(current_position != previous_position) {
            this.scrolled_vertical_pixels_specific.push({ 'position' : current_position, 'change' : rawAmount });
            // this.scrolled_vertical_pixels_specific.push({ 'timestamp' : timestamp, 'position' : current_position, 'change' : rawAmount });
            
            previous_position = current_position;
        }
    },
    submit_callable: function () {
        return {
            'content':  this.scrolled_vertical_pixels_specifics
        };
    }
};

var auditor_scrolled_vertical_pixels_specific = Object.create(AuditorScrolledVerticalPixelsSpecific);

$(document).ready(function() {
    $(window).scroll(auditor_scrolled_vertical_pixels_specific
                            .log_vscroll_specific
                            .bind(auditor_scrolled_vertical_pixels_specific));
});

overlord.register_auditor('scrolled_vertical_pixels_specific',
                          auditor_scrolled_vertical_pixels_specific
                            .submit_callable
                            .bind(auditor_scrolled_vertical_pixels_specific));
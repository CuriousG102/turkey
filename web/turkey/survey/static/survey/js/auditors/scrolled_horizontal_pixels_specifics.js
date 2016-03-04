var AuditorScrolledHorizontalPixelsSpecific = {
    // start_date: new Date(),
    scrolled_horizontal_pixels_specific: [],
    previous_position: 0,
    log_hscroll_specific: function (e) {
        var current_position = $(window).scrollLeft();
        // var timestamp = ((new Date()).getTime() - start_date.getTime()) / 1000.0;

        var rawAmount = current_position - previous_position;
        previous_position = current_position;
        
        this.scrolled_horizontal_pixels_specific.push({ 'position' : current_position, 'change' : rawAmount });
        // this.scrolled_horizontal_pixels_specific.push({ 'timestamp' : timestamp, 'position' : current_position, 'change' : rawAmount });
    },
    submit_callable: function () {
        return {
            'content':  this.scrolled_horizontal_pixels_specifics != []
                        ?
                        this.scrolled_horizontal_pixels_specifics
                        :
                        null
        };
    }
};

var auditor_scrolled_horizontal_pixels_specific = Object.create(AuditorScrolledHorizontalPixelsSpecific);

$(document).ready(function() {
    $(window).scroll(auditor_scrolled_horizontal_pixels_specific
                            .log_hscroll_specific
                            .bind(auditor_scrolled_horizontal_pixels_specific));
});

overlord.register_auditor('scrolled_horizontal_pixels_specific',
                          auditor_scrolled_horizontal_pixels_specific
                            .submit_callable
                            .bind(auditor_scrolled_horizontal_pixels_specific));
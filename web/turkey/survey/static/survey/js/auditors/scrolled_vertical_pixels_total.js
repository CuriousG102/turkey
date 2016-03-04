var AuditorScrolledVerticalPixelsTotal = {
    scrolled_vertical_pixels_total: 0,
    previous_position: 0,
    log_vscroll_event: function (e) {
        var current_position = $(window).scrollTop();
        
        if(current_position != previous_position) {
            var rawAmount = current_position - previous_position;
            var amount = Math.abs(rawAmount);

            this.scrolled_vertical_pixels_total += amount;

            previous_position = current_position;
        }
    },
    submit_callable: function () {
        return {
            'amount': this.scrolled_vertical_pixels_total
        };
    }
};

var auditor_scrolled_vertical_pixels_total = Object.create(AuditorScrolledVerticalPixelsTotal);

$(document).ready(function() {
    $(window).scroll(auditor_scrolled_vertical_pixels_total
                            .log_vscroll_event
                            .bind(auditor_scrolled_vertical_pixels_total));
});

overlord.register_auditor('scrolled_vertical_pixels_total',
                          auditor_scrolled_vertical_pixels_total
                            .submit_callable
                            .bind(auditor_scrolled_vertical_pixels_total));
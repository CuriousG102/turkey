var AuditorClicksTotal = {
    clicks_total: 0,
    log_click_event: function (e) {
        e.stopPropagation();
        this.clicks_total += 1;
    },
    submit_callable: function () {
        return {
            'count': this.clicks_total
        };
    }
};

var auditor_clicks_total = Object.create(AuditorClicksTotal);

$(document).ready(function() {
    $(document).click(auditor_clicks_total
                            .log_click_event
                            .bind(auditor_clicks_total));
});

overlord.register_auditor('clicks_total',
                          auditor_clicks_total
                            .submit_callable
                            .bind(auditor_clicks_total));
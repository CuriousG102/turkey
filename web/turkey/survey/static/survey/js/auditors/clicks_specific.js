var AuditorClicksSpecifics = {
    clicks_specifics: [],
    log_click_content: function (e) {
        e.stopPropagation();
        this.clicks_specifics.push(e.target);
    },
    submit_callable: function () {
        return {
            'content':  this.clicks_specifics
        };
    }
};

var auditor_clicks_specifics = Object.create(AuditorClicksSpecifics);

$(document).ready(function() {
    $(document).click(auditor_clicks_specifics
                            .log_click_content
                            .bind(auditor_clicks_specifics));
});

overlord.register_auditor('clicks_specifics',
                          auditor_clicks_specifics
                            .submit_callable
                            .bind(auditor_clicks_specifics));
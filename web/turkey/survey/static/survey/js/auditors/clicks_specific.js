var AuditorClicksSpecific = {
    start_date: new Date(),
    clicks_specific: [],
    log_click_content: function (e) {
        var dom = {
            'dom_type'  :   e.target.nodeName.toLowerCase(),
            'dom_id'    :   e.target.id != '' && e.target.id != undefined
                            ? e.target.id : null,
            'dom_class' :   e.target.className != '' && e.target.className != undefined
                            ? e.target.className : null,
            'dom_name'  :   $(e.target).attr('name') != '' && $(e.target).attr('name') != undefined
                            ? $(e.target).attr('name') : null,
            'time'      :   (new Date()).getTime() - this.start_date.getTime()
        };
        this.clicks_specific.push(dom);
    },
    submit_callable: function () {
        return this.clicks_specific;
    }
};

var auditor_clicks_specific = Object.create(AuditorClicksSpecific);

$(document).ready(function() {
    $(document).click(auditor_clicks_specific
                            .log_click_content
                            .bind(auditor_clicks_specific));
});

turkey.register_auditor('clicks_specific',
                          auditor_clicks_specific
                            .submit_callable
                            .bind(auditor_clicks_specific));
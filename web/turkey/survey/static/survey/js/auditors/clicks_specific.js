var AuditorClicksSpecific = {
    clicks_specific: [],
    log_click_content: function (e) {
        var dom = {
            'dom_type' :   e.target.nodeName.toLowerCase(),
            'dom_id'   :   e.target.id != '' && e.target.id != undefined 
                            ? e.target.id : null,
            'dom_class':   e.target.class != '' && e.target.class != undefined 
                            ? e.target.class : null,
            'dom_name' :   e.target.name != '' && e.target.name != undefined 
                            ? e.target.name : null                
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

overlord.register_auditor('clicks_specific',
                          auditor_clicks_specific
                            .submit_callable
                            .bind(auditor_clicks_specific));
var AuditorURL = {
    get_url: function() {
        this.url = window.location.href;
    },
    submit_callable: function() {
        return {
            "url" : this.url
        };
    }
};

var auditor_url = Object.create(AuditorURL);

$(document).ready(function() {
    auditor_url.get_url();
});

turkey.register_auditor('url',
                          auditor_url
                            .submit_callable
                            .bind(auditor_url));
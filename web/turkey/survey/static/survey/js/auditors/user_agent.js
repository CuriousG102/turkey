var AuditorUserAgent = {
    // ua = {},
    get_user_agent: function() {
        var uas = navigator.userAgent;
        // uas = encodeURI(uas);

        // var url = "http://www.useragentstring.com/?uas="
        //     + uas
        //     + "&getJSON=all";
        
        // $.ajax({
        //     type: "GET",
        //     url: url,
        //     async: true,
        //     dataType: "jsonp",
        //     crossDomain: true,
        //     success: function(data) {
        //         this.ua = data;
        //     }
        // });
    },
    submit_callable: function() {
        return {
            "user_agent" : uas
        };
    }
}

var auditor_user_agent = Object.create(AuditorUserAgent);

$(document).ready(function() {
    auditor_user_agent.get_user_agent();
});

overlord.register_auditor('user_agent',
                          auditor_user_agent
                            .submit_callable
                            .bind(auditor_user_agent));
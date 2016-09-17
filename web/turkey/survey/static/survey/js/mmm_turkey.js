var AuditorHandler = function (submission_endpoint, fetch_interaction_endpoint,
                               task_pk, fetch_interaction) {
    this.auditors = [];
    this.submission_endpoint = submission_endpoint;
    this.TIMEOUT = 10 * Math.pow(10, 3); // seconds
    if (fetch_interaction) {
        $.post({
            url: fetch_interaction_endpoint,
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({'task_pk': task_pk}),
            async: false,
            success: function(data, txt, xhr) {
               if (xhr.status !== 201) {
                    console.error(data);
                    console.error(xhr);
                }
                this.submission_endpoint = data['auditor_submission_url'];
            }.bind(this),
            error: function (data) {
                console.error(data);
            }
        });
    }
    $(window).ready(function () {
        $(window).on('unload', function() {
            this.submit();
        }.bind(this));
    }.bind(this));
};

AuditorHandler.prototype.register_auditor = function(name, callback) {
    this.auditors.push([name, callback]);
};

AuditorHandler.prototype.submit = function() {
    var submission = {
        'auditors': {}
    };

    $.each(this.auditors, function(i, el) {
        var name = el[0], callback = el[1];
        submission['auditors'][name] = callback();
    });

    $.post({
        url: this.submission_endpoint,
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(submission),
        timeout: this.TIMEOUT,
        async: false,
        success: function(data, txt, xhr) {
           if (xhr.status !== 201) {
                console.error(data);
                console.error(xhr);
            }
        },
        error: function (data) {
            console.error(data);
        }
    });
};



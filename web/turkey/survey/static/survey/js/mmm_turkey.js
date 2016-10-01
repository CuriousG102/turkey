var AuditorHandler = function (interaction_manager) {
    this.auditors = [];
    this.TIMEOUT = 10 * Math.pow(10, 3); // seconds
    interaction_manager.get_interaction(function (endpoints, token) {
        this.submission_endpoint = endpoints['auditor_submission_endpoint'];
        this.token = token;
    }.bind(this));
    $(window).ready(function () {
        window.onbeforeunload = function() {
            this.submit();
        }.bind(this);
    }.bind(this));
};

AuditorHandler.prototype.register_auditor = function(name, callback) {
    this.auditors.push([name, callback]);
};

AuditorHandler.prototype.submit = function() {
    var submission = {
        'auditors': {},
        'token': this.token
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
        success: function(data, txt, xhr) {
           if (xhr.status !== 201) {
                console.error(data);
                console.error(xhr);
            }
        },
        error: function (data) {
            console.error(data);
            console.error(submission);
        }
    });
};



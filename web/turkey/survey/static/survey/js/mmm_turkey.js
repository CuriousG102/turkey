var AuditorHandler = function (endpoint) {
    this.auditors = [];
    this.submission_endpoint = endpoint;
    $(window).on('unload', function() {
        this.submit();
    })
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



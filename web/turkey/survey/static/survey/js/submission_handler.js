/**
 * Created by Miles on 9/10/16.
 */
var NOT_READY_TO_SUBMIT = "whoops";

var SubmissionHandler = function(endpoint, next_page) {
    this.submission_endpoint = endpoint;
    this.next_page = next_page;
    this.steps = [];
    this.posting = false;
};

SubmissionHandler.prototype.register_step = function(name, callback) {
    this.steps.push([name, callback]);
};

SubmissionHandler.prototype.submit = function() {
    if (this.posting) {
        window.alert('Submission in progress, please wait.');
        return;
    }

    this.posting = true;
    var submission = {
        'steps': {}
    };

    var error_func = function() {
        window.alert('Submission failed. Please try again.');
    };

    var unsuccessful = false;
    $.each(this.steps, function(i, el) {
        var name = el[0], callback = el[1];
        try {
            submission['steps'][name] = callback();
        } catch (err) {
            unsuccessful = true;
        }
    });

    if (unsuccessful) {
        this.posting = false;
        error_func();
        return;
    }

    $.post({
        url: this.submission_endpoint,
        contentType:"application/json; charset=utf-8",
        data: JSON.stringify(submission),
        timeout: 10 * Math.pow(10, 3), // seconds
        success: function (data, txt, xhr) {
            this.posting = false;
            if (xhr.status !== 201) {
                console.error(data);
                console.error(xhr);
                error_func();
            }
            // window.alert("Success!");
            window.location.replace(this.next_page);
        }.bind(this),
        error: function (data) {
            console.error(data);
            this.posting = false;
            error_func();
        }.bind(this)
    });
};

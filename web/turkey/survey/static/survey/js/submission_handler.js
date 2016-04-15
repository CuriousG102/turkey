// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    },
    timeout: 10 * Math.pow(10, 3) // seconds
});

var NOT_READY_TO_SUBMIT = "whoops";

var Overlord = {
    steps: [],
    auditors: [],
    posting: false,

    register_step: function(name, callback) {
        this.steps.push([name, callback]);
    },

    register_auditor: function(name, callback) {
        this.auditors.push([name, callback]);
    },
    
    submit: function() {
        if (this.posting) {
            window.alert('Submission in progress, please wait.');
            return;
        }

        this.posting = true;
        var submission = {
            'auditors': {},
            'steps': {}
        };

        var error_func = function() {
            window.alert('Submission failed. Please try again.')
        };

        var unsuccessful = false;
        $.each(this.steps, function(i, el) {
            var name = el[0], callback = el[1];
            try {
                submission['steps'][name] = callback();
            } catch (err) {
                unsuccessful = true;
                if (err !== NOT_READY_TO_SUBMIT) ; // TODO
            }
        });

        if (unsuccessful) {
            this.posting = false;
            return;
        }

        $.each(this.auditors, function(i, el) {
            var name = el[0], callback = el[1];
            submission['auditors'][name] = callback();
        });

        $.post({
            url: SUBMISSION_ENDPOINT,
            contentType:"application/json; charset=utf-8",
            data: JSON.stringify(submission),
            success: function (data, txt, xhr) {
                this.posting = false;
                if (xhr.status !== 201) {
                    console.error(data);
                    console.error(xhr);
                    error_func();
                }
                window.alert("Success!");
                window.location.replace(NEXT_PAGE);
            }.bind(this),
            error: function (data) {
                console.error(data);
                this.posting = false;
                error_func();
            }.bind(this)
        })
    }
};

var overlord = Object.create(Overlord);

$(document).ready(function() {
    $('#submit').click(function() {
        overlord.submit();
    });
});

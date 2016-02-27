$.ajaxSetup({
    timeout: 10 * Math.pow(10, 3) // seconds
});

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
        var submission = {
            'auditors': {},
            'steps': {}
        };
        $.each(this.steps, function(i, el) {
            var name = el[0], callback = el[1];
            submission['steps'][name] = callback();
        });

        var error_func = function() {
            window.alert('Submission failed. Please try again.')
        };

        $.post({
            url: SUBMISSION_ENDPOINT,
            data: JSON.stringify(submission),
            dataType: 'json',
            success: function (data, txt, xhr) {
                this.posting = false;
                if (xhr.status !== 201) {
                    console.error(data);
                    console.error(xhr);
                    error_func();
                }
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
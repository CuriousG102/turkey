/**
 * Created by Miles on 9/30/16.
 */

var InteractionManager = function (fetch_interaction_endpoint, task_pk,
                                   token_name) {
    this.fetch_interaction_endpoint = fetch_interaction_endpoint;
    this.task_pk = task_pk;
    this.token_name = token_name;
    this.fetching = false;
    this.fetched = false;
    this.auditor_submission_endpoint = null;
    this.step_submission_endpoint = null;
    this.token = null;
};

// gets interaction if one is not already created
// and passes submission endpoints('auditor_submission_endpoint',
// 'step_submission_endpoint') and token value
// into callback
InteractionManager.prototype.get_interaction = function(callback) {
    if (this.fetching)
        return;
    // god forgive me
    var call_callback = function () {
        callback({
            'auditor_submission_endpoint': this.auditor_submission_endpoint,
            'step_submission_endpoint': this.step_submission_endpoint
        }, this.token);
    };
    if (this.fetched) {
        call_callback();
        return;
    }

    this.fetching = true;
    var post_data = {'task_pk': this.task_pk};
    var ec = new evercookie();

    // I dream of a day where literally everyone uses promises and
    // callbacks are no more than a distant memory. May our children never
    // know the horrors of callbacks.
    $(document).ready(function() {
        ec.get(this.token_name, function (token) {
            if (token) {
                post_data['token'] = token;
            }
            $.post({
                url: this.fetch_interaction_endpoint,
                contentType: "application/json; charset=ut-8",
                data: JSON.stringify(post_data),
                success: function (data, text, xhr) {
                    if (xhr.status !== 201) {
                        console.error(data);
                        console.error(xhr);
                        return;
                    }
                    this.token = data['token'];
                    this.auditor_submission_endpoint = data['auditor_submission_url'];
                    this.step_submission_endpoint = data['step_submission_url'];
                    this.fetching = false;
                    this.fetched = true;
                    call_callback();
                }.bind(this),
                error: function (data) {
                    console.error(data);
                    this.fetching = false;
                }.bind(this)
            });
        });
    });
};
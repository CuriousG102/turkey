/**
 * Created by Miles on 9/30/16.
 */

var InteractionManager = function (fetch_interaction_endpoint, task_pk,
                                   token_name) {
    this.fetch_interaction_endpoint = fetch_interaction_endpoint;
    this.task_pk = task_pk;
    this.token_name = token_name;
    this.request_promise = null;
};

// gets interaction if one is not already created
// and passes submission endpoints('auditor_submission_endpoint',
// 'step_submission_endpoint') and token value
// into callback
InteractionManager.prototype.get_interaction = function(callback) {
    var call_callback = function (data, text, xhr) {
        callback({
            'auditor_submission_endpoint': data['auditor_submission_url'],
            'step_submission_endpoint': data['step_submission_url']
        }, data['token']);
    }.bind(this);

    if (this.request_promise) {
        this.request_promise.done(call_callback);
        return;
    }

    var post_data = {'task_pk': this.task_pk};

    // I dream of a day where literally everyone uses promises and
    // callbacks are no more than a distant memory. May our children never
    // know the horrors of callbacks.
    var token = Cookies.get(this.token_name);
    if (token) {
        post_data['token'] = token;
    }
    this.request_promise = $.post({
        url: this.fetch_interaction_endpoint,
        contentType: "application/json; charset=ut-8",
        data: JSON.stringify(post_data),
    }).promise();
    this.request_promise
        .done(function (data, text, xhr) {
           if (xhr.status !== 201) {
                console.error(data);
                console.error(xhr);
                return;
            }
            Cookies.set(this.token_name, data['token']);
            call_callback(data, text, xhr);
        }.bind(this))
        .fail(function (data) { console.error(data); });
};
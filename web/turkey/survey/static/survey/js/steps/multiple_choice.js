var StepMultipleChoice = {
    submit_callable: function () {
        var step_mcs = {};
        var successful = true;

        $.each($('.step-mc'), function (el) {
            var name = el.attr('id');
            var name_split = name.split('-');
            var pk = Number(name_split[name_split.length-1]);
            var response = $('input[name='+name+']').filter(':checked').val();
            if (!response) {
                successful = false;
                // TODO: Error message added to DOM for user
            } else {
                var response_split = response.split('-');
                response = Number(response_split[response_split.length-1]);
                step_mcs[pk] = {'response': response};
            }
        });

        if (!successful) throw NOT_READY_TO_SUBMIT;

        return step_mcs;
    }
};

var step_multiple_choice = Object.create(StepMultipleChoice);
overlord.register_step('multiple_choice',
                       step_multiple_choice
                           .submit_callable
                           .bind(step_multiple_choice));
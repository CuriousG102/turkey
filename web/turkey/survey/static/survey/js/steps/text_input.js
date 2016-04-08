var StepTextInput = {
    submit_callable: function () {
        var step_tis = {};
        var successful = true;

        $('.step-ti').each(function () {
            var name = $(this).attr('id');
            var name_split = name.split('-');
            var pk = Number(name_split[name_split.length-1]);
            var response = $('textarea[name='+name+']').val();
            if (!response) {
                successful = false;
                // TODO: Error message added to DOM for user
            } else {
                var response_split = response.split('-');
                response = Number(response_split[response_split.length-1]);
                step_tis[pk] = {'response': response};
            }
        });

        if (!successful) throw NOT_READY_TO_SUBMIT;

        console.log(step_tis);
        return step_tis;
    }
};

var step_text_input = Object.create(StepTextInput);
overlord.register_step('text_input',
                       step_text_input
                           .submit_callable
                           .bind(step_text_input));
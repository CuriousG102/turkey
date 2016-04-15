var StepMultipleAnswers = {
    submit_callable: function () {
        var step_mas = {};
        var successful = true;

        $('.step-ma').each(function () {
            var name = $(this).attr('id');
            var name_split = name.split('-');
            var pk = Number(name_split[name_split.length-1]);
            var response = [];
            $('input[name='+name+']:checked').each(function() {
                response.push($(this).val());
            });
            if (response == []) {
                successful = false;
                // TODO: Error message added to DOM for user
            } else {
                // var response_split = response.split('-');
                // response = Number(response_split[response_split.length-1]);
                step_mas[pk] = {'response': response.toString()};
            }
        });

        if (!successful) throw NOT_READY_TO_SUBMIT;

        return step_mas;
    }
};

var step_multiple_answers = Object.create(StepMultipleAnswers);
overlord.register_step('multiple_answers',
                       step_multiple_answers
                           .submit_callable
                           .bind(step_multiple_answers));
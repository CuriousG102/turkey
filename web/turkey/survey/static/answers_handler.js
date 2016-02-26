// do all the crap to send incoming json on user generated events

// function to be called when submit button is pressed
var my_submit_function = function() {
var key = 'multiple_choice_text';
var value = {'stuff': 'stuff'}
	return [key, value];
};
god.register(my_submit_function);
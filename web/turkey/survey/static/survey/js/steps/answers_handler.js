// do all the crap to send incoming json on user generated events

// question answers
var rating = undefined, justification = '', feedback = '';

// function to be called when submit button is pressed
var my_submit_function;

$(document).ready(function() {	
	// Q1: radio button value
	$('input[type=radio]').change(function() {
		rating = $('input[name="relevancy"]:checked').val();
	}),

	// Q2: justification text in some textarea with id 'justification'
	$('#justification').change(function() {
		justification = $('#justification').val().trim();
	}),

	// Q3: feedback text in some textarea with id 'feedback'
	$('#feedback').change(function() {
		feedback = $('#feedback').val().trim();
	}),

	my_submit_function = function(rating, justification, feedback) {
		return {
			'name'	:	'multiple_choice_text';
			'value' :	{
							'rating'		:	rating,
							'justification'	:	justification,
							'feedback'		:	feedback
						}
		};
	};
}); 
// submit button with id 'submit'
$('#submit').click(function() {
	if(rating != undefined && justification != '') {
		Overlord.register(my_submit_function);
		Overlord.register(submit_auditor);
		Overlord.submit();
	}
});
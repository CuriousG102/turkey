var AuditorMouseMovementSpecific = {
    start_date: new Date(),
    mouse_movement_specific: [],
    log_mousemove_specific: function (e) {
        this.mouse_movement_specific.push(
            {
                'x' : e.pageX,
                'y' : e.pageY,
                'time': (new Date()).getTime() - this.start_date.getTime()
            }
        );
    },
    submit_callable: function () {
        return this.mouse_movement_specific;
    }
};

var auditor_mouse_movement_specific = Object.create(AuditorMouseMovementSpecific);

$(window).mousemove(
    $.debounce(250, function(e) {
        auditor_mouse_movement_specific
            .log_mousemove_specific
            .bind(auditor_mouse_movement_specific)(e);
    })
);

turkey.register_auditor('mouse_movement_specific',
                          auditor_mouse_movement_specific
                            .submit_callable
                            .bind(auditor_mouse_movement_specific));
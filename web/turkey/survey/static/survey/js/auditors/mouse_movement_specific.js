var AuditorMouseMovementSpecific = {
    mouse_movement_specific: [],
    log_mousemove_specific: function (e) {
        this.mouse_movement_specific.push(
            {
                'X' : e.pageX,
                'Y' : e.pageY
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
            .bind(auditor_mouse_movement_specific);
    });
);

overlord.register_auditor('mouse_movement_specific',
                          auditor_mouse_movement_specific
                            .submit_callable
                            .bind(auditor_mouse_movement_specific));
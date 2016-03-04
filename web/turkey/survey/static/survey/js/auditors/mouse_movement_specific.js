var AuditorMouseMovementSpecific = {
    mouse_movement_specific: [],
    previous_position: 0,
    log_mousemove_specific: function (e) {
            var position = [e.pageX, e.pageY];
            this.mouse_movement_specific.push(position);
        }
    },
    submit_callable: function () {
        return {
            'content':  this.mouse_movement_specific != null
                        ?
                        this.mouse_movement_specific
                        :
                        null
        };
    }
};

var auditor_mouse_movement_specific = Object.create(AuditorMouseMovementSpecific);

$(document).ready(function() {
    $(window).mousemove(auditor_mouse_movement_specific
                            .log_mousemove_specific
                            .bind(auditor_mouse_movement_specific));
});

overlord.register_auditor('mouse_movement_specific',
                          auditor_mouse_movement_specific
                            .submit_callable
                            .bind(auditor_mouse_movement_specific));
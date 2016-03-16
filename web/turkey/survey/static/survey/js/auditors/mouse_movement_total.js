var AuditorMouseMovementTotal = {
    mouse_movement_total: 0,
    setup: function {
        // https://github.com/cowboy/jquery-throttle-debounce
        (function(b,c){var $=b.jQuery||b.Cowboy||(b.Cowboy={}),a;$.throttle=a=function(e,f,j,i){var h,d=0;if(typeof f!=="boolean"){i=j;j=f;f=c}function g(){var o=this,m=+new Date()-d,n=arguments;function l(){d=+new Date();j.apply(o,n)}function k(){h=c}if(i&&!h){l()}h&&clearTimeout(h);if(i===c&&m>e){l()}else{if(f!==true){h=setTimeout(i?k:l,i===c?e-m:e)}}}if($.guid){g.guid=j.guid=j.guid||$.guid++}return g};$.debounce=function(d,e,f){return f===c?a(d,e,false):a(d,f,e!==false)}})(this);
    },
    log_mousemove_event: function (e) {
            this.mouse_movement_total += 1;
        }
    },
    submit_callable: function () {
        return {
            'amount': this.mouse_movement_total
        };
    }
};

var auditor_mouse_movement_total = Object.create(AuditorMouseMovementTotal);
auditor_mouse_movement_total.setup();

$(window).mousemove(
    $.debounce(250, function(e) { 
        auditor_mouse_movement_total
            .log_mousemove_event
            .bind(auditor_mouse_movement_total);
    });
);

overlord.register_auditor('mouse_movement_total',
                          auditor_mouse_movement_total
                            .submit_callable
                            .bind(auditor_mouse_movement_total));
var Overlord = {
    steps: [],
    submission: {}, // results
    
    // enqueue a function f
    register: function(f) {
        this.steps.push(f);
    },
    
    submit: function() {
        $.each(this.steps, function(index, value) {
            var result = value();
            this.submission[result.name] = result.value;
        }
    };

    // post submission map to endpoint
    }
}
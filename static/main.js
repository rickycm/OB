//$(function() { /// = Document is ready

window.Patient = Backbone.Model.extend();

window.PatientCollection = Backbone.Collection.extend({
	model: Patient,
	url: "/patients",
});

window.PatientListView = Backbone.View.extend({

	el: '#patientList',

	initialize: function() {
	    console.log("init");
		this.model.bind("reset", this.render, this);
        /*var self = this;
        this.model.bind("add", function (patient) {
            $(self.el).append(new PatientListItemView({model:patient}).render().el);
        });*/
	},

    render: function(eventName) {
		console.log('list');
		//$(this.el).clear();
		_.each(this.model.models, function(patient) {
            $(this.el).append(new PatientListItemView({model: patient}).render().el);
		}, this);
		return this;
    }
});

window.PatientListItemView = Backbone.View.extend({

	tagName: "li",

	template: _.template($('#patient-list-item').html()),

	/*initialize: function() {
	    this.model.bind("change", this.render, this);
        this.model.bind("destroy", this.close, this);
	},*/

    render: function(eventName) {
        console.log('render one');
		$(this.el).html(this.template(this.model.toJSON()));
		return this;
    },

    /*close:  function() {
        $(this.el).unbind();
        $(this.el).remove();
    }*/
});

/*window.PatientView = Backbone.View.extend({
    el: $('#mainArea'),
	template: _.template($('#patient-details').html()),
	initialize: funcfion(){
	    this.model.bind("change", this.render, this);
	},
    render: function(eventName) {
		$(this.el).html(this.template(this.model.toJSON()));
		return this;
    },
});*/

var AppRouter = Backbone.Router.extend({
	routes: {
		"": "list",
		"patients/:id"	: "patientDetails"
	},

	list: function() {
    	this.patientList = new PatientCollection();
    	this.patientListView = new PatientListView({model: this.patientList});
		this.patientList.fetch({reset:true});
  	},
});

var app = new AppRouter();
Backbone.history.start();
//});
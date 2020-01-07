var engine =  {

	modal_opened: false,
	components: [],
	listeners: [],

	component_register: function(component_id) {
		if (this.components.indexOf(component_id) === -1)
			this.components.push(component_id);
		else {
			if(typeof window[component_id] == 'object' && typeof window[component_id].init == 'function') {
				window[component_id].init();
			}
		}
	},

	components_init: function() {
		this.components.forEach(function(component) {
			if(typeof window[component] == 'object' && typeof window[component].init == 'function'){
				window[component].init();
				engine.subscribe_auto(window[component]);
			}
		});
	},

	subscribe: function(event_name, context) {

		if(typeof(context[event_name]) !== 'function'){
			return;
		}

		if(typeof(this.listeners[event_name]) == 'undefined')
			this.listeners[event_name] = [];

		this.listeners[event_name].push({
			context: context,
			callback: context[event_name]
		})
	},

	unsubscribe: function(event_name, context) {
		if(typeof(context[event_name]) == 'undefined') {
			return;
		}

		delete(this.listeners[event_name]);
	},

	subscribe_auto: function(context){
        var key;
        for (key in context){
            if (!context.hasOwnProperty(key))
                continue;
            if (typeof(context[key]) != 'function')
                continue;
            if (key.substring(0, 3) !== "em_")
                continue;
            this.subscribe(key, context);
        }
    },

    unsubscribe_auto: function(context){
        var key;
        for (key in context){
            if (!context.hasOwnProperty(key))
                continue;
            if (typeof(context[key]) != 'function')
                continue;
            if (key.substring(0, 3) !== "em_")
                continue;
            this.unsubscribe(key, context);
        }
    },

	dispatch: function(event_name, data) {
		if(typeof(this.listeners[event_name]) == 'undefined') {
			return;
		}
		data = (typeof(data) == 'undefined') ? null : data;
		
		var listeners = this.listeners[event_name];

        for (var f = 0; f < listeners.length; f++)
            listeners[f].callback.apply(listeners[f].context, [data]);
	},


	em_html_append: function(data) {
		$(data.element).append(data.html);
	},

	em_html_replace: function(data) {
		var elem = $(data.element);
		elem.replaceWith(data.html);
	},

	em_modal_open: function(data) {
		$('body').append(data.html);
		var dialog = $('#' + data.id);
		dialog.modal('show');
		this.modal_opened = true;
	},

	em_modal_close: function(modal_id) {
		$('#' + modal_id).modal('hide');
		this.modal_opened = false;
	},

	em_redirect: function(url){
        var a, b;
        window.location = url;
        a = document.createElement('a');
        a.href = url;
        //ie9 bugfix
        b = a.pathname;
        if ((url[0] == '/') && (b[0] != '/'))
            b = '/' + b;
        if ((b == window.location.pathname) && (a.hash !== ''))
            window.location.reload();
    },

	em_form_invalidate: function(data) {
		var errors, field, error_field;
		var form = $("#"+data.prefix);
		var errors_fields = form.find('.form__error');
		errors_fields.remove();
		errors = JSON.parse(data.errors);
		console.log(errors);
		for (var error in errors) {
			field = form.find("#id_" + data.prefix + '-' + error);
			error_field = document.createElement('span');
			error_field.className = 'form__error';
			error_field.innerText = errors[error][0]['message'];
			$(error_field).insertAfter(field);
		}
	},

	getCookie: function getCookie(name) {
  		var matches = document.cookie.match(new RegExp(
    		"(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  		));
  		return matches ? decodeURIComponent(matches[1]) : undefined;
	},

	request: function(url, data, animate) {
		if (!data) {
			data = {};
		}
 		
 		var csrftoken = this.getCookie('csrftoken');
		data.csrfmiddlewaretoken = csrftoken;

		if (animate) {
			this.preloader.show();
		}

		 $.ajax({
            url: url,
            type: 'POST',
            dataType: 'json',
            data: data,
            error: this._ajax_request_err,
            success: this._ajax_request_ok
        });
	},

	preloader: {
		show: function () {
			console.log('preloader show');
		},

		hide: function() {
			console.log('preloader hide');
		}
	},
	
	_ajax_request_ok: function(data) {
		console.log(data);
		if (data.events !== undefined) {
			for (var i=0; i < data.events.length; i++) {
				engine.dispatch(data.events[i].event_id, data.events[i].data)
			}
		}
	},

	_ajax_request_err: function(data) {
		flash_message.addMessage('alert', "JSON request error");
	},


	init: function() {
		this.components_init();
		this.subscribe_auto(engine);
		this.subscribe_auto(flash_message);
		
		$(document).ajaxStop(this.preloader.hide());

		$(document).on('click', '.engine-ajax-request', function(e) {
			var url, data;

			url = $(this).attr('href');
			data = $(this).data();
			
			engine.request(url, data, data.animate);
		});

		$(document).off('click', '.engine-form-submit').on('click', '.engine-form-submit', function (e) {
			var form = e.target.parentElement;
			$(form).off('submit').on('submit', function (e) {
				var form = $(this);
				engine.request(form.attr('action'), form.serialize());
				e.preventDefault();
			});
		})
	}
};

$(document).on('ready', function() {
	engine.init();
});
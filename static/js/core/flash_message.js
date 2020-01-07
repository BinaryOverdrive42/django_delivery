var flash_message = {
	em_message: function(data) {
		this.addMessage(data.type, data.text)
	},

	addMessage: function(type, text) {
		var messages = document.getElementById('flash-messages');
		
		if (messages === null) {
			messages = document.createElement('div');
			messages.className = 'flash-messages';
			messages.id = 'flash-messages';
			document.body.appendChild(messages);
		}

		var message = document.createElement('div');
		message.className = 'f_message';
		message.innerHTML = text;
		message.addEventListener('click', this._removeMessage);

		if (type === 'info') {
			message.classList.add('f_message_info');
		} else if (type === 'alert') {
			message.classList.add('f_message_alert');
		}

		messages.appendChild(message);

		setTimeout(function() {
			if (messages.contains(message))
				messages.removeChild(message);
		}, 4000);
	},

	_removeMessage: function(e) {
		var messages = document.getElementById('flash-messages');
		messages.removeChild(e.target);
	}
}
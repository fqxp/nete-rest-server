(function($) {
	NeteDocument = function(data, nete_api) {
		for (var key in data) {
			this[key] = data[key];
		}
		this._api = nete_api;
	}

	// This makes NeteDocument act like an associative array
	NeteDocument.prototype = Object();
	
	NeteDocument.prototype.api = function() {
		return self._api;
	}
	
	NeteDocument.prototype.toString = function() {
		return "String: " + this;
	}
})(jQuery);

(function($) {
	NeteAPI = function() {
		this.base_url = '/api/';
	}

	/* NeteAPI class **********************************************************/
	
	NeteAPI.prototype.load = function(nete_id, callback, include_children) {
		var obj = this;
		var url = this.base_url + nete_id;
		var include_children = include_children || false;
		$.ajax({url: url,
			    data: {'include-children': include_children},
			    dataType: 'json',
			    success: function(data) {
			    	if (callback) {
			    		var doc = new NeteDocument(data, obj);
			    		callback(data);
			    	}
			    }
		});
	};
	
	NeteAPI.prototype.store = function(doc) {
		$.ajax({type: 'PUT',
				url: this.base_url + doc.data['_id'],
				data: doc.data,
				dataType: 'json',
				success: function(data) {
					alert('just stored');
				}});
	};
	
	NeteAPI.prototype.list = function(nete_id, callback) {
		if (nete_id) {
			nete_id = nete_id + '/';
		} else {
			nete_id = '';
		}
		$.ajax({type: 'GET',
			    url: this.base_url + nete_id + '_list',
			    dataType: 'json',	
			    success: function(data) {
			    	callback(data);
			    }});
	}
})(jQuery);

(function($) {
	var methods = {
		init: function(options) {
			    return $(this).each(function() {
					var $this = $(this);
					$this.data('nete_api', options.nete_api);
					$this.Page('load', options.page_id);
			    });
		},
		update: function() {
			var $this = $(this);
			var nete_api = $this.data('nete_api');
			var page_id = $this.data('page_id');
			nete_api.load(page_id, function(page_doc) {
				$this.empty()
					 .attr('data-nete-id', page_doc.id)
					 .addClass('nete-' + page_doc.type);
				for (var i in page_doc.children) {
					var child = page_doc.children[i];
					$this.append('<div class="nete-document nete-' + child.type + '" '
							   + 'data-nete-id="' + child.id + '">' 
							   + child.text
							   + '</div>');
				}
			},
			true); // include_children
		},
		load: function(nete_id) {
			this.data('page_id', nete_id);
			this.Page('update');
		}
	}
	
	$.fn.Page = function(method) {
	    if (methods[method]) {
	      return methods[method].apply(this, 
	    		  Array.prototype.slice.call(arguments, 1));
		} else if (typeof method === 'object' || !method) {
			return methods.init.apply(this, arguments);
		} else {
			$.error('Method ' + method + ' does not exist on jQuery.Page');
		}    
	}
})(jQuery);

(function($) {
	var methods = {
		init: function(options) {
				var obj = this;
				obj.data('current_page_id', options.current_page_id || null);
				obj.data('nete_api', options.nete_api);
				obj.data('page', options.page);
				obj.PageIndex('update');
			  },
	    /** Update this widget by reloading the page list.
	     */
		update: function() {
			var obj = this;
			var nete_api = obj.data('nete_api');
			nete_api.list('', function(data) {
								obj.empty()
								   .addClass('nete-page-bar');
								obj.append('<ul></ul>');
								for (var i in data) {
									var page_doc = data[i];
									var el = $('<li>' + page_doc.name + '</li>');
									if (page_doc.id == obj.data('current_page_id')) {
										el.addClass('current-selection');
									}
									el.click({page_id: page_doc.id}, function(ev) {
										obj.data('current_page_id', ev.data.page_id);
										obj.PageIndex('update');
										obj.data('page').Page('load', ev.data.page_id);
									})
									$('ul', obj).append(el);
								}
							});
		},
	}

	$.fn.PageIndex = function(method) {
	    if (methods[method]) {
	      return methods[method].apply(this, 
	    		  Array.prototype.slice.call(arguments, 1));
		} else if (typeof method === 'object' || !method) {
			return methods.init.apply(this, arguments);
		} else {
			$.error('Method ' + method + ' does not exist on jQuery.PageIndex');
		}    
	}
})(jQuery);
/*
This file is part of nete.

Copyright (C) 2011  Frank Ploss

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/

(function($) {
	$.fn.extend({
		// Calls the handler function if the user has clicked outside the object (and not on any of the exceptions)
		clickOutside: function(handler) {
			var $this = this;
			$('body').click(function(ev) {
				if ($.contains($this[0], ev.target)) {
					ev.stopPropagation();
				} else {
					handler(ev);
				}
			})
			return this;
		}
	});
/*	$("body").bind("click", function(event) {
		if (exceptions && $.inArray(event.target, exceptions) > -1) {
			return;
		} else if ($.contains($this[0], event.target)) {
			return;
		} else {
			handler(event, $this);
		}
	});
	*/
	var noteTemplate = _.template('<div id="<%= id %>"><%= text %> (<%= id %>)</div> ');
	var noteEditTemplate = _.template('<div id="<%= id %>"><textarea>value="<%= text %>"</textarea></div> ');
	
	NoteView = Backbone.View.extend({
		className: 'note',
		initialize: function() {
			this.editMode = false;
			this.model.bind('change', function(ev) {
				// leave this here for the live update later on!
				// this is cool!
				console.log('noteview: got change event');
				this.render();
			}, this);
			this.render();
		},
		render: function() {
			console.log('render: editmode=' + this.editMode);
			if (this.editMode) {
				$(this.el)
					.html(noteEditTemplate({text: this.model.get('text'),
											'id': this.model.get('id')}))
					.addClass('nete-editing')
					.click(function(ev) {
						ev.stopPropagation();
					});
				$('body').one("click", function(ev) {
					console.log('clicked outside of editor');
				});
			} else {
				$(this.el).html(noteTemplate({text: this.model.get('text'),
					'id': this.model.get('id')})).
					removeClass('nete-editing');
			}
		},
		events: {
			'click': 'edit'
		},
		edit: function(ev) {
			console.log('noteview going into edit mode')
			this.editMode = true;
			this.model.fetch();  // just to minimize chance of editing a stale doc
			this.render();
		}
	});

	NoteCollectionView = Backbone.View.extend({
	    className: 'note-collection',
	    initialize: function() {
	        this.collection.bind('reset', function(ev) {
	        	this.render();
	        }, this);
	    },
	    render: function() {
	    	$(this.el).empty();
	        for (var i in this.collection.models) {
	            var model = this.collection.models[i];
	            var modelView = new NoteView({model: model});
	            $(this.el).append(modelView.el);
	        }
	        return this;
	    }
	});
}(jQuery));
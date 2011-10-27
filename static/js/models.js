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

// Override the sync method to support JSONP
(function($) {
	Backbone.sync = function(method, model, options) {
		console.log('sync method: ' + method);
		var params = _.extend({
			dataType: 'jsonp',
			url: model.url(),
			jsonp: "_callback",
			processData: false
		}, options);
		if (method == 'read') {
			params.type = 'GET';
		} else if (method == "create") {
			params.type = 'POST';
		}
		return jQuery.ajax(params);
	}
	
	Page = Backbone.Model.extend({
		'id': null,
		rev: null,
		parent_id: null,
		name: null,
		url: function() { return 'http://localhost:8888/rest/' + this.id; }
	});
	
	Note = Backbone.Model.extend({
		'id': null,
		rev: null,
		type: null,
		parent_id: null,
		url: function() { return 'http://localhost:8888/rest/' + this.id; }
	});
	
	PageCollection = Backbone.Collection.extend({
		model: Page,
		url: function() {
			return 'http://localhost:8888/rest/' + this.id + '/_children?type=page';
		}
	});
	
	NoteCollection = Backbone.Collection.extend({
		model: Note,
		url: function() {
			return 'http://localhost:8888/rest/' + this.id + '/_children?type=note';
		}
	});
}(jQuery));
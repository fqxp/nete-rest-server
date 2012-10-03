window.App = Ember.Application.create({
  ready: function(){
  }
});

// models
window.App.Note = Ember.Object.extend({
  text: null,
  author: null,
});

// views
window.App.NoteView = Ember.View.extend({
  templateName: "note",
  click: function() {
    console.log(this);
  }
});

window.App.NoteEdit = Ember.TextArea.extend({
});

window.App.pageView = Ember.CollectionView.create({
  content: [],
  itemViewClass: window.App.NoteView
});
window.App.pageView.appendTo('body');

// controllers
window.App.notesController = Ember.ArrayController.create({
  content: [],
  loadNotes: function(){
    var self = this;

    jQuery.ajax('http://localhost:8888/notes', {
        success: function(data, textStatus) {
            data.forEach(function(item){
              self.pushObject(window.App.Note.create(item));
            });
        }
    });
  }
});


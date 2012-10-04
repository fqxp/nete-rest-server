window.App = Ember.Application.create({
  ready: function(){
    window.App.notesController.loadNotes();
  }
});

// models
window.App.Note = Ember.Object.extend({
  id: null,
  text: null,
  author: null,
});

// views
window.App.NoteView = Ember.View.extend({
  templateName: "note",
  click: function() {}
});

window.App.NoteEditView = Ember.View.extend({
  templateName: "note-edit",

  createNote: function() {
    var text = this.get("text");
    window.App.notesController.createNote(text);
  }
});

window.App.pageView = Ember.CollectionView.create({
  content: [],
  itemViewClass: window.App.NoteView
});

function generate_uuid()
{
  var S4 = function()
  {
    return Math.floor(
      Math.random() * 0x10000 /* 65536 */
    ).toString(16);
  };

  return (
    S4() + S4() + "-" +
    S4() + "-" +
    S4() + "-" +
    S4() + "-" +
    S4() + S4() + S4()
  );
}

// controllers
window.App.notesController = Ember.ArrayController.create({
  content: [],

  newNote: function() {
    var noteEditor = window.App.NoteEditView.create();
    noteEditor.appendTo('body');
  },

  loadNotes: function(){
    var self = this;

    jQuery.ajax('http://localhost:8888/notes', {
      success: function(data, textStatus) {
        self.clear();
        data.forEach(function(item){
          self.pushObject(window.App.Note.create(item));
        });
      }
    });
  },

  createNote: function(text) {
    var id = generate_uuid();
    var note = window.App.Note.create({
      id: generate_uuid(),
      text: text
    });

    var data = {
      text: note.text
    };
    jQuery.ajax('http://localhost:8888/notes/' + id,
        {
          type: 'put',
          dataType: 'json',
          data: JSON.stringify(data)
        });
    this.pushObject(note);
  }
});


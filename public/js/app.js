window.App = Ember.Application.create();

Note = Ember.Object.extend({
  text: "This is the note text!!! It's great!"
});

var note_1 = Note.create();
var note_1 = Note.create();
var note_2 = Note.create();

var noteView = Ember.View.create({
  templateName: 'note',
  classNames: ['note'],
  note: note_1
});

$(function() {
  noteView.appendTo('body');
});

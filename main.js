var RefSpeaker = require('refspeaker');
var EventEmitter = require('events').EventEmitter;
var emitter = new EventEmitter();

var ref = new RefSpeaker();

var keypress = require('keypress');

// make `process.stdin` begin emitting "keypress" events
keypress(process.stdin);

// listen for the "keypress" event
process.stdin.on('keypress', function (ch, key) {

  console.log('got "keypress"', key);

  if (key.name === 'p') {
    ref.action('play');
  }
  if (key.name === 'space') {
    ref.action('pause');
  }
  if (key && key.ctrl && key.name == 'c') {
    process.stdin.pause();
  }
});

process.stdin.setRawMode(true);
process.stdin.resume();
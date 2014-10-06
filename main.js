var RefSpeaker = require('./refspeaker');
var EventEmitter = require('events').EventEmitter;
var emitter = new EventEmitter();

var ref = new RefSpeaker();

//var keypress = require('keypress');

// make `process.stdin` begin emitting "keypress" events
/*keypress(process.stdin);

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
*/
// PYTHON-SHELL
//

var PythonShell = require('python-shell');

var options = {
  scriptPath: './'
};

var pyshell_hello = new PythonShell('./hello.py', options);

pyshell_hello.on('message', function (message) {
  // received a message sent from the Python script (a simple "print" statement)
  console.log(message);
});


var pyshell_volume = new PythonShell('./encoder-volume.py', options);

pyshell_volume.on('message', function (message) {
  // received a message sent from the Python script (a simple "print" statement)
  console.log(message);
});

// end the input stream and allow the process to exit
/*pyshell.end(function (err) {
  if (err) throw err;
  console.log('finished, bye from Python!');
});*/
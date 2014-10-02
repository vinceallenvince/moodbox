var request = require('request');

function RefSpeaker() {

}

RefSpeaker.prototype.action = function(action) {
  request('http://localhost:15004/action?action=' + action, function (error, response, body) {
    if (!error && response.statusCode == 200) {
      console.log(body)
    }
  });
};

module.exports = RefSpeaker;
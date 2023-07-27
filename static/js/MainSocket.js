// var ws_url = `ws://${window.location.hostname}:${window.location.port}${window.location.pathname}ws/`;
var ws_url = `ws://${window.location.hostname}:${window.location.port}/messenger/ws/`;
// socket = new WebSocket(`ws://192.168.1.18:10000/messenger/ws/`);
socket = new WebSocket(ws_url)

var Initials = {
  socket  : socket,
  activeUserName : userName(),
  workSpaceName : getWorkSpaceName(),
  };

function sample_load() {
    const abcd = "hello world"
    return abcd
  }
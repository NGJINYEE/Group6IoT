// alert('Connected!');
console.log('Connected!');

$('#change').click(function(){
  console.log('Clicked!');
  testData = {data: 'Hello from js!'};
  $.ajax({
    type: "POST",
    url: "/load_color",
    data: testData,
    dataType: 'json',
    contentType: 'application/json',
    success: function(data) {
      // console.log(data.hex);
      const color = '#' + data.hex;
      const matchedColor = '#000000'
      // console.log(color);
      $('.your-color').css({backgroundColor: color});
      $('.closest-color').css({backgroundColor: matchedColor});
    }
  });
});


// $(document).ready(function(){
//   var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
//   socket.on('my response', function(msg){
//     $('#log').append('<p> Received: ' + msg + data + '</p>');
//   });
//
//   $('form#emit').submit(function(event){
//     socket.emit('my event', {data: $('#emit_data').val()});
//     return false;
//   });
// });

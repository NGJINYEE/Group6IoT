console.log('Connected!');

//Use jQuery to post request from the server to obtain colour data
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
      //when successfully received data from the server, decode it into two variables
      const oriColor = '#' + data.oriHex;
      const closestColor = '#' + data.closestHex;
      //change the class your-color class and closest-color
      $('.your-color').css({backgroundColor: oriColor});
      $('.closest-color').css({backgroundColor: closestColor});
    }
  });
});


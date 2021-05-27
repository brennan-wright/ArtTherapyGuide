window.onload = function () {
  if (typeof (django) !== 'undefined' && typeof (django.jQuery) !== 'undefined') {
      (function ($) {
        // this loads the code on the window load.
          
$("#id_region").change(function () {
    var url = "/education/ajax/load-cities/";  // get the url of the `load_cities` view
    console.log(url)
    var regionId = $(this).val();  // get the selected country ID from the HTML input
    console.log(regionId)
    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
        'region': regionId       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
        $("#id_city").html(data);  // replace the contents of the city input with the data that came from the server
        }
    });

    // this loads the code at window load.
    });    }(django.jQuery));
  }
};
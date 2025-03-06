function getBathValue() {
    var uiBathrooms = document.getElementsByName("uiBathrooms");
    for(var i in uiBathrooms) {
      if(uiBathrooms[i].checked) {
          return parseInt(i)+1;
      }
    }
    return -1; // Invalid Value
  }
  
  function getBHKValue() {
    var uiBHK = document.getElementsByName("uiBHK");
    for(var i in uiBHK) {
      if(uiBHK[i].checked) {
          return parseInt(i)+1;
      }
    }
    return -1; // Invalid Value
  }
  
  function onClickedEstimatePrice() {
    console.log("Estimate price button clicked");

    var sqft = document.getElementById("uiSqft");
    var bhk = getBHKValue();
    var bathrooms = getBathValue();
    var location = document.getElementById("uiLocations");
    var estPrice = document.getElementById("uiEstimatedPrice");

    var url = "http://127.0.0.1:5000/predict_home_price"; // Update to match your server endpoint

    // Log inputs to ensure they are captured correctly
    console.log("Input values:", {
        total_sqft: parseFloat(sqft.value),
        bhk: bhk,
        bath: bathrooms,
        location: location.value
    });

    $.post(url, {
        total_sqft: parseFloat(sqft.value),
        bhk: bhk,
        bath: bathrooms,
        location: location.value
    }, function(data, status) {
        console.log("Response received:", data);
        if (data.estimated_price) {
            estPrice.innerHTML = `<h2>${data.estimated_price.toString()} Lakh</h2>`;
        } else {
            estPrice.innerHTML = `<h2>Error: ${data.error || "Unexpected response"}</h2>`;
        }
    }).fail(function(error) {
        console.error("Error in API call:", error);
        estPrice.innerHTML = `<h2>Error connecting to the server</h2>`;
    });
}

  
  function onPageLoad() {
    console.log("document loaded");
    var url = "http://127.0.0.1:5000/get_location_names"; // Update to match your API setup
    $.get(url, function (data, status) {
        console.log("Got response for get_location_names request");
        if (data && data.locations) {
            var locations = data.locations;
            var uiLocations = document.getElementById("uiLocations");
            $('#uiLocations').empty(); // Clear existing options
            $('#uiLocations').append(new Option("Choose a Location", "", true, true)); // Default option

            // Add locations to the dropdown
            for (var i = 0; i < locations.length; i++) {
                $('#uiLocations').append(new Option(locations[i], locations[i]));
            }
        } else {
            console.error("No locations found in the response");
        }
    }).fail(function () {
        console.error("Failed to fetch location names from API");
    });
}
  
  window.onload = onPageLoad;
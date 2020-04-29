// Stores the marker data from the API call
var markerData;

/**
 * Stores the Marker Map data into the markerData global variable
 * @param jsonData JSON formatted data from the backend API call
 */
function setMarkerData(jsonData) {
    markerData = jsonData;
}

/**
 * Fills in an HTML formatted string containing all the marker data with styling
 * @param markerData Object containing data for a marker
 * @returns {string} HTML formatted string
 */
function createInfoBoxText(markerData) {
    // assign the text color based on the sentiment score
    var sentimentScoreColor;
    if (markerData.sentiment_score > 1) {
        sentimentScoreColor = '"color:green;"';
    } else if (markerData.sentiment_score < -1) {
        sentimentScoreColor = '"color:red;"';
    } else {
        sentimentScoreColor = '"color:gold;"';
    }

    return '<div class="flex-container">' + '<div><img src="https://cfcdnpull-creativefreedoml.netdna-ssl.com/wp-content/uploads/2017/06/Twitter-featured.png" height="16.25" width="20"></div>' +
        '<div><h3>' + markerData.user_name + '</h3></div></div><div><p>' +  markerData.text +
    '</p><p><b>Sentiment:</b><span style=' + sentimentScoreColor + '> ' + markerData.sentiment_score + '</span></p><p><b>' + markerData.retweet_count +
    '</b> Retweets<b>&nbsp;&nbsp;&nbsp;' + markerData.favorite_count +
    '</b> Likes</p><p>' +  markerData.date + '</p></div>';
}

/**
 * Initializes the Google Map API with tweet markers
 */
function initMap() {
    // location of the White House
    var whiteHouse = {lat: 38.8976763, lng: -77.0387185};

    // initialize the map and center it on the White House
    var map = new google.maps.Map(
    document.getElementById('map'), {zoom: 6, center: whiteHouse});

    // Info Window object added to each marker
    var infowindow = new google.maps.InfoWindow();

    // create a marker for each record returned from the API call
    var i;
    for (i = 0; i < markerData.length; i++) {
      var markerSettings = {position: {lat: markerData[i].location[0], lng: markerData[i].location[1]}, map: map};

      // changing the marker icon to a blue marker if the tweet refers to joe biden
      // otherwise change the marker icon to a red marker for donald trump
      if (markerData[i].candidate == 'joe biden') {
          markerSettings.icon = {url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'};
      } else {
          markerSettings.icon = {url: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'};
      }

      var marker = new google.maps.Marker(markerSettings);
      google.maps.event.addListener(marker, 'click', (function (marker, i) {
          return function () {
              infowindow.setContent(createInfoBoxText(markerData[i]));
              infowindow.open(map, marker);
          }
      })(marker, i));
    }
}

#ALL CREDIT GOES TO MEGHANA

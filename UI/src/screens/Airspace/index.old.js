import React, { useEffect } from "react";
// import mapboxgl from "mapbox-gl";
import ContextualAirspacePlugin from "../../js-contextual-airspace-plugin/src/index";
// import "mapbox";
// import "leaflet";
import arc from "./stuff/arc";
// import largeAirports from "../data/large_airports_only.csv";
import "./stuff/mapbox.js";
import "./stuff/jquery.min.js";
// import "./stuff/ajax.js";
// import "ajax/lib/ajax.js";
import "./stuff/arc.js";
// import "jquery/src/jquery.js";
// import "mapbox/dist/mapbox-sdk.min.js";
import L from "leaflet";

function Airspace() {
  // var L = window.L;
  L.mapbox.accessToken = "";
  useEffect(() => {
    // let L = window.L;
    const AIRMAP_API_KEY =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVkZW50aWFsX2lkIjoiY3JlZGVudGlhbHw0Z242Z0tNaW5KODQza2h6NjRFZGJpT1pBS25hIiwiYXBwbGljYXRpb25faWQiOiJhcHBsaWNhdGlvbnxRTHk0NVIySDhKV3YzZ2lOUUdtM1poRHYwQTRxIiwib3JnYW5pemF0aW9uX2lkIjoiZGV2ZWxvcGVyfDc5NVlrQm1Db3hSQm53aTluOURiTEh3OTVLMFEiLCJpYXQiOjE1MjcxNTA4MDJ9.TkESuJIEQ9pjfU9F4TgIUNCF15OO2eeWU1GRONXf33Q";
    const MAPBOX_ACCESS_TOKEN =
      "pk.eyJ1IjoiZ2VvZmZyZXlueWFnYSIsImEiOiJjamdmM3Q5NG4wdnprMnhyMGJqd3U1N25yIn0.R_3l_E-DDVpHQ0rL3zgElQ";

    // Create an instance of the map

    // const map = new mapboxgl.Map({
    //   container: "mapid1",
    //   style: "mapbox://styles/mapbox/streets-v8",
    //   center: [37.496475, 0.024212],
    //   zoom: 8,
    //   accessToken: MAPBOX_ACCESS_TOKEN,
    // });

    //

    const mapboxAccessToken = MAPBOX_ACCESS_TOKEN;

    L.mapbox.accessToken = MAPBOX_ACCESS_TOKEN;

    var map = L.mapbox
      .map("mapid1", "mapbox.streets", {
        // set that bounding box as maxBounds to restrict moving the map
        // see full maxBounds documentation:
        // http://leafletjs.com/reference.html#map-maxbounds
        //maxBounds: [[ -4.77369399748329, 33.909937402767],
        //    [5.03342194387382, 41.9067738648657 ]],
        //maxZoom: 19,
        minZoom: 8,
      })
      .setView([-1.03326, 37.06933], 14);

    L.control.fullscreen().addTo(map);

    map.locate();

    async function getCountry(lat, long, mapboxToken) {
      x = await fetch(
        `https://api.mapbox.com/geocoding/v5/mapbox.places/${long},${lat}.json?access_token=${mapboxToken}`
      )
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          // console.log(data, "data");
          return data;
        });

      return x;
    }

    map.on("locationfound", function (e) {
      getCountry(e.latlng.lat, e.latlng.lng, mapboxAccessToken).then((data) => {
        console.log(data, "step 1");
        const features = data["features"];
        console.log(features, "step 2");

        features.forEach((feature) => {
          //if feature["id"].includes('country')
          if (feature["place_type"][0] == "country") {
            console.log(feature["place_type"][0], "step 3");
            console.log(feature["properties"], "step 3.5");

            const bbox = feature["bbox"];
            console.log(bbox, "step 3.7");

            const bound_sw = L.latLng(bbox[1], bbox[0]);
            console.log(bound_sw, "step 3.7");

            const bound_ne = L.latLng(bbox[3], bbox[2]);
            console.log(bound_ne, "step 3.7");

            console.log([bound_sw, bound_ne], "[bound_sw, bound_ne]");
            const bounds = [[bound_sw, bound_ne]];
            //let bounds = L.latLngBounds(bound_sw, bound_ne);
            console.log(bounds, "bounds");

            localStorage.setItem("bounds", JSON.stringify(bounds));
            if (localStorage.getItem("setCountryBounds") == null) {
              localStorage.setItem("setCountryBounds", false);
            }
          }
        });
      });

      console.log(e.bounds, "on location found");
      map.fitBounds(e.bounds);

      console.log("after the fact");

      map.setZoom(12);

      var myLayer = L.mapbox.featureLayer().addTo(map);
      myLayer.setGeoJSON({
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: [e.latlng.lng, e.latlng.lat],
        },
        properties: {
          title: "You Are Here!",
          "marker-color": "#ff8888",
          "marker-symbol": "star",
        },
      });
    });

    map.on("locationerror", function () {
      alert("Position could not be found");
      if (localStorage.getItem("bounds") == null) {
        map.setMaxBounds([
          [-4.77369399748329, 33.909937402767],
          [5.03342194387382, 41.9067738648657],
        ]);
      }
    });

    //TO DO: URGENT SET TO COUNTRY
    //DONE:
    map.on("zoomstart", function (e) {
      // because localstorage returns null if not found
      console.log("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX");

      if (
        localStorage.getItem("bounds") !== null &&
        localStorage.getItem("setCountryBounds") == "false"
      ) {
        //console.log(localStorage.getItem("bounds"),"its here")
        //console.log(typeof JSON.parse(localStorage.getItem("bounds")),"its here")
        console.log("setting the bounds");
        map.setMaxBounds(JSON.parse(localStorage.getItem("bounds")));
        localStorage.setItem("setCountryBounds", true);
      }
    });

    // ---------- AIRMAP AIRSPACES LOAD --------------------------//
    var url = "https://api.airmap.com/maps/v4/tiles";

    //https://developers.airmap.com/v2.0/docs/add-airspace-layers-to-the-map
    var layers = [
      "airports_commercial",
      "airports_recreational_private",
      "airports_commercial_private",
      "class_b",
      "class_c",
      "class_d",
      "class_e0",
      "sua_prohibited",
      "sua_restricted",
      "national_parks",
      "noaa",
      "hospitals",
      "schools",
      "heliports",
      "power_plants",
      "tfrs",
      "wildfires",
    ];

    var layerString = layers.toString().split(",");

    console.log(layerString, "layerstring");

    function getStyle(layer) {
      var style = {};
      switch (layer) {
        case "airports_recreational":
        case "airports_recreational_private":
        case "airports_commercial":
        case "airports_commercial_private":
        case "hospitals":
        case "heliports":
        case "power_plants":
        case "schools":
          style.color = "rgba(246, 165, 23, 0.2)";
          style.outline = {
            color: "rgb(246, 165, 23)",
            size: 0,
          };
          break;
        case "national_parks":
        case "noaa":
          style.color = "rgba(224, 18, 18, 0.2)";
          style.outline = {
            color: "rgb(224, 18, 18)",
            size: 0,
          };
          break;
        case "sua_restricted":
        case "sua_prohibited":
          style.color = "rgba(27, 90, 207, 0.2)";
          style.outline = {
            color: "rgb(27, 90, 207)",
            size: 0,
          };
          break;
        case "class_b":
          style.color = "rgba(26, 116, 179, 0.2)";
          style.outline = {
            color: "rgb(26, 116, 179)",
            size: 0,
          };
          break;
        case "class_c":
          style.color = "rgba(155, 108, 157, 0.3)";
          style.outline = {
            color: "rgb(155, 108, 157)",
            size: 0,
          };
          break;
        case "class_d":
          style.color = "rgba(26, 116, 179, 0.2)";
          style.outline = {
            color: "rgb(26, 116, 179)",
            size: 0,
          };
          break;
        case "class_e0":
          style.color = "rgba(155, 108, 157, 0.2)";
          style.outline = {
            color: "rgb(155, 108, 157)",
            size: 0,
          };
          break;
      }

      return style;
    }

    var mvtSource = new L.TileLayer.MVTSource({
      url:
        url + "/" + layerString + `/{z}/{x}/{y}.pbf?apikey=${AIRMAP_API_KEY}`,
      clickableLayers: [...layers],
      mutexToggle: true,
      getIDForLayerFeature: function (feature) {
        //console.log(feature.properties.name,"feature.properties")
        return feature.properties.name;
      },
      onClick: function (e) {
        // https://github.com/SpatialServer/Leaflet.MapboxVectorTile/issues/53
        console.log(e, "click");
        // console.log([...layers],'layers');

        var feature = e.feature;
        console.log(feature, "feature");
        console.log(feature !== null, " feature !== null should be true ");

        let coord = e.latlng;
        console.log(coord, "coord ");

        if (feature !== undefined && feature !== null) {
          var prop = feature.properties;
          var popup = L.popup({ closeOnClick: true })
            .setLatLng(coord)
            .setContent(prop.name)
            .openOn(feature.map);
        }
      },

      style: function (feature) {
        var layer = feature.properties.type;
        return getStyle(layer);
      },
    });

    //console.log(mvtSource.layers[Object.keys(layers)[0]],'mvtSource');
    //Add layer
    map.addLayer(mvtSource);
    // var miniMap = new L.Control.MiniMap(littleMap).addTo(map);

    console.log(mvtSource.layers, "mvtSource.layers");
    console.log(typeof mvtSource.layers, "typeof mvtSource.layers");

    var x = mvtSource.layers;
    console.log(x.sua_restricted, "x");
    // var y = mvtSource.layers.sua_restricted.features.coordinates

    // console.log(y,"y");

    // var keys = Object.keys(x)

    // console.log(keys,"keys");

    // ------------------------------------//

    // ---------- RESERVED AIRSPACES LOAD --------------------------//
    var baseURL =
      location.protocol +
      "//" +
      location.hostname +
      (location.port && ":" + location.port);
    //console.log(baseURL,"baseURL")
    // function getData() {
    //   return $.ajax({
    //     url: `${baseURL}/applications/airspace/geojson/`,
    //     type: "GET",
    //     cache: true,
    //   });
    // }

    // getData().then(function (data) {
    //   // do something with data
    //   // Note that calling `.eachLayer` here depends on setting GeoJSON _directly_
    //   // above. If you're loading GeoJSON asynchronously, like from CSV or from a file,
    //   // you will need to do this within a `featureLayer.on('ready'` event.
    //   var featureLayer = L.mapbox.featureLayer(data).addTo(map);

    //   featureLayer.eachLayer(function (layer) {
    //     //console.log(layer,"layer in each")
    //     //map.fitBounds(featureLayer.getBounds());
    //     // here you call `bindPopup` with a string of HTML you create - the feature
    //     // properties declared above are available under `layer.feature.properties`
    //     var content =
    //       "<h2>Booked Airspace</h2>" +
    //       "<p>From: " +
    //       layer.feature.properties.name +
    //       "<br />" +
    //       "to: " +
    //       layer.feature.properties.name +
    //       "</p>";
    //     layer.bindPopup(content);
    //   });
    // });

    // ---------------------------------//
  }, []);

  //
  useEffect(() => {});
  //
  return (
    <div className="page-inner" style={{ padding: "5px" }}>
      <hr />
      <div id="main-wrapper">
        <div className="col-xs-9">
          <p>Leaflet JS</p>

          <div
            id="mapid1"
            className="map"
            style={{ height: "100vh", width: "100%" }}
          ></div>
        </div>
      </div>
    </div>
  );
}

export default Airspace;

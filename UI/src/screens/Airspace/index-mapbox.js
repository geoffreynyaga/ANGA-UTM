import React, { useEffect } from "react";
import * as mapboxgl from "mapbox-gl";
// import ContextualAirspacePlugin from "../../js-contextual-airspace-plugin/src/index";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import * as L from "leaflet";

function Airspace() {
  useEffect(() => {
    const AIRMAP_API_KEY =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVkZW50aWFsX2lkIjoiY3JlZGVudGlhbHw0Z242Z0tNaW5KODQza2h6NjRFZGJpT1pBS25hIiwiYXBwbGljYXRpb25faWQiOiJhcHBsaWNhdGlvbnxRTHk0NVIySDhKV3YzZ2lOUUdtM1poRHYwQTRxIiwib3JnYW5pemF0aW9uX2lkIjoiZGV2ZWxvcGVyfDc5NVlrQm1Db3hSQm53aTluOURiTEh3OTVLMFEiLCJpYXQiOjE1MjcxNTA4MDJ9.TkESuJIEQ9pjfU9F4TgIUNCF15OO2eeWU1GRONXf33Q";
    const MAPBOX_ACCESS_TOKEN =
      "pk.eyJ1IjoiZ2VvZmZyZXlueWFnYSIsImEiOiJjamdmM3Q5NG4wdnprMnhyMGJqd3U1N25yIn0.R_3l_E-DDVpHQ0rL3zgElQ";

    // Create an instance of the map

    const map = new mapboxgl.Map({
      container: "map",
      style: "mapbox://styles/mapbox/streets-v8",
      center: [37.496475, 0.024212],
      zoom: 8,
      accessToken: MAPBOX_ACCESS_TOKEN,
    });

    //

    function getRandomColor() {
      var letters = "0123456789ABCDEF";
      var color = "#";
      for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }

    function addRulesets(jurisdictions) {
      let rulesets = [];
      jurisdictions.forEach((jurisdiction) => {
        jurisdiction.rulesets.forEach((ruleset) => {
          if (ruleset.selection_type == "pick1") {
            if (ruleset.id == "usa_part_107") rulesets.push(ruleset);
          } else {
            rulesets.push(ruleset);
          }
        });
      });
      return rulesets;
    }

    function parseJurisdictions() {
      var layers = map.queryRenderedFeatures();

      // Iterate through layers
      var jurisdictions = layers
        .filter(
          (x) =>
            x.layer.source == "jurisdictions" &&
            x.properties.jurisdiction !== null
        )
        .map((feature) => JSON.parse(feature.properties.jurisdiction));

      console.log(jurisdictions, "jurisdictions");
      // Remove duplicate or empty jurisdictions
      jurisdictions = jurisdictions
        .filter((x) => x.rulesets.length > 0)
        .filter((obj, pos, arr) => {
          return (
            arr.map((mapObj) => mapObj["uuid"]).indexOf(obj["uuid"]) === pos
          );
        });

      return jurisdictions;
    }

    // Add layers
    map.on("load", () => {
      // Add Jurisdictions
      console.log("----------map on load------------------");
      map.addLayer(
        {
          id: "jurisdictions",
          type: "fill",
          source: {
            type: "vector",
            tiles: [
              "https://api.airmap.com/tiledata/v1/base-jurisdiction/{z}/{x}/{y}",
            ],
            minzoom: 6,
            maxzoom: 12,
          },
          "source-layer": "jurisdictions",
          minzoom: 6,
          maxzoom: 22,
        },
        "background"
      );
    });

    map.on("sourcedata", (data) => {
      // Check for jurisdiction
      // console.log("-----------map on source data----------");
      // console.log(data, "sourcedata");
      if (data.sourceId == "jurisdictions" && data.isSourceLoaded) {
        // Parse jurisdiction
        console.log("step 2");
        console.log(data.sourceId, "data.sourceId");
        console.log(data.isSourceLoaded, "data.isSourceLoaded");

        var jurisdictions = parseJurisdictions();
        // Add rulesets
        var rulesets = addRulesets(jurisdictions);
        console.log(rulesets, "rulesets");

        rulesets.forEach((ruleset) => {
          // Add Part 107 Source

          console.log(
            "https://api.airmap.com/tiledata/v1/" +
              ruleset.id +
              "/" +
              ruleset.layers.join(",") +
              "/{z}/{x}/{y}" +
              `?apiKey=${AIRMAP_API_KEY}`
          );
          console.log(ruleset.id, "reuleset.id");
          map.addSource(ruleset.id, {
            type: "vector",
            tiles: [
              "https://api.airmap.com/tiledata/v1/" +
                ruleset.id +
                "/" +
                ruleset.layers.join(",") +
                `/{z}/{x}/{y}?apiKey=${AIRMAP_API_KEY}`,
            ],
            minzoom: 6,
            maxzoom: 12,
          });

          ruleset.layers.forEach((layer) => {
            // All Controlled Airspace
            console.log(layer, "layer");
            console.log(ruleset.id + "_" + layer, "id: ruleset.id + _ + layer");

            let airspaceLayer = {
              type: "fill",

              id: ruleset.id + "_" + layer,
              source: ruleset.id,
              "source-layer": ruleset.id + "_" + layer,
              interactive: true,
              paint: {
                "fill-opacity": 0.4,
                "fill-color": getRandomColor(),
              },
            };

            console.log(airspaceLayer + "airspaceLayer");

            map.addLayer(airspaceLayer, ruleset.id);
          });
        });
      }
    });
    // const config = {
    //   airmap: {
    //     api_key: AIRMAP_API_KEY,
    //   },
    //   auth0: {
    //     client_id: "",
    //     callback_url: "",
    //   },
    //   mapbox: {
    //     access_token: MAPBOX_ACCESS_TOKEN,
    //   },
    // };
    // const options = {
    //   preferredRulesets: ["usa_part_107", "deu_rules_waiver"],
    //   overrideRulesets: [
    //     // 'usa_part_107'
    //   ],
    //   enableRecommendedRulesets: true,
    //   theme: "light",
    //   /* refer to the docs for a comprehensive list of options */
    // };
    // const plugin = new ContextualAirspacePlugin(config, options);
    // // map.addControl(plugin, "top-left");
    //
  }, []);

  //
  useEffect(() => {
    var mymap = L.map("mapid1").setView([51.505, -0.09], 13);
    L.tileLayer(
      "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw",
      {
        maxZoom: 18,
        attribution:
          'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
          'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: "mapbox/streets-v11",
        tileSize: 512,
        zoomOffset: -1,
      }
    ).addTo(mymap);
  });
  //
  return (
    <div className="page-inner" style={{ padding: "5px" }}>
      <hr />
      <div id="main-wrapper">
        {/* <div className="col-xs-3">
          <p>Mapbox</p>
          <div
            id="map"
            className="map"
            style={{ height: "100vh", width: "300" }}
          ></div>
        </div> */}

        <div className="col-xs-6">
          <p>Leaflet JS</p>

          <div
            id="mapid1"
            className="map"
            style={{ height: "100vh", width: "100%" }}
          ></div>
          <div className="col-xs-6">
            <p>React Leaflet</p>

            <MapContainer
              center={[51.505, -0.09]}
              zoom={13}
              scrollWheelZoom={false}
              style={{ height: "100vh", width: "100%" }}
            >
              <TileLayer
                attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <Marker position={[51.505, -0.09]}>
                <Popup>
                  A pretty CSS3 popup. <br /> Easily customizable.
                </Popup>
              </Marker>
            </MapContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Airspace;

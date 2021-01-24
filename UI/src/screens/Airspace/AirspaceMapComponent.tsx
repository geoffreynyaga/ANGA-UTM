import React, { useEffect, useRef, useState } from "react";
import {
  Map,
  TileLayer,
  withLeaflet,
  LayersControl,
  GeoJSON,
  FeatureGroup,
  Tooltip,
  Marker,
  Popup,
} from "react-leaflet";

import {
  polygon as TurfPolygon,
  area as TurfArea,
  circle as TurfCircle,
} from "@turf/turf";
import VectorGridDefault from "react-leaflet-vectorgrid";
import { EditControl } from "react-leaflet-draw";

import { renderToStaticMarkup } from "react-dom/server";
import { divIcon } from "leaflet";
import { LatLng } from "leaflet";

import Search from "react-leaflet-search";
import LocateControl from "./locate";

const VectorGrid = withLeaflet(VectorGridDefault);

interface MarkerInterface {
  coordinates: {
    lat: string;
    lng: string;
  };
  data: Properties;
}

interface GeojsonType {
  type:
    | "Polygon"
    | "Point"
    | "MultiPoint"
    | "LineString"
    | "MultiLineString"
    | "MultiPolygon"
    | "GeometryCollection"
    | "Feature"
    | "FeatureCollection";
  features: Feature[];
}

interface Feature {
  id: number;
  type:
    | "Polygon"
    | "Point"
    | "MultiPoint"
    | "LineString"
    | "MultiLineString"
    | "MultiPolygon"
    | "GeometryCollection"
    | "Feature"
    | "FeatureCollection";
  geometry: GeometryType;
  properties: Properties;
}

interface GeometryType {
  type:
    | "Polygon"
    | "Point"
    | "MultiPoint"
    | "LineString"
    | "MultiLineString"
    | "MultiPolygon"
    | "GeometryCollection"
    | "Feature"
    | "FeatureCollection";
  coordinates: Array<Array<number[]>>;
}

interface Properties {
  user_full_name: string;
  user_phone_number: string;
  user_profile_pic: string;
  user_organization: string;
  created_by: number;
  rpas_name: string;
  rpas_serial: string;
  rpas_pic: string;
  airframe_type: string;
  start_day: Date;
  start_time: string;
  start_datetime: Date;
  end: string;
  mission_type_display: string;
  area: number;
  application_number: null | string;
  status: number;
  expiry: boolean;
  centroid: Centroid;
}

interface Centroid {
  type: string;
  coordinates: number[];
}
interface Props {
  draw: boolean;
}

function AirspaceMapComponent(props: Props) {
  const [airspaceClassLayers, setAirspaceClassLayers] = useState([
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
    "heliports",
    "prisons",
  ]);

  const [airspaceClassLayers2, setAirspaceClassLayers2] = useState([
    "hospitals",
    "schools",
    "power_plants",
    "tfrs",
    "wildfires",
  ]);

  const [selectedAirspaceClassLayers] = useState([]);

  const [urlState, setUrlState] = useState<string | null>(null);
  const [urlState2, setUrlState2] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [showAirspaceClass, setShowAirspaceClass] = useState<boolean>(true);
  const [showAirspaceClass2, setShowAirspaceClass2] = useState<boolean>(true);
  const [geojson, setGeojson] = useState<GeojsonType | null>(null);
  const [geofencegeojson, setGeofenceGeojson] = useState<GeojsonType | null>(
    null
  );
  const [drawnGeoJSON, setDrawnGeoJSON] = useState<GeojsonType | null>(null);

  const [drawnGeoJSONProperties, setDrawnGeoJSONProperties] = useState<any>(
    null
  );

  const [search, setSearch] = useState<any>(new LatLng(37.8, -1.9));
  const [bounds, setBounds] = useState<any>([
    [-4.77369399748329, 33.909937402767],
    [5.03342194387382, 41.9067738648657],
  ]);

  const AIRMAP_API_KEY: string =
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVkZW50aWFsX2lkIjoiY3JlZGVudGlhbHw0Z242Z0tNaW5KODQza2h6NjRFZGJpT1pBS25hIiwiYXBwbGljYXRpb25faWQiOiJhcHBsaWNhdGlvbnxRTHk0NVIySDhKV3YzZ2lOUUdtM1poRHYwQTRxIiwib3JnYW5pemF0aW9uX2lkIjoiZGV2ZWxvcGVyfDc5NVlrQm1Db3hSQm53aTluOURiTEh3OTVLMFEiLCJpYXQiOjE1MjcxNTA4MDJ9.TkESuJIEQ9pjfU9F4TgIUNCF15OO2eeWU1GRONXf33Q";

  useEffect(() => {
    console.log("useEffect");
    if (geojson === null || geofencegeojson === null) {
      fetchGeoJSON();
      fetchGeofenceGeoJSON();
    }
    //
    var url: string = "https://api.airmap.com/maps/v4/tiles";
    let layers = airspaceClassLayers;
    let layers2 = airspaceClassLayers2;

    var layerString = layers.toString().split(",");
    var layerString2 = layers2.toString().split(",");

    let tryUrl =
      url + "/" + layerString + `/{z}/{x}/{y}.pbf?apikey=${AIRMAP_API_KEY}`;

    let tryUrl2 =
      url + "/" + layerString2 + `/{z}/{x}/{y}.pbf?apikey=${AIRMAP_API_KEY}`;

    if (isLoading === false) {
      console.log("useEffect, Loading is False");
      setUrlState(tryUrl);
      setUrlState2(tryUrl2);
    } else {
      console.log("useEffect, Loading is true");
      setUrlState(tryUrl);
      setUrlState2(tryUrl2);
      setIsLoading(false);
      console.log(isLoading, "should be false");
    }
  }, [isLoading]);
  //

  //
  let options = {
    type: "protobuf",
    popup: (layer: any) =>
      `<div>${JSON.stringify(layer.properties.type)} <hr/>${
        layer.properties.name
      }</div>`,
    vectorTileLayerStyles: {
      airports_commercial: function (properties: any) {
        // console.log(properties, "shoooow me!!!");
        return {
          fillColor: "#F0E1C5",
          fillOpacity: 0.8,
          fill: true,
          weight: 2,
          color: "#D9A851",
          opacity: 1,
          // radius: 6,
        };
      },
      airports_recreational_private: function (properties: any) {
        // console.log(properties, "shoooow me!!!");
        return {
          fillColor: "#D5D0C2",
          fillOpacity: 0.8,
          fill: true,
          weight: 2,
          color: "#D9A851",
          opacity: 1,
          // radius: 6,
        };
      },
      airports_commercial_private: function (properties: any) {
        // console.log(properties, "shoooow me!!!");
        return {
          fillColor: "#D5D0C2",
          fillOpacity: 0.8,
          fill: true,
          weight: 2,
          color: "#D9A851",
          opacity: 1,
          // radius: 6,
        };
      },
      heliports: {
        fillColor: "#F0E1C5",
        fill: true,
        fillOpacity: 0.6,
        weight: 1,

        color: "#F6A517",
      },
      class_b: {
        fillColor: "rgba(26, 116, 179, 0.2)",
        fill: true,
        fillOpacity: 0.8,

        color: "rgb(26, 116, 179)",
      },
      class_c: {
        fillColor: "#D4DCE5",
        fill: true,
        fillOpacity: 0.7,
        color: "#9B6C9D",
        weight: 1,
      },
      class_d: {
        fillColor: "rgba(26, 116, 179, 0.2)",
        fillOpacity: 0.7,
        fill: true,
        dashArray: ".5, 8",

        color: "rgb(26, 116, 179)",
      },
      class_e0: {
        fillColor: "rgba(155, 108, 157, 0.2)",
        fill: true,
        fillOpacity: 0.8,

        color: "rgb(155, 108, 157)",
      },
      schools: {
        fillColor: "#f5a519",
        fill: true,
        fillOpacity: 1,

        color: "#ffd460",
      },
      hospitals: {
        fillColor: "#f8f8f8",
        fill: true,
        fillOpacity: 1,

        color: "#86a6df",
      },
      // case "national_parks":
      noaa: {
        fillColor: "rgba(224, 18, 18, 0.2)",
        fill: true,
        fillOpacity: 0.7,

        color: "rgb(224, 18, 18)",
      },
      sua_prohibited: {
        fillColor: "rgba(27, 90, 207, 0.2)",
        fill: true,
        fillOpacity: 0.6,
        weight: 1,

        color: "rgb(27, 90, 207)",
      },
      sua_restricted: {
        fillColor: "#CFDAEB",
        fill: true,
        fillOpacity: 0.6,
        weight: 1,

        color: "#3D72D4",
      },

      power_plants: {
        fillColor: "#F1DBB3",
        fill: true,
        fillOpacity: 0.6,
        weight: 1,

        color: "#F6A517",
      },
      prisons: {
        fillColor: "rgb(224, 18, 18)",
        fill: true,
        fillOpacity: 0.7,

        color: "rgb(224, 18, 18)",
      },
    },
    subdomains: "abcd",
    key: AIRMAP_API_KEY,
    zIndex: 1,
    interactive: true,
  };

  function removeAirspace(selectedAirspace: string) {
    let x = airspaceClassLayers;
    const index = x.indexOf(selectedAirspace);
    x.splice(index, 1);

    setAirspaceClassLayers(x);
    setIsLoading(true);
  }

  function toggleAirspace(selectedAirspace: string) {
    let x = airspaceClassLayers;
    let y = selectedAirspaceClassLayers;
    const index = x.indexOf(selectedAirspace);
    x.splice(index, 1);

    setAirspaceClassLayers(x);
    setIsLoading(true);
  }

  function toggleAirspaceClasses(selectedAirspaceClass: string) {
    if (selectedAirspaceClass === "class1") {
      console.log("class selected to be toggled");
      setShowAirspaceClass(!showAirspaceClass);
    } else if (selectedAirspaceClass === "class2") {
      setShowAirspaceClass2(!showAirspaceClass2);
    } else {
      console.log("error: not here");
    }
    setIsLoading(true);
  }

  //
  const fetchGeoJSON = async () => {
    console.log("called");
    return fetch(
      "http://localhost:8000/api/applications/v1/reserve-airspaces/list/",
      {
        method: "GET", // or 'PUT'
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          Authorization: "Token b363791c3baa5ac7b7023f2f2189ea2e6794f820",
        },
      }
    )
      .then((response) => response.json())
      .then((data) => {
        // console.log("Success: fetchGeoJSON", data);
        setGeojson(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  //
  const fetchGeofenceGeoJSON = async () => {
    console.log("called");
    return fetch("http://localhost:8000/api/maps/geofence-locations/", {
      method: "GET", // or 'PUT'
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Authorization: "Token b363791c3baa5ac7b7023f2f2189ea2e6794f820",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // console.log("Success: fetchGeofenceGeoJSON", data);
        setGeofenceGeojson(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const geoJSONStyle = (feature: any) => {
    switch (feature.properties.status) {
      //pending
      case 0:
        // console.log("case 0 pending", "getReserveAreaColor");
        return {
          fillColor: "#FFCD41",
          weight: 2,
          opacity: 1,
          color: "red",
          dashArray: "3",
          fillOpacity: 0.5,
        };
      case 1: //denied
        // console.log("case 1 denied", "getReserveAreaColor");

        return {
          fillColor: "#be6a15",
          weight: 4,
          opacity: 1,
          color: "#f3cf7a",
          dashArray: "1",
          fillOpacity: 0.8,
        };
      case 2: //approved
        // console.log("case 2 approved", "getReserveAreaColor");

        return {
          fillColor: "#2cb978",
          weight: 2,
          opacity: 1,
          color: "#83e85a",
          dashArray: "1",
          fillOpacity: 0.95,
        };
      default:
        console.log("case default ", "getReserveAreaColor");

        return {
          fillColor: "blue",
          weight: 2,
          opacity: 1,
          color: "white",
          dashArray: "3",
          fillOpacity: 0.8,
        };
    }
  };

  //
  const geofenceJSONStyle = (feature: any) => {
    return {
      fillColor: "red",
      weight: 1,
      opacity: 1,
      // color: "white",
      // dashArray: "3",
      fillOpacity: 0.5,
    };
  };
  //

  //
  const onEachAirspaceFeature = (feature: any, layer: any) => {
    // does this feature have a property named popupContent?
    // console.log(JSON.stringify(feature.geometry), "onEachAirspaceFeature");

    if (
      feature.properties !== undefined &&
      feature.properties.start_day !== undefined
    ) {
      let data = layer.feature.properties;
      // console.log(data, "data");

      var y = `
      <div
      class="box"
      style="
        width: 200px;
        // height: 300px;
        // margin-left: 30px;
        border-width: 2px;
        border-color: red;
        background-color: #e2f3f5;
      "
    >
      <div class="panel panel-default"
      style="
     
      marginBottom: 0px;
      padding-bottom: 0px;
     
    ">
        <div class="panel-heading">
          ${data.application_number ? data.application_number : ""}
        </div>
        
      <div  class="panel-body" 
      style="
      align-items: center;
      align-content: center;
      padding:0px;
      margin-top: 0px;
      marginBottom: 0px;

      padding-top: 5px;
      padding-bottom: 5px;

    ">
        <span style="text-align: center; ">
          <p 
          style=" 
          display: block;
          margin-top: 5px;
          padding-top: 5px;
         
        "
        >
            <b>${data.user_organization}</b>
          </p>
        </span>

        <p>
          Mission Start: <b>${data.start_day}</b>
        </p>
        <p>
          from <b>${data.start_time}</b>
          to: <b> ${data.end}</b>
        </p>
        <p>
          RPAS: <b>${data.rpas_name}</b> Type: <b> ${data.airframe_type}</b>
        </p>
        <img  src=${data.rpas_pic} 
        style="
        display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;">

  <button data-toggle="collapse" data-target="#demo"
  style="
        display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;"
  >
                  Details
                </button>
      </div>

      <div id="demo" class="collapse" >
      <div
          class="panel-body"
          style="
            flex-direction: "column";
            justify-content: "center";
            align-items: "center";
            align-content: "center";
            margin: "0px";
            padding: "5px";
            // position: "relative",
            // top: "65px",
            // left: "50%",
            // marginLeft: "-45px",
          "
        >
          <div
            // className="widget-user-image"
            style="
              flex-direction: column;
              justify-content: center;
              align-items: center;
              align-content: center;
              // position: relative;
              // top: "65px",
              // left: "50%",
              // marginLeft: "-45px",
            "
          >
            <img
              // class="img-circle"
              src=${data.user_profile_pic}
              alt="User Avatar"
              style=" border-radius: 50%;
                height: auto;
                border: 3px solid #fff;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 50%;
              "
            >
          </div>
        </div>

      <div
      
          class="panel-footer "
          style="border-top-left-radius: 0;
            border-top-right-radius: 0;
            border-bottom-left-radius: 3px;
            border-bottom-right-radius: 3px;
            border-top:  1px solid #f4f4f4;
            padding: 10px;
            background-color: #ffffff;
          "
        >
          <div class="row">
            <div class="col-xs-4">
              <div
                className="description-block"
                style="display: block;
                  margin: "10px 0";
                  text-align: "center";
                "
              >
                <a href="tel:${data.user_phone_number}">
                  <h5>
                    <i class="ion-ios-telephone"></i>
                  </h5>
                  <span class="description-text">Call</span>
                </a>
              </div>
            </div>
            <div class="col-xs-4">
              <div
                style="
                  justify-content: center;
                  align-items: center;
                "
              >
                
              </div>
            </div>
            <div class="col-xs-4 ">
              <div
                class="description-block"
                style="
                  display: block;
                  margin: 10px 0;
                  text-align: center;
                "
              >
                <a href="/account/profile/${data.created_by}">
                  <h5>
                    <i class="ion-person"></i>
                  </h5>
                  <span class="description-text ">Profile </span>
                </a>
              </div>
            </div>
          </div>
          </div>

        </div>
      </div>
      
    </div>
  
      `;
      layer.bindPopup(y);
    } else {
      console.log("why im i here");
    }
  };
  //

  const onEachGeofenceFeature = (feature: any, layer: any) => {
    if (
      feature.properties !== undefined &&
      feature.properties.name !== undefined
    ) {
      // console.log(
      //   "these are present >>>> feature.properties && feature.properties.start_day"
      // );
      // console.log(feature.properties.name, "feature.properties.name");

      var name = feature.properties.name ? feature.properties.name : "geofence";
      var content = "<h4>Restricted Area:</h4>" + "<hr />" + name + "</p>";
      layer.bindPopup(content);
    } else {
      console.log("why im i here");
    }
  };
  //
  const getAdvisory = async (data: any) => {
    console.log("getAdvisory called: ", data);

    return fetch("https://api.airmap.com/rules/v1/", {
      method: "POST", // or 'PUT'
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        // Authorization: "Token b363791c3baa5ac7b7023f2f2189ea2e6794f820",
        "x-api-key": AIRMAP_API_KEY,
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success: getAdvisory", data);
        // setGeojson(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };
  //
  function onEditPath(e: any) {
    console.log(e, "onEditPath");
  }
  //
  function onCreate(e: any) {
    console.log(e.layer, "onCreate");

    // featureGroup.addLayer(e.layer);
    var json = e.layer.toGeoJSON();
    console.log(json, "json");

    setDrawnGeoJSON(json);
    var y = { geometry: json["geometry"] };
    getAdvisory(y);

    if (json.geometry.type === "Point") {
      console.log(e.layer.getRadius(), "e.layer.getRadius()");
      json.properties.radius = e.layer.getRadius();

      var center = json.geometry.coordinates;
      var radius = json.properties.radius;
      // var options = { steps: 10, units: "meters", properties: { foo: "bar" } };
      var circle = TurfCircle(center, radius, {
        steps: 10,
        units: "meters",
        properties: {},
      });

      // var area2 = TurfArea(circle);
      var area = 3.141 * radius * radius;

      // console.log(area, "circle area");
      // console.log(area2, "circle area2");
      // console.log((area2 - area) * 0.000247105, "circle diff");

      // console.log(circle, "circle area");

      // console.log(center, "circle center");

      if (area / 1e6 >= 9) {
        console.log("area more than 9sq km");

        setDrawnGeoJSONProperties({
          area: `${(area / 1e6).toFixed(1)} sq.km`,
          error: "Area greater than recommended 9sq. km",
        });
      } else if (area / 1e6 < 4) {
        setDrawnGeoJSONProperties({
          area: ` ${(area * 0.000247105).toFixed(2)} acres`,
        });
      } else {
        setDrawnGeoJSONProperties({
          area: `${(area / 1e6).toFixed(1)} sq.km`,
        });
      }
    }

    if (json.geometry.type === "Polygon") {
      console.log(json.geometry.type, "json.geometry.type");

      // var polygon = TurfPolygon([
      //   [
      //     [125, -15],
      //     [113, -22],
      //     [154, -27],
      //     [144, -15],
      //     [125, -15],
      //   ],
      // ]);

      var polygon = TurfPolygon(json.geometry.coordinates);

      var polygonArea = TurfArea(polygon);
      console.log(polygonArea, "area");

      if (polygonArea / 1e6 >= 9) {
        console.log("area more than 9sq km");

        setDrawnGeoJSONProperties({
          area: `${(polygonArea / 1e6).toFixed(1)} sq.km`,
          error: "Area greater than recommended 9sq. km",
        });
      } else if (polygonArea / 1e6 < 4) {
        setDrawnGeoJSONProperties({
          area: ` ${(polygonArea * 0.000247105).toFixed(2)} acres`,
        });
      } else {
        setDrawnGeoJSONProperties({
          area: `${(polygonArea / 1e6).toFixed(1)} sq.km`,
        });
      }
    }
  }

  var L = window.L;
  const customMarker1 = L.icon({
    iconUrl: "https://unpkg.com/leaflet@1.4.0/dist/images/marker-icon.png",
    iconSize: [25, 41],
    iconAnchor: [10, 41],
    popupAnchor: [2, -40],
  });

  const iconMarkup = (property: Properties) => {
    // ("PLANE", "PLANE"),
    //     ("QUAD", "QUADCOPTER"),
    //     ("HEXA", "HEXACOPTER"),
    //     ("TRI", "TRICOPTER"),
    //     ("OCTA", "OCTACOPTER"),
    //     ("VTOL", "VTOL"),
    switch (property.airframe_type) {
      case "PLANE":
        return renderToStaticMarkup(
          <img
            src="/icons/fixed-wing.png"
            style={{ height: 25, width: 30 }}
            alt="quad"
          />
        );
      case "QUADCOPTER":
        return renderToStaticMarkup(
          <img
            src="/icons/quadcopter.png"
            style={{ height: 25, width: 25 }}
            alt="quad"
          />
        );
      default:
        return renderToStaticMarkup(
          <img
            src="/icons/quad.png"
            style={{ height: 25, width: 25 }}
            alt="quad"
          />
        );
    }
  };

  const customMarkerIcon = (property: Properties) => {
    return divIcon({
      html: iconMarkup(property),
      className: "dummy",
      iconSize: [25, 25],
      // iconAnchor: [10, 41],
      popupAnchor: [2, -40],
    });
  };

  var customMarker = L.Icon.extend({
    options: {
      shadowUrl: "leaf-shadow.png",
      iconSize: [38, 95],
      shadowSize: [50, 64],
      iconAnchor: [22, 94],
      shadowAnchor: [4, 62],
      popupAnchor: [-3, -76],
    },
  });

  //
  // Setup LocateControl options
  const locateOptions = {
    position: "topleft",
    strings: {
      title: "Show me where I am, yo!",
    },
    showCompass: true,
    onActivate: () => {}, // callback before engine starts retrieving locations
    onLocationError: function (e: any) {
      console.log(e);
      console.log("Location access denied.");
    },
    LocationFound: function (e: any) {
      console.log("_onLocationFound", e);
    },
    locationfound: function (e: any) {
      console.log("onLocationFound", e);
    },
  };
  return (
    <div>
      <Map
        center={[-1.5, 36.9]}
        zoom={11}
        scrollWheelZoom={true}
        style={{ height: "95vh", width: "100%" }}
        // touchZoom={true}
        maxBounds={bounds}
        minZoom={10}
        maxZoom={16}
      >
        <LayersControl position="topright">
          <LayersControl.BaseLayer checked name="OpenStreetMap.Mapnik">
            <TileLayer
              attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
          </LayersControl.BaseLayer>
          {/* // */}
          <LayersControl.BaseLayer name="OpenStreetMap.BlackAndWhite">
            <TileLayer
              attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
              url="https://tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png"
            />
          </LayersControl.BaseLayer>

          <LocateControl options={locateOptions} startDirectly />

          <Search
            // customProvider={this.provider}
            //   onChange={(info) => {
            //     console.log("FROM onChange: ", info);
            //   }}
            position="topleft"
            inputPlaceholder="Search Places"
            // search={this.state.search}
            showMarker={false}
            zoom={14}
            closeResultsOnClick={true}
            openSearchOnLoad={false}
            // these searchbounds would limit results to only Turkey.
            providerOptions={{
              searchBounds: [
                new LatLng(-5.320104825856594, 33.74990005448136),
                new LatLng(4.966902087397791, 42.80099156930539),
              ],
              region: "ke",
            }}
            // default provider OpenStreetMap
            // provider="BingMap"
            // providerKey="AhkdlcKxeOnNCJ1wRIPmrOXLxtEHDvuWUZhiT4GYfWgfxLthOYXs5lUMqWjQmc27"
          >
            {(info) => (
              <Marker position={info?.latLng}>
                {"this.customPopup(info)"}
              </Marker>
            )}
          </Search>

          <LayersControl.Overlay
            checked
            name=" Airport, Heliport, Controlled Airspace, Special Use
              Airspace,Temporary Flight Restriction"
          >
            {urlState !== null && showAirspaceClass === true ? (
              <VectorGrid
                {...Object.assign(options, {
                  url: urlState,
                })}
                // updateWhenIdle={true}
                // url={urlState}
                // updateInterval={600}
                key={urlState}
              />
            ) : null}
          </LayersControl.Overlay>

          {/* // */}
          <LayersControl.Overlay
            checked
            name="School, Hospital, Wildfire, Power Plant, Prison"
          >
            {urlState2 !== null && showAirspaceClass2 === true ? (
              <VectorGrid
                {...Object.assign(options, {
                  url: urlState2,
                })}
                // updateWhenIdle={true}
                // url={urlState2}
                // updateInterval={600}
                key={urlState2}
              />
            ) : null}
          </LayersControl.Overlay>

          {/* // */}
          {geojson !== null ? (
            <LayersControl.Overlay checked name="All Reserved Airspaces">
              <GeoJSON
                key={"geojson"}
                data={geojson}
                style={geoJSONStyle}
                onEachFeature={onEachAirspaceFeature}

                // @ts-ignore
                // pointToLayer={pointToLayerGeoJSON}
              />
            </LayersControl.Overlay>
          ) : (
            ""
          )}
          {/* // */}
          {geofencegeojson !== null ? (
            <LayersControl.Overlay checked name="Custom Geofences">
              <GeoJSON
                key={"geofencegeojson"}
                data={geofencegeojson}
                style={geofenceJSONStyle}
                onEachFeature={onEachGeofenceFeature}
              />
            </LayersControl.Overlay>
          ) : (
            ""
          )}
        </LayersControl>

        <FeatureGroup>
          {geojson !== null
            ? geojson.features.map((feature: any, idx: number) => (
                // var x = position.coordinates;
                <Marker
                  key={`marker-${idx}`}
                  position={[
                    feature.properties.centroid.coordinates[1],
                    feature.properties.centroid.coordinates[0],
                  ]}
                  icon={customMarkerIcon(feature.properties)}
                >
                  <Popup>
                    <div
                      className="box"
                      style={{
                        width: 200,
                        borderWidth: 2,
                        borderColor: "red",
                        backgroundColor: "#e2f3f5",
                      }}
                    >
                      <div
                        className="panel panel-default"
                        style={{ marginBottom: 0, paddingBottom: 0 }}
                      >
                        <div className="panel-heading">
                          {feature.properties.application_number
                            ? feature.properties.application_number
                            : ""}
                        </div>

                        <div
                          className="panel-body"
                          style={{
                            alignItems: "center",
                            alignContent: "center",
                            padding: 0,
                            marginTop: 0,
                            marginBottom: 0,

                            paddingTop: 5,
                            paddingBottom: 5,
                          }}
                        >
                          <span style={{ textAlign: "center" }}>
                            <p
                              style={{
                                display: "block",
                                marginTop: 5,
                                paddingTop: 5,
                              }}
                            >
                              <b>{feature.properties.user_organization}</b>
                            </p>
                          </span>

                          <p>
                            Mission Start: <b>{feature.properties.start_day}</b>
                          </p>
                          <p>
                            from <b>{feature.properties.start_time}</b>
                            to: <b> {feature.properties.end}</b>
                          </p>
                          <p>
                            RPAS: <b>{feature.properties.rpas_name}</b> Type:{" "}
                            <b> {feature.properties.airframe_type}</b>
                          </p>
                          <img
                            src={feature.properties.rpas_pic}
                            style={{
                              display: "block",
                              marginLeft: "auto",
                              marginRight: "auto",
                              width: "50%",
                            }}
                          />

                          <button
                            data-toggle="collapse"
                            data-target="#demo"
                            style={{
                              display: "block",
                              marginLeft: "auto",
                              marginRight: "auto",
                              width: "50%",
                            }}
                          >
                            Details
                          </button>
                        </div>

                        <div id="demo" className="collapse">
                          <div
                            className="panel-body"
                            style={{
                              flexDirection: "column",
                              justifyContent: "center",
                              alignItems: "center",
                              alignContent: "center",
                              margin: "0px",
                              padding: "5px",
                              // position: "relative",
                              // top: "65px",
                              // left: "50%",
                              // marginLeft: "-45px",
                            }}
                          >
                            <div
                              // className="widget-user-image"
                              style={{
                                flexDirection: "column",
                                justifyContent: "center",
                                alignItems: "center",
                                alignContent: "center",
                                // position: relative;
                                // top: "65px",
                                // left: "50%",
                                // marginLeft: "-45px",
                              }}
                            >
                              <img
                                // className="img-circle"
                                src={feature.properties.user_profile_pic}
                                alt="User Avatar"
                                style={{
                                  borderRadius: "50%",
                                  height: "auto",
                                  border: "3px solid #fff",
                                  display: "block",
                                  marginLeft: "auto",
                                  marginRight: "auto",
                                  width: "50%",
                                }}
                              />
                            </div>
                          </div>

                          <div
                            className="panel-footer "
                            style={{
                              borderTopLeftRadius: 0,
                              borderTopRightRadius: 0,
                              borderBottomLeftRadius: 3,
                              borderBottomRightRadius: 3,
                              borderTop: "1px solid #f4f4f4",
                              padding: 10,
                              backgroundColor: " #ffffff",
                            }}
                          >
                            <div className="row">
                              <div className="col-xs-4">
                                <div
                                  className="description-block"
                                  style={{
                                    display: "block",
                                    margin: "10px 0",
                                    textAlign: "center",
                                  }}
                                >
                                  <a href="tel:${feature.properties.user_phone_number}">
                                    <h5>
                                      <i className="ion-ios-telephone"></i>
                                    </h5>
                                    <span className="description-text">
                                      Call
                                    </span>
                                  </a>
                                </div>
                              </div>
                              <div className="col-xs-4">
                                <div
                                  style={{
                                    justifyContent: "center",
                                    alignItems: "center",
                                  }}
                                ></div>
                              </div>
                              <div className="col-xs-4 ">
                                <div
                                  className="description-block"
                                  style={{
                                    display: "block",
                                    margin: "10px 0",
                                    textAlign: "center",
                                  }}
                                >
                                  <a href="/account/profile/${feature.properties.created_by}">
                                    <h5>
                                      <i className="ion-person"></i>
                                    </h5>
                                    <span className="description-text ">
                                      Profile{" "}
                                    </span>
                                  </a>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </Popup>
                </Marker>
              ))
            : ""}
        </FeatureGroup>

        {/* Draw */}

        {props.draw ? (
          <FeatureGroup>
            <EditControl
              position="topleft"
              onEdited={onEditPath}
              onCreated={onCreate}
              // onDeleted={this._onDeleted}
              draw={{
                rectangle: {
                  shapeOptions: {
                    color: "#28c7fa",
                    weight: 5,
                  },
                },
                polygon: {
                  showLength: true,
                  showArea: true,
                  allowIntersection: false,

                  shapeOptions: {
                    color: "#28c7fa",
                    weight: 5,
                  },
                },
                polyline: false,
                marker: false,
                circlemarker: false,
                circle: {
                  shapeOptions: {
                    color: "#28c7fa",
                    weight: 5,
                  },
                },
              }}
            />

            <div>
              {drawnGeoJSON !== null ? (
                <Tooltip
                  direction="bottom"
                  offset={[0, 20]}
                  opacity={1}
                  permanent
                >
                  <p>
                    <span>Area: {"  "}</span>
                    <span style={{ fontWeight: "bold", display: "inline" }}>
                      {drawnGeoJSONProperties && drawnGeoJSONProperties.area
                        ? drawnGeoJSONProperties.area
                        : ""}
                    </span>
                  </p>

                  {drawnGeoJSONProperties && drawnGeoJSONProperties.error ? (
                    <>
                      <hr />

                      <p
                        style={{
                          color: "red",
                          fontStyle: "italic",
                          fontWeight: "bold",
                        }}
                      >
                        {drawnGeoJSONProperties.error}
                      </p>
                      <p></p>
                      <p style={{ color: "red", textAlign: "center" }}>
                        Mission wont be accepted!
                      </p>
                    </>
                  ) : (
                    ""
                  )}
                </Tooltip>
              ) : (
                ""
              )}
            </div>
          </FeatureGroup>
        ) : (
          ""
        )}

        {/*  */}
      </Map>
    </div>
  );
}

export default AirspaceMapComponent;

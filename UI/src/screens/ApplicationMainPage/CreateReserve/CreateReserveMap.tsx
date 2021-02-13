import React, { useEffect, useState, useRef } from "react";
import AirspaceMapComponent from "../../Airspace/AirspaceMapComponent";

// import ReactMapGL from "react-map-gl";

function CreateReserveMap() {
  const [viewport, setViewport] = useState({
    width: "100%",
    height: "80vh",
    latitude: -1.7577,
    longitude: 36.4376,
    zoom: 8,
    mapStyle: "mapbox://styles/mapbox/streets-v11",
    mapboxApiAccessToken: process.env.REACT_APP_mapboxApiAccessToken,
  });

  return (
    <>
      {/* Page Inner  */}

      <AirspaceMapComponent draw={true} />

      <div className="page-footer" style={{ marginBottom: "15px" }}>
        <p>
          Made with <i className="fa fa-heart"></i> by Geoffrey Nyaga
        </p>
      </div>
    </>
  );
}

export default CreateReserveMap;

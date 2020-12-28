import React from "react";
import MapOnly from "../MapOnly";

function Airspace() {
  return (
    <div className="page-inner" style={{ padding: "5px" }}>
      {/* <hr /> */}
      {/* <h3>Airspace</h3> */}
      <div id="main-wrapper"></div>

      <MapOnly />
    </div>
  );
}

export default Airspace;

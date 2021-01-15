import React, { useEffect, useRef, useState } from "react";

import AirspaceMapComponent from "../Map";

function Mapbox6() {
  return (
    <div>
      <AirspaceMapComponent draw={false} />
    </div>
  );
}

export default Mapbox6;

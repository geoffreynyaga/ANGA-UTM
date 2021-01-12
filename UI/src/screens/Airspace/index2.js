/*
 * File: /mnt/c/Projects/ANGA UTM/src/UI/src/screens/Airspace/index2.js
 * Project: MFUKO
 * Author: Geoffrey Nyaga Kinyua  at geoffrey@mfuko.co.ke
 * -----
 * Last Modified: Sunday January 3rd 2021 9:48:34 am
 * Modified By: Geoffrey Nyaga Kinyua at geoffrey@mfuko.co.ke
 * -----
 * This file should not be copied and/or distributed without the express
 * permission of MFUKO PAYMENTS SERVICES Ltd.
 * 
 * Copyright (c) 2021 MFUKO PAYMENTS SERVICES Ltd.
 * -----
 * HISTORY:
 */

import React, { Component } from "react";
import ReactDOM from "react-dom";
import { Map } from "react-leaflet";

import MapboxLayer from "./MapBoxLayer";
import "./styles.css";

const MAPBOX_ACCESS_TOKEN =
  "pk.eyJ1IjoiZ2VvZmZyZXlueWFnYSIsImEiOiJjamdmM3Q5NG4wdnprMnhyMGJqd3U1N25yIn0.R_3l_E-DDVpHQ0rL3zgElQ";

export default class Airspace extends Component {
  state = {
    center: [51.505, -0.091],
    zoom: 13,
  };

  render() {
    return (
      <div>
        <Map center={this.state.center} zoom={this.state.zoom}>
          <MapboxLayer
            accessToken={MAPBOX_ACCESS_TOKEN}
            style="mapbox://styles/mapbox/streets-v9"
          />
        </Map>
      </div>
    );
  }
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);

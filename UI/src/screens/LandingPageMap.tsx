import React from "react";
import MapOnly from "./MapOnly";

function LandingPageMap() {
  return (
    <div className="page-inner">
      <div className="page-title">
        <h3 className="breadcrumb-header">Main Landing Page</h3>
      </div>
      <div id="main-wrapper">
        <div className="row" style={{ marginBottom: "5px" }}>
          <div className="col-lg-3 col-md-6">
            <a href="" className="btn btn-primary">
              Create Flight Plan
            </a>
          </div>
          <div className="col-lg-6 col-md-6">
            {/* <h2>Landing Page </h2> */}
          </div>
          <div className="col-lg-3 col-md-6">
            <a href="" className="btn btn-primary">
              Go To Flight Logs
            </a>
          </div>
        </div>

        <div className="row">
          <div className="col-lg-12 col-md-12">
            <MapOnly />
          </div>
        </div>
      </div>
    </div>
  );
}

export default LandingPageMap;
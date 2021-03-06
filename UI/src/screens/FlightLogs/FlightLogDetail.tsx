import React, { useEffect, useState } from "react";
import AirspaceSingleMapInstanceComponent from "../Airspace/AirspaceSingleMapInstanceComponent";
import { Feature } from "../Airspace/interface";

function FlightLogDetail() {
  const [missionGeojson, setMissionGeojson] = useState<Feature | null>(null);

  useEffect(() => {
    fetchMissionGeoJSON();
  }, []);

  const fetchMissionGeoJSON = async () => {
    console.log("called");
    return fetch(
      `http://localhost:8000/api/applications/v1/reserve-airspaces/${1}/`,
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
      .then((data: Feature) => {
        // console.log("Success: fetchGeoJSON", data);
        setMissionGeojson(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div className="page-inner">
      <hr />
      {/* <h5>Flight Logs Detail</h5> */}
      <div id="main-wrapper">
        <div
          className="row"
          style={{ marginBottom: "20px", paddingBottom: "20x" }}
        >
          <div className="col-sm-4">
            <nav aria-label="breadcrumb" role="navigation">
              <ol className="breadcrumb">
                <li className="breadcrumb-item active" aria-current="page">
                  Log Number:
                </li>
                <span className="pull-right">
                  <b>{missionGeojson?.properties.application_number}</b>
                </span>
              </ol>
            </nav>
          </div>
          <div className="col-sm-4">
            <nav aria-label="breadcrumb" role="navigation">
              <ol className="breadcrumb">
                <li className="breadcrumb-item " aria-current="page">
                  Pilot:
                </li>
                <span className="pull-right">
                  <b>{missionGeojson?.properties.user_full_name}</b>
                </span>
              </ol>
            </nav>
          </div>
          <div className="col-sm-4">
            <a
              className="btn btn-primary btn-xs btn-block"
              href="/flight_plans/logs/11/update"
              role="button"
            >
              <i className="fa fa-pencil-square-o" aria-hidden="true"></i>
              Update log
            </a>
          </div>
        </div>

        <div className="row" style={{ paddingTop: 10, marginTop: 20 }}>
          <div className="col-sm-4">
            <div
              className="panel panel-warning"
              style={{ padding: 5, margin: 0 }}
            >
              <div
                className="panel-heading"
                style={{ backgroundColor: "#FF9800" }}
              >
                <h3
                  className="panel-title"
                  style={{
                    textAlign: "center",
                    color: "white",
                    padding: "5px",
                  }}
                >
                  Overall Details
                </h3>
              </div>
              <div className="panel-body">
                <h6 className="card-subtitle mb-2 text-muted">
                  Organization:
                  <span className="pull-right">
                    <b>{missionGeojson?.properties.user_organization}</b>
                  </span>
                </h6>
                <p className="card-text">
                  Purpose:
                  <span className="pull-right">
                    <b>{missionGeojson?.properties.mission_type_display}</b>
                  </span>
                </p>
                <p className="card-text">
                  Date:
                  <span className="pull-right">
                    <b>{missionGeojson?.properties.start_datetime}</b>
                  </span>
                </p>
                <p className="card-text">
                  Approval:
                  <span className="pull-right">
                    <b>{missionGeojson?.properties.status}</b>
                  </span>
                </p>
              </div>
            </div>
          </div>

          <div className="col-sm-4">
            <div
              className="panel panel-warning"
              style={{ padding: 5, margin: 0 }}
            >
              <div
                className="panel-heading"
                style={{ backgroundColor: "#FF9800" }}
              >
                <h3
                  className="panel-title"
                  style={{
                    textAlign: "center",
                    color: "white",
                    padding: "5px",
                  }}
                >
                  Mission RPAS
                </h3>
              </div>
              <div className="panel-body">
                <h6 className="card-subtitle mb-2 text-muted">
                  RPAS:
                  <span className="pull-right">
                    <b>{missionGeojson?.properties.rpas_name}</b>
                  </span>
                </h6>
                <p className="card-text">
                  Model:
                  <span className="pull-right">
                    <b>{missionGeojson?.properties.rpas_name}</b>
                  </span>
                </p>
                <p className="card-text">
                  Airframe Type:
                  <span className="pull-right">
                    <b>{missionGeojson?.properties.airframe_type}</b>
                  </span>
                </p>
                <p className="card-text">
                  Serial:
                  <span className="pull-right">
                    <b>{missionGeojson?.properties.rpas_serial}</b>
                  </span>
                </p>
                <p className="card-text">
                  Nickname:
                  <span className="pull-right">
                    <b>{missionGeojson?.properties.rpas_name}</b>
                  </span>
                </p>
                <p className="card-text">
                  Manufacturer:
                  <span className="pull-right">
                    <b>{missionGeojson?.properties.rpas_name}</b>
                  </span>
                </p>
              </div>
            </div>
          </div>

          <div className="col-sm-4">
            <div
              className="panel panel-warning"
              style={{ padding: 5, margin: 0 }}
            >
              <div
                className="panel-heading"
                style={{ backgroundColor: "#FF9800" }}
              >
                <h3
                  className="panel-title"
                  style={{
                    textAlign: "center",
                    color: "white",
                    padding: "5px",
                  }}
                >
                  Mission Payload
                </h3>
              </div>
              {/* <!-- TODO: LOG PAYLOAD: if else statement, if unfinished, show link as in list view to complete --> */}
              <div className="panel-body">
                <h6 className="card-subtitle mb-2 text-muted">
                  Payload:
                  <span className="pull-right">
                    <b>{missionGeojson?.properties.rpas_name}</b>
                  </span>
                </h6>
                <p className="card-text">
                  Model:
                  <span className="pull-right">
                    <b>None</b>
                  </span>
                </p>
                <p className="card-text">
                  Model Type:
                  <span className="pull-right">
                    <b></b>
                  </span>
                </p>
                <p className="card-text">
                  Serial:
                  <span className="pull-right">
                    <b>None</b>
                  </span>
                </p>
                <p className="card-text">
                  Nickname:
                  <span className="pull-right">
                    <b></b>
                  </span>
                </p>
                <p className="card-text">
                  Manufacturer:
                  <span className="pull-right">
                    <b></b>
                  </span>
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="row">
          <div className="col-sm-8">
            <div
              className="panel panel-warning"
              style={{ padding: 5, margin: 0 }}
            >
              <div
                className="panel-heading"
                style={{ backgroundColor: "#FF9800" }}
              >
                <h3
                  className="panel-title"
                  style={{
                    textAlign: "center",
                    color: "white",
                    padding: "5px",
                  }}
                >
                  {"Map"}
                </h3>
              </div>
              <div className="panel-body">
                <AirspaceSingleMapInstanceComponent
                  missiongeojson={missionGeojson}
                />
              </div>
            </div>
          </div>
          <div className="col-sm-4">
            <div
              className="panel panel-warning"
              style={{ padding: 5, margin: 0 }}
            >
              <div
                className="panel-heading"
                style={{ backgroundColor: "#FF9800" }}
              >
                <h3
                  className="panel-title"
                  style={{
                    textAlign: "center",
                    color: "white",
                    padding: "5px",
                  }}
                >
                  Pre-flight
                </h3>
              </div>
              {/* <!-- TODO: Pre Flight: if else statement, if unfinished, show link as in list view to complete --> */}

              <div className="panel-body">
                <p className="card-text">
                  Altitude:
                  <span className="pull-right">
                    <b> ft</b>
                  </span>
                </p>
                <p className="card-text">
                  Estimated Flight Time:
                  <span className="pull-right">
                    <b> mins</b>
                  </span>
                </p>
                <p className="card-text">
                  Area Size:
                  <span className="pull-right">
                    <b>{missionGeojson?.properties.area}</b>
                  </span>
                </p>
                <p className="card-text">
                  No. of Flights:
                  <span className="pull-right">
                    <b>1</b>
                  </span>
                </p>
                <p className="card-text">
                  Other Info:
                  <span className="pull-right">
                    <b>None</b>
                  </span>
                </p>
                <p className="card-text">
                  Batt Reminder:
                  <span className="pull-right">
                    <b> %</b>
                  </span>
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="row">
          <div className="col-sm-4">
            <div
              className="panel panel-warning"
              style={{ padding: 5, margin: 0 }}
            >
              <div
                className="panel-heading"
                style={{ backgroundColor: "#FF9800" }}
              >
                <h3
                  className="panel-title"
                  style={{
                    textAlign: "center",
                    color: "white",
                    padding: "5px",
                  }}
                >
                  Emergency Info
                </h3>
              </div>
              {/* <!-- TODO: Emmergency Info: if else statement, if unfinished, show link as in list view to complete --> */}
              <div className="panel-body">
                <p className="card-text">
                  closest Hospital:
                  <span className="pull-right">
                    <b></b>
                  </span>
                </p>
                <p className="card-text">
                  closest Fire Dept:
                  <span className="pull-right">
                    <b></b>
                  </span>
                </p>
                <p className="card-text">
                  closest Police Station:
                  <span className="pull-right">
                    <b></b>
                  </span>
                </p>
                <p className="card-text">
                  Security Service:
                  <span className="pull-right">
                    <b></b>
                  </span>
                </p>
                <p className="card-text">
                  Other:
                  <span className="pull-right">
                    <b></b>
                  </span>
                </p>
              </div>
            </div>
          </div>

          <div className="col-sm-4">
            <div
              className="panel panel-warning"
              style={{ padding: 5, margin: 0 }}
            >
              <div
                className="panel-heading"
                style={{ backgroundColor: "#FF9800" }}
              >
                <h3
                  className="panel-title"
                  style={{
                    textAlign: "center",
                    color: "white",
                    padding: "5px",
                  }}
                >
                  Post-flight
                </h3>
              </div>
              <div className="panel-body">
                <p className="card-text">
                  damages:
                  <span className="pull-right">
                    <b>None</b>
                  </span>
                </p>
                <p className="card-text">
                  Comments:
                  <span className="pull-right">
                    <b>None</b>
                  </span>
                </p>
                <p className="card-text">
                  Success? :
                  <span className="pull-right">
                    <b>False</b>
                  </span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default FlightLogDetail;

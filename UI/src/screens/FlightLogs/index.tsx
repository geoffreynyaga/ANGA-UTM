import React, { useEffect, useState } from "react";

interface FlightLog {
  user_first_name: string;
  user_last_name: string;
  no_of_flights: number;

  reserve_airspace: {
    rpas_name: string | null;
    start_day: string;
    start_time: string;
    end: string;
    application_number: null | string;
    status: number;
    start_datetime: string;
    area: number;
    mission_type_display: string;
  };
  post_flight_completion: number;
  pre_flight_completion: number;
}

function FlightLogsMainPage() {
  const [logs, setLogs] = useState<[FlightLog] | null>(null);
  const fetchLogs = async () => {
    console.log("called");
    return fetch("http://localhost:8000/api/flight_plans/logs/list/", {
      method: "GET", // or 'PUT'
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Authorization: "Token b363791c3baa5ac7b7023f2f2189ea2e6794f820",
      },
      // body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        // console.log("Success:", data);
        setLogs(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  useEffect(() => {
    fetchLogs();
    // return () => {
    //   cleanup
    // }
  }, []);

  const iterationNumber = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  return (
    <div className="page-inner">
      <hr />
      <h5>Flight Logs</h5>

      <div id="main-wrapper">
        <div className="row" style={{ marginBottom: "5px" }}>
          {logs !== null ? (
            logs.map((log, index) => (
              <div
                key={index}
                className="col-lg-3 col-md-3 col-xs-3"
                style={{ paddingBottom: "10x", marginBottom: "10px" }}
              >
                <div
                  className="panel panel-info"
                  style={{ padding: 5, margin: 0 }}
                >
                  <div className="panel-heading">
                    <h3
                      className="panel-title"
                      style={{
                        textAlign: "center",
                        color: "white",
                        padding: "5px",
                      }}
                    >
                      Log No: {log.reserve_airspace.application_number}
                    </h3>
                  </div>
                  <div className="panel-body">
                    <p>Date: {log.reserve_airspace.start_datetime}</p>
                    <p>RPAS Used: {log.reserve_airspace.rpas_name}</p>
                    <p>Purpose: {log.reserve_airspace.mission_type_display}</p>
                    <p>Number of flights: {log.no_of_flights}</p>
                    <p>Area Size: {log.reserve_airspace.area} sq. km </p>
                    <p></p>
                    <small>Pre-Flight Completion</small>
                    <span className="pull-right">
                      {log.pre_flight_completion < 100 ? (
                        <a href="" style={{ color: "blue" }}>
                          <i className="fa fa-external-link" aria-hidden="true">
                            <small> Complete</small>
                          </i>
                        </a>
                      ) : (
                        <i className="fa fa-check" aria-hidden="true">
                          <small> Done</small>
                        </i>
                      )}
                    </span>

                    <div className="progress">
                      <div
                        className="progress-bar progress-bar-info progress-bar-striped "
                        role="progressbar"
                        style={{ width: log.pre_flight_completion + "%" }}
                        aria-valuenow={log.pre_flight_completion}
                        aria-valuemin={0}
                        aria-valuemax={100}
                      ></div>
                    </div>

                    <small> Post-Flight Completion</small>
                    <span className="pull-right">
                      {log.post_flight_completion < 100 ? (
                        <a href="" style={{ color: "blue" }}>
                          <i className="fa fa-external-link" aria-hidden="true">
                            <small> Complete</small>
                          </i>
                        </a>
                      ) : (
                        <i className="fa fa-check" aria-hidden="true">
                          <small> Done</small>
                        </i>
                      )}
                    </span>

                    <div className="progress">
                      <div
                        className="progress-bar progress-bar-info progress-bar-striped"
                        role="progressbar"
                        style={{ width: log.post_flight_completion + "%" }}
                        aria-valuenow={log.post_flight_completion}
                        aria-valuemin={0}
                        aria-valuemax={100}
                      ></div>
                    </div>

                    <small>Approval Status</small>
                    <span className="pull-right">
                      {log.reserve_airspace.status === 0 ? (
                        <i
                          className="fa fa-spinner"
                          aria-hidden="true"
                          style={{ color: "#FF9800" }}
                        >
                          <small> Pending</small>
                        </i>
                      ) : log.reserve_airspace.status === 1 ? (
                        <i
                          className="fa fa-times"
                          aria-hidden="true"
                          style={{ color: "red" }}
                        >
                          <small> Rejected</small>
                        </i>
                      ) : (
                        <i
                          className="fa fa-check"
                          aria-hidden="true"
                          style={{ color: "green" }}
                        >
                          <small> Approved</small>
                        </i>
                      )}
                    </span>
                    <br />
                    <p></p>

                    <div
                      className="row"
                      style={{ paddingLeft: 5, marginRight: 5 }}
                    >
                      <div className="col-xs-6">
                        <a className="btn btn-primary " href="" role="button">
                          <i className="fa fa-eye" aria-hidden="true"></i>
                          View{" "}
                        </a>
                      </div>
                      <div className="col-xs-6">
                        <a className="btn btn-primary " href="" role="button">
                          <i
                            className="fa fa-pencil-square-o"
                            aria-hidden="true"
                          ></i>
                          Update
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <h5>Loading Logs..... </h5>
          )}
        </div>
      </div>
    </div>
  );
}

export default FlightLogsMainPage;

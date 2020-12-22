import React from "react";

function FlightLogsMainPage() {
  const iterationNumber = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  return (
    <div className="page-inner">
      <hr />
      <h5>Flight Logs</h5>

      <div id="main-wrapper">
        <div className="row" style={{ marginBottom: "5px" }}>
          {iterationNumber.map((item, index) => (
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
                    Log No: 2134/56/33
                  </h3>
                </div>
                <div className="panel-body">
                  <p>Date: May 9, 2020, 7:33 a.m.</p>
                  <p>RPAS Used: ebee</p>
                  <p>Purpose: Other</p>
                  <p>Number of flights: 1</p>
                  <p>Area Size: 0.151 sq. km </p>
                  <br />
                  <div className="row" style={{ padding: 0, margin: 0 }}>
                    <div className="col-xs-8" style={{ padding: 0, margin: 0 }}>
                      <p style={{ fontSize: "10px" }}>Pre-Flight Completion</p>
                    </div>
                    <div className="col-xs-4" style={{ padding: 0, margin: 0 }}>
                      <a href="" style={{ fontSize: "10px", color: "blue" }}>
                        Complete {">"}
                      </a>
                    </div>
                  </div>
                  <div className="progress progress-md">
                    <div
                      className="progress-bar progress-bar-info progress-bar-striped"
                      role="progressbar"
                      // aria-valuenow={20}
                      aria-valuemin={0}
                      aria-valuemax={100}
                      style={{ width: "20%" }}
                    >
                      <span className="sr-only">20% Complete</span>
                    </div>
                  </div>
                  <div className="row" style={{ padding: 0, margin: 0 }}>
                    <div className="col-xs-8" style={{ padding: 0, margin: 0 }}>
                      <p style={{ fontSize: "10px" }}>Post-Flight Completion</p>
                    </div>
                    <div className="col-xs-4" style={{ padding: 0, margin: 0 }}>
                      <a href="" style={{ fontSize: "10px", color: "blue" }}>
                        Complete {">"}
                      </a>
                    </div>
                  </div>
                  <div className="progress progress-md">
                    <div
                      className="progress-bar progress-bar-info progress-bar-striped"
                      role="progressbar"
                      // aria-valuenow={20}
                      aria-valuemin={0}
                      aria-valuemax={100}
                      style={{ width: "20%" }}
                    >
                      <span className="sr-only">20% Complete</span>
                    </div>
                  </div>

                  <div className="row" style={{ padding: 0, margin: 0 }}>
                    <div className="col-xs-6" style={{ padding: 0, margin: 0 }}>
                      <p style={{ fontSize: "10px" }}>Approval Status</p>
                    </div>
                    <div className="col-xs-6" style={{ padding: 0, margin: 0 }}>
                      <div className="col-xs-3">
                        <a href="../icon/spinner">
                          <i className="fa fa-spinner" aria-hidden="true"></i>
                        </a>
                      </div>
                      <div className="col-xs-1"></div>
                      <div className="col-xs-8">
                        <p style={{ fontSize: "10px", color: "red" }}>
                          Pending
                        </p>
                      </div>
                    </div>
                  </div>

                  <div
                    className="row"
                    style={{ paddingLeft: 5, marginRight: 5 }}
                  >
                    <div className="col-xs-6">
                      <a href="" className="btn btn-primary">
                        View {">"}
                      </a>
                    </div>
                    <div className="col-xs-6">
                      <a href="" className="btn btn-primary">
                        Update {">"}
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default FlightLogsMainPage;

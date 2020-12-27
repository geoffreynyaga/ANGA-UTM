import React from "react";

function UASList() {
  return (
    <div className="page-inner">
      <hr />
      {/* <h3>My UAS</h3> */}
      <div id="main-wrapper">
        <div className="row">
          <div className="col-sm-4">
            <nav aria-label="breadcrumb" role="navigation">
              <ol className="breadcrumb">
                <li className="breadcrumb-item">
                  <a href="/">Home</a>
                </li>
                <li className="breadcrumb-item active" aria-current="page">
                  My UAS List
                </li>
              </ol>
            </nav>
          </div>
          <div className="col-sm-4">
            <nav aria-label="breadcrumb" role="navigation">
              <ol className="breadcrumb">
                <li>User: {"Geoffrey"}</li>
              </ol>
            </nav>
          </div>
          <div className="col-sm-4">
            <p className="bg-primary">
              <a
                className="btn btn-primary btn-block"
                href="/uas/create/"
                role="button"
              >
                <i className="fa fa-plus-square " aria-hidden="true"></i> Add
                UAS
              </a>
            </p>
          </div>
        </div>
        <p></p>

        <div className="row">
          <div className="col-sm-3">
            <div
              className="panel panel-primary"
              style={{ padding: 5, margin: 0 }}
            >
              <div
                className="panel-heading"
                style={{
                  alignSelf: "center",
                  justifyContent: "center",
                  alignItems: "center",
                }}
              >
                <h3
                  className="panel-title"
                  style={{
                    textAlign: "center",
                    color: "white",
                    padding: "5px",
                  }}
                >
                  motp
                </h3>
              </div>
              <div className="panel-body">
                <br />
                Type: None
                <span className="pull-right"></span>
                <br />
                <p>Serial No: motp/001</p>
                <small>Rpas Model Completion</small>
                <span className="pull-right">
                  <a
                    href="/rpas/rpas-model/2/update/"
                    style={{ color: "#237FCA", textAlign: "center" }}
                  >
                    <i className="fa fa-external-link" aria-hidden="true">
                      <small> Complete</small>
                    </i>
                  </a>
                </span>
                <div className="progress">
                  <div
                    className="progress-bar progress-bar-info progress-bar-striped"
                    role="progressbar"
                    style={{ width: "50.0%" }}
                    aria-valuenow={50.0}
                    aria-valuemin={0}
                    aria-valuemax={100}
                  ></div>
                </div>
                <small>Payload Completion</small>
                <span className="pull-right">
                  <a
                    href="/rpas/payload/2/update/"
                    style={{ color: "#237FCA", textAlign: "center" }}
                  >
                    <i className="fa fa-external-link" aria-hidden="true">
                      <small> Complete</small>
                    </i>
                  </a>
                </span>
                <div className="progress">
                  <div
                    className="progress-bar progress-bar-info progress-bar-striped"
                    role="progressbar"
                    style={{ width: "33.3%" }}
                    aria-valuenow={33.3}
                    aria-valuemin={0}
                    aria-valuemax={100}
                  ></div>
                </div>
              </div>
              <div className="panel-footer">
                <a
                  href="/uas/2/"
                  className="card-link"
                  style={{ color: "#0070E0", textAlign: "center" }}
                >
                  View Details{"  "}
                  <i className="fa fa-external-link" aria-hidden="true"></i>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UASList;

import React from "react";
import PreFlightUpdate from "./PreFlightUpdate";
import PostFlightUpdate from "./PostFlightUpdate";
import EmergencyUpdate from "./EmergencyUpdate";

function FlightLogUpdate() {
  return (
    <div className="page-inner">
      <hr />
      <h5>Flight Log Update</h5>
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
                  <b>{123445}</b>
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
                  <b>{"Geoffrey"}</b>
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

        <div className="row">
          <div className="col-sm-6">
            <div className="panel" style={{ padding: 5, margin: 0 }}>
              <div
                className="panel-heading"
                style={{ backgroundColor: "#318BE5" }}
              >
                <h3
                  className="panel-title"
                  style={{
                    textAlign: "center",
                    color: "white",
                    padding: "5px",
                  }}
                >
                  <b>Detailed updates</b> <em>(Recommended)</em>
                </h3>
              </div>

              <div className="panel-body">
                <ul className="nav nav-pills nav-stacked">
                  <li role="presentation" style={{ paddingLeft: "15px" }}>
                    <a
                      // href="/flight_plans/preflight/11/update"
                      data-toggle="modal"
                      data-target="#preFlightUpdate"
                    >
                      {/* <!-- 11  --> */}
                      <em>Go to {"  "}</em>
                      <b>Pre Flight</b>
                      <span className="pull-right">
                        <i className="fa fa-arrow-right" aria-hidden="true"></i>
                      </span>
                    </a>
                    <PreFlightUpdate />
                  </li>
                  <li role="presentation">
                    <a
                      // href="/flight_plans/postflight/11/update"
                      data-toggle="modal"
                      data-target="#postFlightUpdate"
                    >
                      {/* <!-- 11  --> */}
                      <em>Go to {"  "} </em>
                      <b>Post Flight</b>
                      <span className="pull-right">
                        <i className="fa fa-arrow-right" aria-hidden="true"></i>
                      </span>
                    </a>

                    <PostFlightUpdate />
                  </li>
                  <li role="presentation">
                    <a
                      // href="/flight_plans/emergency-info/11/update"
                      data-toggle="modal"
                      data-target="#emergencyUpdate"
                    >
                      <em> Go to {"  "} </em>
                      <b>Emergency Info</b>
                      <span className="pull-right">
                        <i className="fa fa-arrow-right" aria-hidden="true"></i>
                      </span>
                    </a>
                    <EmergencyUpdate />
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div className="col-sm-6">
            <div className="panel" style={{ padding: 5, margin: 0 }}>
              <div
                className="panel-heading"
                style={{ backgroundColor: "#318BE5" }}
              >
                <h3
                  className="panel-title"
                  style={{
                    textAlign: "center",
                    color: "white",
                    padding: "5px",
                  }}
                >
                  <b>Log Details </b>
                </h3>
              </div>
              <div className="panel-body">
                <form method="POST">
                  <input
                    type="hidden"
                    name="csrfmiddlewaretoken"
                    defaultValue="yaZ2w0JCVlqRWqVemUuG9OQxWpweS6OAwzjGI2dpYa06TPFVixKWy1LOqtRl7hMa"
                  />{" "}
                  <div className="form-group">
                    <label
                      className="control-label"
                      htmlFor="id_emmergency_info"
                    >
                      Emergency info
                    </label>
                    <select
                      name="emmergency_info"
                      className="form-control"
                      title=""
                      id="id_emmergency_info"
                    >
                      <option value="">---------</option>
                      <option value={1} />
                      <option value={2} />
                      <option value={3} />
                      <option value={4} />
                      <option value={5} />
                      <option value={6} />
                      <option value={7} />
                      <option value={8} />
                      <option value={9} />
                      <option value={10} />
                      <option value={11} selected />
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="control-label" htmlFor="id_pre_flight">
                      Pre flight
                    </label>
                    <select
                      name="pre_flight"
                      className="form-control"
                      title=""
                      id="id_pre_flight"
                    >
                      <option value="">---------</option>
                      <option value={1} />
                      <option value={2} />
                      <option value={3} />
                      <option value={4} />
                      <option value={5} />
                      <option value={6} />
                      <option value={7} />
                      <option value={8} />
                      <option value={9} />
                      <option value={10} />
                      <option value={11} selected />
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="control-label" htmlFor="id_post_flight">
                      Post flight
                    </label>
                    <select
                      name="post_flight"
                      className="form-control"
                      title=""
                      id="id_post_flight"
                    >
                      <option value="">---------</option>
                      <option value={1}>None</option>
                      <option value={2}>None</option>
                      <option value={3}>None</option>
                      <option value={4}>None</option>
                      <option value={5}>None</option>
                      <option value={6}>None</option>
                      <option value={7}>None</option>
                      <option value={8}>None</option>
                      <option value={9}>None</option>
                      <option value={10}>None</option>
                      <option value={11} selected>
                        None
                      </option>
                    </select>
                  </div>
                  <p />
                  <button type="submit" className="btn btn-primary ">
                    {" "}
                    Save
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default FlightLogUpdate;

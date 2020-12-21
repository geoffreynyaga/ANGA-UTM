import React from "react";

function ReservesHistory() {
  return (
    <div className="page-inner" style={{ padding: "5px" }}>
      <hr />
      <h3>Reserves History</h3>
      <div id="main-wrapper">
        <div className="row">
          <div className="col-lg-3 col-md-12 col-xs-12">
            <div className="panel panel-success">
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
                  Approved
                </h3>
              </div>
              <div className="panel-body">
                <hr />

                <p>All Approved Flights</p>

                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th>Start Date</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <th scope="row">12th Dec 2020</th>
                      <td>
                        <a href="" className="btn " style={{ color: "blue" }}>
                          Details {">"}
                        </a>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          <div className="col-lg-5 col-md-12 col-xs-12">
            <div className="panel panel-danger" id="js-alerts">
              <div className="panel-heading">
                <h3
                  className="panel-title"
                  style={{
                    textAlign: "center",
                    color: "white",
                    padding: "5px",
                  }}
                >
                  Rejected
                </h3>
              </div>
              <div className="panel-body">
                <hr />
                <p>All Rejected Flights</p>

                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th>Time to start</th>
                      <th>Reason</th>
                      <th></th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <th>3 hours, 11minutes</th>
                      <td>Mark</td>
                      <td>
                        <a href="" className="btn " style={{ color: "blue" }}>
                          View Details {">"}
                        </a>
                      </td>
                      <td>
                        <a href="" style={{ color: "blue" }}>
                          Update {">"}
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <th scope="row">2</th>
                      <td>Jacob</td>
                      <td>
                        <a href="" style={{ color: "blue" }}>
                          View Details {">"}
                        </a>
                      </td>
                      <td>
                        <a href="" style={{ color: "blue" }}>
                          Update {">"}
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <th scope="row">3</th>
                      <td>Larry</td>
                      <td>
                        <a href="" style={{ color: "blue" }}>
                          View Details {">"}
                        </a>
                      </td>
                      <td>
                        <a href="" style={{ color: "blue" }}>
                          Update {">"}
                        </a>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          <div className="col-lg-4 col-md-12 col-xs-12">
            <div className="panel panel-warning">
              <div className="panel-heading">
                <h3
                  className="panel-title"
                  style={{
                    textAlign: "center",
                    color: "white",
                    padding: "5px",
                  }}
                >
                  Pending
                </h3>
              </div>
              <div className="panel-body">
                <hr />

                <p>Pending Approval</p>

                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th>Time to start</th>
                      <th></th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <th scope="row">5 hours, 11minutes</th>

                      <td>
                        <a href="" className="btn " style={{ color: "blue" }}>
                          <span> Details {">"}</span>
                        </a>
                      </td>
                      <td>
                        <a href="" style={{ color: "blue" }}>
                          Update {">"}
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <th scope="row">2</th>
                      <td>
                        <a href="" style={{ color: "blue" }}>
                          Details {">"}
                        </a>
                      </td>
                      <td>
                        <a href="" style={{ color: "blue" }}>
                          Update {">"}
                        </a>
                      </td>
                    </tr>
                    <tr>
                      <th scope="row">3</th>
                      <td>
                        <a href="" style={{ color: "blue" }}>
                          Details {">"}
                        </a>
                      </td>
                      <td>
                        <a href="" style={{ color: "blue" }}>
                          Update {">"}
                        </a>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ReservesHistory;

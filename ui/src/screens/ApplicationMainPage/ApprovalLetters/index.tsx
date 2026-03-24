import React from "react";

function ApprovalLetters() {
  return (
    <div className="page-inner">
      <hr />
      <h3>Approval Letters</h3>
      <div id="main-wrapper">
        <div className="row">
          <div className="col-lg-12 col-md-12 col-xs-12">
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
                  My Approval Letters
                </h3>
              </div>
              <div className="panel-body">
                <hr />
                {/* <p>All Rejected Flights</p> */}

                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th>Approval Number </th>
                      <th>Details</th>
                      <th>Date</th>
                      <th>Status</th>
                      <th>Comments</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <th>mndhd/op/1035</th>
                      <td>
                        <a
                          href=""
                          className="btn btn-default btn-xs"
                          style={{ color: "blue" }}
                        >
                          Open{">"}
                        </a>
                      </td>
                      <td>20th Dec 2020</td>
                      <td>
                        <a
                          href=""
                          className="btn btn-success btn-xs"
                          // style={{ color: "blue" }}
                        >
                          Approved
                        </a>
                      </td>
                      <td>None</td>
                    </tr>

                    <tr>
                      <th>xysdb/op/1896</th>
                      <td>
                        <a
                          href=""
                          className="btn btn-default btn-xs"
                          style={{ color: "blue" }}
                        >
                          Open{">"}
                        </a>
                      </td>
                      <td>10th Dec 2020</td>
                      <td>
                        <a
                          href=""
                          className="btn btn-success btn-xs"
                          // style={{ color: "blue" }}
                        >
                          Approved
                        </a>
                      </td>
                      <td>be cautious of road</td>
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

export default ApprovalLetters;

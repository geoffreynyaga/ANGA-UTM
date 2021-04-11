import React from "react";

function UASDetails() {
  return (
    <div className="page-inner">
      <hr />
      {/* <h3>My UAS</h3> */}
      <div id="main-wrapper">
        <nav aria-label="breadcrumb" role="navigation">
          <ol className="breadcrumb">
            <li className="breadcrumb-item">
              <a href="/">Home</a>
            </li>

            <li className="breadcrumb-item">
              <a href="/uas/list ">My UAS List</a>
            </li>

            <li className="breadcrumb-item active" aria-current="page">
              UAS Details
            </li>
          </ol>
        </nav>

        <div className="panel ">
          <div className="panel-heading">
            <h3 className="panel-title">
              <nav aria-label="breadcrumb" role="navigation">
                <ol className="breadcrumb">
                  <h4>
                    <li className="breadcrumb-item ">
                      <p>None</p>
                    </li>
                    <li className="breadcrumb-item ">{"motp"}</li>
                  </h4>
                </ol>
              </nav>
            </h3>
          </div>
          <div className="panel-body">
            <div className="row">
              <div className="col-sm-4">
                <div className="card">
                  <div className="card-body">
                    <ul>
                      <li> Serial: motp/001 </li>
                      <li> Payload: None </li>
                      <li> Manufacturer: None </li>
                      <li> Payload Manufacturer: </li>
                      <li> Payload Serial: None </li>
                    </ul>
                  </div>
                </div>
              </div>

              <div className="col-sm-3">
                <img
                  className="mw-10"
                  style={{ width: "100%" }}
                  src="/media/images/rpas/2.png"
                  alt="No RPAS Image"
                />
                <div className="">
                  <br />
                </div>
              </div>

              <div className="col-sm-5">
                <div className="card">
                  <div className="card-body">
                    <div className="media">
                      <div className="media-body">
                        <h4 className="media-heading">Manufacturer: None </h4>
                        <p>Country: </p>
                        <br />
                        weight: 1.0 kg
                      </div>
                      <div className="media-right"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="panel-footer">
            <a className="btn btn-primary" href="/uas/2/update/" role="button">
              <i className="fa fa-pencil-square-o" aria-hidden="true"></i>
              Update motp
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UASDetails;

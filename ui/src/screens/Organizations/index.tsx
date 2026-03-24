import React from "react";

function OrganizationsMainScreen() {
  return (
    <div className="page-inner">
      <hr />
      {/* <h3>My UAS</h3> */}
      <div id="main-wrapper">
        <div className="row">
          <div className="col-xs-8">
            <p>Welcome {"Geoffrey"},</p>
          </div>
        </div>

        <div className="row">
          <div className="col-md-4">
            {/* <!-- Widget: user widget style 1 --> */}
            <div
              className="panel panel-primary"
              style={{ padding: 5, margin: 0 }}
            >
              {/* <!-- Add the bg color to the header using any of the bg-* classes --> */}
              <div className="panel-heading">
                <h3
                  className="panel-title"
                  style={{
                    textAlign: "center",
                    color: "white",
                    padding: "5px",
                  }}
                >
                  My Postholds
                </h3>
              </div>
              <div className="panel-body">
                <hr />
                <p>You currently have no approved positions</p>
                <p>Kindly communicate to your company admin to do so</p>
              </div>
            </div>
            {/* <!-- /.widget-user --> */}
          </div>
          {/* <!-- /.col --> */}

          <div className="col-md-4">
            {/* <!-- Widget: user widget style 1 --> */}

            <div
              className="panel panel-primary"
              style={{ padding: 5, margin: 0 }}
            >
              {/* <!-- Add the bg color to the header using any of the bg-* classes --> */}
              <div className="panel-heading">
                <h3
                  className="panel-title"
                  style={{
                    textAlign: "center",
                    color: "white",
                    padding: "5px",
                  }}
                >
                  Flight Logs
                </h3>
              </div>
              <div className="panel-body">
                <ul className="nav nav-stacked">
                  <li>
                    <a href="#">
                      FP/CAA/ROC/1 by geoff
                      <span
                        className="pull-right badge "
                        style={{ backgroundColor: "blue" }}
                      >
                        PENDING
                      </span>
                    </a>
                  </li>

                  <li>
                    <a href="#">
                      FP/CAA/ROC/2 by geoff
                      <span className="pull-right badge bg-blue">PENDING</span>
                    </a>
                  </li>

                  <li>
                    <a href="#">
                      FP/CAA/ROC/3 by geoff
                      <span className="pull-right badge bg-blue">PENDING</span>
                    </a>
                  </li>

                  <li>
                    <a href="#">
                      None by geoff
                      <span className="pull-right badge bg-blue">DENIED</span>
                    </a>
                  </li>

                  <li>
                    <a href="#">
                      None by geoff
                      <span className="pull-right badge bg-blue">PENDING</span>
                    </a>
                  </li>

                  <li>
                    <a href="#">
                      None by geoff
                      <span className="pull-right badge bg-blue">PENDING</span>
                    </a>
                  </li>

                  <li>
                    <a href="#">
                      None by geoff
                      <span className="pull-right badge bg-blue">PENDING</span>
                    </a>
                  </li>

                  <li>
                    <a href="#">
                      None by geoff
                      <span className="pull-right badge bg-blue">APPROVED</span>
                    </a>
                  </li>

                  <li>
                    <a href="#">
                      None by geoff
                      <span className="pull-right badge bg-blue">PENDING</span>
                    </a>
                  </li>

                  <li>
                    <a href="#">
                      None by geoff
                      <span className="pull-right badge bg-blue">PENDING</span>
                    </a>
                  </li>
                </ul>
              </div>
            </div>
            {/* <!-- /.widget-user --> */}
          </div>
          {/* <!-- /.col --> */}

          <div className="col-md-4">
            {/* <!-- Widget: user widget style 1 --> */}
            <div
              className="panel panel-primary"
              style={{ padding: 5, margin: 0 }}
            >
              {/* <!-- Add the bg color to the header using any of the bg-* classes --> */}
              <div className="panel-heading">
                <h3
                  className="panel-title"
                  style={{
                    textAlign: "center",
                    color: "white",
                    padding: "5px",
                  }}
                >
                  Employees
                </h3>
              </div>
              <div className="panel-body">
                <div>
                  <h5>{"Organization 1"}</h5>
                </div>
                <hr />

                <ul className="nav nav-stacked">
                  <li>
                    <a href="#">
                      {"geoff"}
                      <span className="pull-right badge bg-blue"></span>
                    </a>
                  </li>
                </ul>
              </div>
            </div>
            {/* <!-- /.widget-user --> */}
          </div>
          {/* <!-- /.col --> */}
        </div>

        <div className="row">
          {/* <!--  */}
          <div className="pagination">
            <span className="page-links">
              <span className="page-current">Page 1 of 3.</span>

              <a href="/organizations/logs/?page=2">next</a>
            </span>
          </div>
          {/* --> */}
        </div>
      </div>
    </div>
  );
}

export default OrganizationsMainScreen;

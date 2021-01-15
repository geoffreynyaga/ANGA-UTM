import React from "react";
import AirspaceMapComponent from "../../Map";

function CreateReserve() {
  return (
    <div className="page-inner">
      {/* <div className="page-title">
        <h5 className="breadcrumb-header">Create A Reserve</h5>
      </div> */}
      <hr />
      <div id="main-wrapper">
        <div className="row">
          <div
            className="col-lg-8 col-md-12 col-xs-12"
            style={{ marginLeft: "0px" }}
          >
            <AirspaceMapComponent draw={true} />
          </div>
          <div className="col-lg-4 col-md-12 col-xs-12">
            <h4
              style={{
                color: "#0083E6",
                fontWeight: "bold",
                textAlign: "center",
              }}
            >
              Mission Details
            </h4>
            <div className="panel-body">
              <form className="form-horizontal">
                {/* Mission Name */}

                <div className="form-group">
                  <label
                    htmlFor="input-Default"
                    className="col-sm-3 control-label"
                  >
                    Mission Name
                  </label>
                  <div className="col-sm-9">
                    <input
                      type="text"
                      className="form-control"
                      id="input-Default"
                    />
                  </div>
                </div>
                {/* RPAS  */}

                <div className="form-group">
                  <label className="col-sm-3 control-label">RPAS</label>
                  <div className="col-sm-9">
                    <select
                      style={{ marginBottom: "15px" }}
                      className="form-control"
                    >
                      <option>1</option>
                      <option>2</option>
                      <option>3</option>
                      <option>4</option>
                      <option>5</option>
                    </select>
                  </div>
                </div>

                {/* Start Day  */}

                <div className="form-group">
                  <label className="col-sm-3 control-label">Start Date</label>
                  <div className="col-sm-9">
                    <input type="text" className="form-control date-picker" />
                  </div>
                </div>

                {/* Start Time  */}

                <div className="form-group">
                  <label className="col-sm-3 control-label">Start Time</label>
                  <div className="col-sm-9">
                    <div className="input-group input-append bootstrap-timepicker">
                      <input
                        id="timepicker1"
                        type="text"
                        className="form-control"
                      />
                      <span className="input-group-addon add-on">
                        <i className="fa fa-clock-o"></i>
                      </span>
                    </div>
                  </div>
                </div>

                {/* File upload  */}
                <label className="col-sm-3 control-label">Log (optional)</label>
                <div className="col-sm-9">
                  <div className="panel panel-white">
                    <div className="panel-heading clearfix">
                      <h4 className="panel-title">
                        Alternatively, you can upload a mission planner log
                        instead of drawing on the map
                      </h4>
                    </div>
                    <div className="panel-body">
                      <input type="file" id="myfile" name="myfile" />
                    </div>
                  </div>
                </div>

                {/* Submit */}
                <div className="col-sm-12">
                  <button
                    type="submit"
                    className="btn btn-primary "
                    style={{ width: "100%" }}
                  >
                    Submit
                  </button>
                </div>

                <hr />
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CreateReserve;

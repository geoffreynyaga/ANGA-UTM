import React from "react";

function UASCreate() {
  return (
    <div className="page-inner">
      <div className="page-title">
        <div className="row">
          <div className="col-xs-7">
            <div className="panel panel-primary">
              <div
                className="panel-heading"
                style={{
                  alignSelf: "center",
                  justifyContent: "center",
                  alignItems: "center",
                }}
              >
                <h3
                  className="panel-title "
                  style={{
                    textAlign: "center",
                    color: "white",
                    padding: "5px",
                  }}
                >
                  <b>ADD YOUR UAS </b>
                </h3>
              </div>
              <div className="panel-body">
                <form className="" method="POST" encType="multipart/form-data">
                  <input type="hidden" name="csrfmiddlewaretoken" />{" "}
                  <div className="form-group">
                    <label className="control-label" htmlFor="id_organization">
                      Organization
                    </label>
                    <select
                      name="organization"
                      className="form-control"
                      title=""
                      required
                      id="id_organization"
                    >
                      <option value="" selected>
                        ---------
                      </option>

                      <option value="1">CAA/ROC/1</option>
                      <option value="1">CAA/ROC/2</option>
                      <option value="1">CAA/ROC/3</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="control-label" htmlFor="id_rpas_nickname">
                      UAS nickname
                    </label>
                    <input
                      type="text"
                      name="rpas_nickname"
                      maxLength={20}
                      className="form-control"
                      placeholder="Rpas nickname"
                      title="If any....e.g My Phantom Bird"
                      id="id_rpas_nickname"
                    />

                    <div className="help-block">
                      If any....e.g My Phantom Bird
                    </div>
                  </div>
                  <div className="form-group">
                    <label className="control-label" htmlFor="id_rpas_serial">
                      Rpas serial
                    </label>
                    <input
                      type="text"
                      name="rpas_serial"
                      maxLength={20}
                      className="form-control"
                      placeholder="UAS serial"
                      title=""
                      required
                      id="id_rpas_serial"
                    />
                  </div>
                  <div className="form-group">
                    <label className="control-label" htmlFor="id_rpas_pic">
                      UAS pic
                    </label>
                    <div className="row bootstrap3-multi-input">
                      <div className="col-xs-12">
                        <input
                          type="file"
                          name="rpas_pic"
                          accept="image/*"
                          className=""
                          title=""
                          required
                          id="id_rpas_pic"
                        />
                      </div>
                    </div>
                  </div>
                  <p></p>
                  <input
                    type="submit"
                    className="btn btn-primary "
                    value="Save"
                  />
                </form>
              </div>
            </div>
          </div>
          <div className="col-xs-5">
            <div className="panel panel-warning">
              <div
                className="panel-heading"
                style={{
                  alignSelf: "center",
                  justifyContent: "center",
                  alignItems: "center",
                }}
              >
                <span
                  className="pull-left"
                  style={{
                    color: "white",
                    paddingLeft: "5px",
                    marginLeft: "5px",
                  }}
                >
                  <i className="fa fa-info" aria-hidden="true"></i>
                </span>
                <span>
                  <h3
                    className="panel-title text-center"
                    style={{
                      textAlign: "center",
                      color: "white",
                      padding: "5px",
                    }}
                  >
                    <em> Hey, some pointers here</em>
                  </h3>
                </span>
              </div>
              <div className="panel-body">
                <li>Rpas Serial number as found on the drone</li>
                <li>
                  The nickname is whatever name you uniquely give to your drone,
                  its not compulsory
                </li>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UASCreate;

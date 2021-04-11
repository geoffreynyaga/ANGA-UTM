import React from "react";

function UASUpdate() {
  return (
    <div className="page-inner">
      <hr />
      {/* <h3>My UAS</h3> */}
      <div id="main-wrapper">
        <nav aria-label="breadcrumb" role="navigation">
          <ol className="breadcrumb">
            <li className="breadcrumb-item">
              <a href="/uas/">My RPAS</a>
            </li>
            <li className="breadcrumb-item">
              <a href="/uas/2/">motp</a>
            </li>
            <li className="breadcrumb-item active" aria-current="page">
              Update
            </li>
          </ol>
        </nav>
      </div>

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
            className="panel-title text-center"
            style={{
              // textAlign: "center",
              color: "white",
              padding: "5px",
            }}
          >
            <b>RPAS Update </b>
          </h3>
        </div>
        <div className="panel-body">
          <hr />
          <form className="" method="POST" encType="multipart/form-data">
            <div className="form-group">
              <label className="control-label" htmlFor="id_rpas_nickname">
                Rpas nickname
              </label>
              <input
                type="text"
                name="rpas_nickname"
                value="motp"
                maxLength={20}
                className="form-control"
                placeholder="Rpas nickname"
                title="If any....e.g My Phantom Bird"
                id="id_rpas_nickname"
              />

              <div className="help-block">If any....e.g My Phantom Bird</div>
            </div>
            <div className="form-group">
              <label className="control-label" htmlFor="id_organization">
                Organization
              </label>
              <select
                name="organization"
                className="form-control"
                title=""
                id="id_organization"
              >
                <option value="">---------</option>

                <option value="1" selected>
                  CAA/ROC/1
                </option>
              </select>
            </div>
            <div className="form-group">
              <label className="control-label" htmlFor="id_rpas_model">
                Rpas model
              </label>
              <select
                name="rpas_model"
                className="form-control"
                title=""
                id="id_rpas_model"
              >
                <option value="">---------</option>

                <option value="1">None</option>

                <option value="2" selected>
                  None
                </option>
              </select>
            </div>
            <div className="form-group">
              <label className="control-label" htmlFor="id_payload">
                Payload
              </label>
              <select
                name="payload"
                className="form-control"
                title=""
                id="id_payload"
              >
                <option value="">---------</option>

                <option value="1">None</option>

                <option value="2" selected>
                  None
                </option>
              </select>
            </div>
            <div className="form-group">
              <label className="control-label" htmlFor="id_rpas_serial">
                Rpas serial
              </label>
              <input
                type="text"
                name="rpas_serial"
                value="motp/001"
                maxLength={20}
                className="form-control"
                placeholder="Rpas serial"
                title=""
                required
                id="id_rpas_serial"
              />
            </div>
            <div className="form-group">
              <label className="control-label" htmlFor="id_rpas_pic">
                Rpas pic
              </label>
              <div className="row bootstrap3-multi-input">
                <div className="col-xs-12">
                  Currently:
                  <a href="/media/images/rpas/2.png">images/rpas/2.png</a>
                  <br />
                  Change:
                  <input
                    type="file"
                    name="rpas_pic"
                    accept="image/*"
                    className=""
                    title=""
                    id="id_rpas_pic"
                  />
                </div>
              </div>
            </div>
            <p></p>
            <input type="submit" className="btn btn-primary " value="Save" />
          </form>
        </div>
      </div>
    </div>
  );
}

export default UASUpdate;

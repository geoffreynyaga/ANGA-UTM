import React from "react";

function PostFlightUpdate() {
  return (
    <div id="main-wrapper">
      <div className="row">
        <div className="col-md-4">
          <div className="panel-body">
            <div
              className="modal fade"
              id="postFlightUpdate"
              tabIndex={-1}
              role="dialog"
              aria-labelledby="postFlightUpdateLabel"
              aria-hidden="true"
            >
              <div className="modal-dialog">
                <div className="modal-content">
                  <div className="modal-header">
                    <button
                      type="button"
                      className="close"
                      data-dismiss="modal"
                      aria-label="Close"
                    >
                      <span aria-hidden="true">&times;</span>
                    </button>
                    <h4 className="modal-title" id="postFlightUpdateLabel">
                      Post Flight Update
                    </h4>
                  </div>
                  <div className="modal-body">
                    <h4>Lorem Ipsum</h4>
                    Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Aenean commodo ligula eget dolor. Aenean massa. Cum sociis
                    natoque penatibus et magnis dis parturient montes, nascetur
                    ridiculus mus.
                    <br />
                    <br />
                    <hr />
                    <h4>Dolor sit amet</h4>
                    Donec quam felis, ultricies nec, pellentesque eu, pretium
                    quis, sem. Nulla consequat massa quis enim. Donec pede
                    justo, fringilla vel, aliquet nec, vulputate eget, arcu. In
                    enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo.
                    <br />
                    <br />
                    Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Aenean commodo ligula eget dolor.
                  </div>
                  <div className="modal-footer">
                    <button
                      type="button"
                      className="btn btn-info"
                      data-dismiss="modal"
                    >
                      Close
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PostFlightUpdate;

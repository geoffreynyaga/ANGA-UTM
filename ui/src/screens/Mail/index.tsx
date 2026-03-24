import React from "react";

function MailMainScreen() {
  return (
    <div className="page-inner">
      <div id="main-wrapper">
        <div className="row">
          <div className="col-md-12">
            <div className="input-group email-search">
              <input
                type="text"
                className="form-control"
                placeholder="Search for an email"
              />
              <span className="input-group-btn">
                <button className="btn btn-primary" type="button">
                  Search
                </button>
              </span>
            </div>
          </div>
        </div>
        {/* <!-- Row --> */}
        <div className="cross-page-line"></div>
        <div className="row">
          <div className="col-md-2">
            <div className="email-actions">
              <a href="#" className="btn btn-primary compose">
                Compose
              </a>
            </div>
            <div className="email-menu">
              <ul className="list-unstyled">
                <li className="active">
                  <a href="#">
                    <i className="icon-inbox"></i>
                    <span>Inbox</span>
                  </a>
                </li>
                <li>
                  <a href="#">
                    <i className="icon-send"></i>
                    <span>Sent</span>
                  </a>
                </li>
                <li>
                  <a href="#">
                    <i className="icon-mail_outline"></i>
                    <span>Drafts</span>
                  </a>
                </li>
                <li>
                  <a href="#">
                    <i className="icon-error"></i>
                    <span>Spam</span>
                  </a>
                </li>
                <li className="divider"></li>
                <li>
                  <a href="#">
                    <i className="icon-delete"></i>
                    <span>Trash</span>
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="col-md-3">
            <div className="email-list">
              <ul className="list-unstyled">
                <li className="active">
                  <a href="#">
                    <div className="email-list-item">
                      <div className="email-author">
                        <img src="http://via.placeholder.com/35x35" alt="" />
                        <span className="author-name">Kenny Highland</span>
                        <span className="email-date">5m ago</span>
                      </div>
                      <div className="email-info">
                        <span className="email-subject">
                          Maecenas porttitor porta erat ac suscipit porta erat
                          ac suscipit
                        </span>
                        <span className="email-text">
                          Vestibulum placerat imperdiet tellus, et tincidunt
                          eros posuere eget
                        </span>
                      </div>
                    </div>
                  </a>
                </li>
                <li>
                  <a href="#">
                    <div className="email-list-item">
                      <div className="email-author">
                        <img src="http://via.placeholder.com/35x35" alt="" />
                        <span className="author-name">Darrell Price</span>
                        <span className="email-date">2:05pm</span>
                      </div>
                      <div className="email-info">
                        <span className="email-subject">
                          Fusce pretium sem sit amet consectetur dictum
                        </span>
                        <span className="email-text">
                          Suspendisse purus mauris, elementum nec ligula sed
                        </span>
                      </div>
                    </div>
                  </a>
                </li>
                <li>
                  <a href="#">
                    <div className="email-list-item">
                      <div className="email-author">
                        <img src="http://via.placeholder.com/35x35" alt="" />
                        <span className="author-name">Amy Walker</span>
                        <span className="email-date">28 Oct</span>
                      </div>
                      <div className="email-info">
                        <span className="email-subject">
                          Curabitur egestas felis dui, sed dictum lorem maximus
                          et
                        </span>
                        <span className="email-text">
                          Ut ullamcorper elit vitae dolor cursus maximus
                        </span>
                      </div>
                    </div>
                  </a>
                </li>
                <li>
                  <a href="#">
                    <div className="email-list-item">
                      <div className="email-author">
                        <img src="http://via.placeholder.com/35x35" alt="" />
                        <span className="author-name">Kathy Olson</span>
                        <span className="email-date">24 Oct</span>
                      </div>
                      <div className="email-info">
                        <span className="email-subject">
                          Phasellus libero quam, luctus ut purus eget
                        </span>
                        <span className="email-text">
                          Fusce mollis sem nisl, eu rutrum sapien tempus in
                        </span>
                      </div>
                    </div>
                  </a>
                </li>
                <li>
                  <a href="#">
                    <div className="email-list-item">
                      <div className="email-author">
                        <img src="http://via.placeholder.com/35x35" alt="" />
                        <span className="author-name">Susan Mabry</span>
                        <span className="email-date">17 Oct</span>
                      </div>
                      <div className="email-info">
                        <span className="email-subject">
                          Class aptent taciti sociosqu ad litora torquent per
                          conubia nostra
                        </span>
                        <span className="email-text">
                          Pellentesque pellentesque condimentum lectus eget
                          accumsan
                        </span>
                      </div>
                    </div>
                  </a>
                </li>
                <li>
                  <a href="#">
                    <div className="email-list-item">
                      <div className="email-author">
                        <img src="http://via.placeholder.com/35x35" alt="" />
                        <span className="author-name">Richard Lunsford</span>
                        <span className="email-date">16 Oct</span>
                      </div>
                      <div className="email-info">
                        <span className="email-subject">
                          Donec aliquet felis sed ante molestie cursus
                        </span>
                        <span className="email-text">
                          Suspendisse euismod leo at enim accumsan volutpat
                        </span>
                      </div>
                    </div>
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="col-md-7">
            <div className="email-actions">
              <a href="#" className="btn btn-default">
                Reply
              </a>
              <a href="#" className="btn btn-default">
                Forward
              </a>
              <a href="#" className="btn btn-default">
                Mark as read
              </a>
              <a href="#" className="btn btn-danger">
                Delete
              </a>
            </div>
            <div className="email">
              <div className="email-header">
                <div className="email-title">
                  <p>
                    Maecenas porttitor porta erat ac suscipit porta erat ac
                    suscipit
                  </p>
                </div>
                <span className="divider"></span>
                <div className="email-author">
                  <img src="http://via.placeholder.com/35x35" alt="" />
                  <span className="author-name">kenny.high@space.com</span>
                  <span className="email-date">4:14pm</span>
                </div>
                <span className="divider"></span>
              </div>
              <div className="email-body">
                <span>
                  Dear Sir/Madam,
                  <br />
                  <br />
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce
                  ut ante id elit molestie ornare. Pellentesque porttitor
                  facilisis risus, sit amet semper ante efficitur et. Etiam quis
                  rutrum leo, vitae posuere augue. Donec odio leo, dapibus id
                  sollicitudin vel, luctus sit amet justo. Aenean cursus, tellus
                  ut consectetur commodo, est dolor fringilla mauris, nec
                  tristique magna orci in diam. Cras eget libero sit amet felis
                  tincidunt mattis.
                  <br />
                  <br />
                  Waiting your reply ASAP,
                  <br />
                  Thanks in advance.
                </span>
              </div>
              <div className="email-reply">
                <div className="summernote"></div>
              </div>
            </div>
          </div>
        </div>
        {/* <!-- Row --> */}
      </div>
      {/* <!-- Main Wrapper --> */}
      <div className="page-footer">
        <p>
          Made with <i className="fa fa-heart"></i> by stacks
        </p>
      </div>
    </div>
    // {/* <!-- /Page Inner --> */}
  );
}

export default MailMainScreen;

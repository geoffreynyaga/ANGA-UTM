import React from "react";

function Header() {
  return (
    <div className="page-header">
      <div className="search-form">
        <form action="#" method="GET">
          <div className="input-group">
            <input
              type="text"
              name="search"
              className="form-control search-input"
              placeholder="Type something..."
            />
            <span className="input-group-btn">
              <button
                className="btn btn-default"
                id="close-search"
                type="button"
              >
                <i className="icon-close"></i>
              </button>
            </span>
          </div>
        </form>
      </div>
      <nav className="navbar navbar-default">
        <div className="container-fluid">
          {/* New features coming soon .... */}
          <div className="navbar-header">
            <div className="logo-sm">
              <a href="javascript:void(0)" id="sidebar-toggle-button">
                <i className="fa fa-bars"></i>
              </a>
              <a className="logo-box" href="index.html">
                <span>Anga UTM (mobile)</span>
              </a>
            </div>
            <button
              type="button"
              className="navbar-toggle collapsed"
              data-toggle="collapse"
              data-target="#bs-example-navbar-collapse-1"
              aria-expanded="false"
            >
              <i className="fa fa-angle-down"></i>
            </button>
          </div>
          {/* Support the project */}
          <div
            className="collapse navbar-collapse"
            id="bs-example-navbar-collapse-1"
          >
            <ul className="nav navbar-nav">
              <li>
                <a
                  href="javascript:void(0)"
                  id="collapsed-sidebar-toggle-button"
                >
                  <i className="fa fa-bars"></i>
                </a>
              </li>
              <li>
                <a href="javascript:void(0)" id="toggle-fullscreen">
                  <i className="fa fa-expand"></i>
                </a>
              </li>
              <li>
                <a href="javascript:void(0)" id="search-button">
                  <i className="fa fa-search"></i>
                </a>
              </li>
            </ul>
            <ul className="nav navbar-nav navbar-right">
              <li>
                <a
                  href="javascript:void(0)"
                  className="right-sidebar-toggle"
                  data-sidebar-id="main-right-sidebar"
                >
                  <i className="fa fa-envelope"></i>
                </a>
              </li>
              <li className="dropdown">
                <a
                  href="javascript:void(0)"
                  className="dropdown-toggle"
                  data-toggle="dropdown"
                  role="button"
                  aria-haspopup="true"
                  aria-expanded="false"
                >
                  <i className="fa fa-bell"></i>
                </a>
                <ul className="dropdown-menu dropdown-lg dropdown-content">
                  <li className="drop-title">
                    Notifications
                    <a href="#" className="drop-title-link">
                      <i className="fa fa-angle-right"></i>
                    </a>
                  </li>
                  <li className="slimscroll dropdown-notifications">
                    <ul className="list-unstyled dropdown-oc">
                      <li>
                        <a href="#">
                          <span className="notification-badge bg-primary">
                            <i className="fa fa-photo"></i>
                          </span>
                          <span className="notification-info">
                            Finished uploading photos to gallery{" "}
                            <b>South Africa</b>.
                            <small className="notification-date">20:00</small>
                          </span>
                        </a>
                      </li>
                      <li>
                        <a href="#">
                          <span className="notification-badge bg-primary">
                            <i className="fa fa-at"></i>
                          </span>
                          <span className="notification-info">
                            <b>John Doe</b> mentioned you in a post Update v1.5.
                            <small className="notification-date">06:07</small>
                          </span>
                        </a>
                      </li>
                      <li>
                        <a href="#">
                          <span className="notification-badge bg-danger">
                            <i className="fa fa-bolt"></i>
                          </span>
                          <span className="notification-info">
                            4 new special offers from the apps you follow!
                            <small className="notification-date">
                              Yesterday
                            </small>
                          </span>
                        </a>
                      </li>
                      <li>
                        <a href="#">
                          <span className="notification-badge bg-success">
                            <i className="fa fa-bullhorn"></i>
                          </span>
                          <span className="notification-info">
                            There is a meeting with <b>Ethan</b> in 15 minutes!
                            <small className="notification-date">
                              Yesterday
                            </small>
                          </span>
                        </a>
                      </li>
                    </ul>
                  </li>
                </ul>
              </li>
              <li className="dropdown user-dropdown">
                <a
                  href="#"
                  className="dropdown-toggle"
                  data-toggle="dropdown"
                  role="button"
                  aria-haspopup="true"
                  aria-expanded="false"
                >
                  <img
                    src="http://via.placeholder.com/36x36"
                    alt=""
                    className="img-circle"
                  />
                </a>
                <ul className="dropdown-menu">
                  <li>
                    <a href="/profile">Profile</a>
                  </li>
                  <li>
                    <a href="/calendar">Calendar</a>
                  </li>
                  <li>
                    <a href="/mail">
                      <span className="badge pull-right badge-danger">42</span>
                      Messages
                    </a>
                  </li>
                  <li role="separator" className="divider"></li>
                  <li>
                    <a href="#">Account Settings</a>
                  </li>
                  <li>
                    <a href="#">Log Out</a>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
}

export default Header;

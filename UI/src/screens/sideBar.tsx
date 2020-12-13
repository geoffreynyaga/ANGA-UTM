import React from "react";

function SideBar() {
  return (
    <div className="page-sidebar">
      <a className="logo-box" href="/">
        <span>Anga UTM</span>
        <i
          className="icon-radio_button_unchecked"
          id="fixed-sidebar-toggle-button"
        ></i>
        <i className="icon-close" id="sidebar-toggle-button-close"></i>
      </a>
      <div className="page-sidebar-inner">
        <div className="page-sidebar-menu">
          <ul className="accordion-menu">
            <li className="active-page">
              <a href="/applications">
                <i className="menu-icon icon-home4"></i>
                <span>Airspace</span>
              </a>
            </li>
            <li>
              <a href="email.html">
                <i className="menu-icon icon-inbox"></i>
                <span>Flight Logs</span>
              </a>
            </li>
            <li>
              <a href="javascript:void(0)">
                <i className="menu-icon icon-flash_on"></i>
                <span>RPAS</span>
                <i className="accordion-icon fa fa-angle-left"></i>
              </a>
              <ul className="sub-menu">
                <li>
                  <a href="ui-alerts.html">Alerts</a>
                </li>
                <li>
                  <a href="ui-buttons.html">Buttons</a>
                </li>
                <li>
                  <a href="ui-icons.html">Icons</a>
                </li>
                <li>
                  <a href="ui-typography.html">Typography</a>
                </li>
                <li>
                  <a href="ui-notifications.html">Notifications</a>
                </li>
                <li>
                  <a href="ui-modals.html">Modals</a>
                </li>
                <li>
                  <a href="ui-progress.html">Progress Bars</a>
                </li>
                <li>
                  <a href="ui-tabs-accordions.html">Tabs &amp; Accordions</a>
                </li>
                <li>
                  <a href="ui-tree-view.html">Tree View</a>
                </li>
                <li>
                  <a href="ui-nestable.html">Nestable</a>
                </li>
              </ul>
            </li>
            <li>
              <a href="javascript:void(0)">
                <i className="menu-icon icon-layers"></i>
                <span>Organization</span>
                <i className="accordion-icon fa fa-angle-left"></i>
              </a>
              <ul className="sub-menu">
                <li>
                  <a href="layout-blank.html">Blank Page</a>
                </li>
                <li>
                  <a href="layout-boxed.html">Boxed Layout</a>
                </li>
                <li>
                  <a href="layout-collapsed-sidebar.html">Collapsed Sidebar</a>
                </li>
                <li>
                  <a href="layout-fixed-header.html">Fixed Header</a>
                </li>
                <li>
                  <a href="layout-fixed-sidebar.html">Fixed Sidebar</a>
                </li>
                <li>
                  <a href="layout-fixed-sidebar-header.html">
                    Fixed Sidebar &amp; Header
                  </a>
                </li>
              </ul>
            </li>
            <li>
              <a href="javascript:void(0)">
                <i className="menu-icon icon-code"></i>
                <span>Calendar</span>
                <i className="accordion-icon fa fa-angle-left"></i>
              </a>
              <ul className="sub-menu">
                <li>
                  <a href="form-elements.html">Elements</a>
                </li>
                <li>
                  <a href="form-wizard.html">Form Wizard</a>
                </li>
                <li>
                  <a href="form-file-upload.html">File Upload</a>
                </li>
                <li>
                  <a href="form-image-crop.html">Image Crop</a>
                </li>
                <li>
                  <a href="form-image-zoom.html">Image Zoom</a>
                </li>
                <li>
                  <a href="form-x-editable.html">X-editable</a>
                </li>
              </ul>
            </li>
            <li>
              <a href="javascript:void(0)">
                <i className="menu-icon icon-format_list_bulleted"></i>
                <span>MailBox</span>
                <i className="accordion-icon fa fa-angle-left"></i>
              </a>
              <ul className="sub-menu">
                <li>
                  <a href="table-static.html">Static</a>
                </li>
                <li>
                  <a href="table-responsive.html">Responsive</a>
                </li>
                <li>
                  <a href="table-data.html">Data Tables</a>
                </li>
              </ul>
            </li>
            <li>
              <a href="charts.html">
                <i className="menu-icon icon-show_chart"></i>
                <span>Regulations</span>
              </a>
            </li>
            <li>
              <a href="javascript:void(0)">
                <i className="menu-icon icon-my_location"></i>
                <span>Maps</span>
                <i className="accordion-icon fa fa-angle-left"></i>
              </a>
              <ul className="sub-menu">
                <li>
                  <a href="maps-google.html">Google</a>
                </li>
                <li>
                  <a href="maps-vector.html">Vector</a>
                </li>
              </ul>
            </li>
            <li>
              <a href="javascript:void(0)">
                <i className="menu-icon icon-star"></i>
                <span>Extra</span>
                <i className="accordion-icon fa fa-angle-left"></i>
              </a>
              <ul className="sub-menu">
                <li>
                  <a href="invoice.html">Invoice</a>
                </li>
                <li>
                  <a href="404.html">404 Page</a>
                </li>
                <li>
                  <a href="500.html">500 Page</a>
                </li>
                <li>
                  <a href="profile.html">Profile</a>
                </li>
                <li>
                  <a href="login.html">Login</a>
                </li>
                <li>
                  <a href="register.html">Register</a>
                </li>
                <li>
                  <a href="lockscreen.html">Lockscreen</a>
                </li>
                <li>
                  <a href="todo.html">Todo</a>
                </li>
                <li>
                  <a href="gallery.html">Gallery</a>
                </li>
                <li>
                  <a href="pricing-tables.html">Pricing Tables</a>
                </li>
                <li>
                  <a href="timeline.html">Timeline</a>
                </li>
              </ul>
            </li>
            <li className="menu-divider"></li>
            <li>
              <a href="index.html">
                <i className="menu-icon icon-help_outline"></i>
                <span>Regulations</span>
              </a>
            </li>
            <li>
              <a href="index.html">
                <i className="menu-icon icon-public"></i>
                <span>Updates</span>
                <span className="label label-danger">1.0</span>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default SideBar;

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
                <i className="menu-icon icon-my_location"></i>

                <span>Airspace</span>
              </a>
            </li>
            <li>
              <a href="/flight-plans/logs">
                <i className="menu-icon icon-archive"></i>

                <span>Flight Logs</span>
              </a>
            </li>
            <li>
              <a href="/uas">
                <i className="menu-icon icon-flash_on"></i>
                <span>UAS</span>
                <i className="accordion-icon fa fa-angle-left"></i>
              </a>
              <ul className="sub-menu">
                <li>
                  <a href="/uas">UAS Main Page</a>
                </li>
                <li>
                  <a href="/uas/list">View All</a>
                </li>
                <li>
                  <a href="/uas/create">Create</a>
                </li>
                <li>
                  <a href="/uas/register">Register</a>
                </li>
              </ul>
            </li>
            <li>
              <a href="/organizations">
                <i className="menu-icon icon-home"></i>

                <span>Organization</span>
              </a>
            </li>
            <li>
              <a href="/calendar">
                <i className="menu-icon icon-calendar"></i>
                <span>Calendar</span>
              </a>
            </li>
            <li>
              <a href="/mail">
                <i className="menu-icon icon-inbox"></i>
                <span>MailBox</span>
                <i className="accordion-icon fa fa-angle-left"></i>
              </a>
              <ul className="sub-menu">
                <li>
                  <a href="/mail">All Mail</a>
                </li>
                <li>
                  <a href="/mail/inbox">Inbox</a>
                </li>
                <li>
                  <a href="/mail/sent">Sent</a>
                </li>
              </ul>
            </li>

            <li className="menu-divider"></li>
            <li>
              <a href="charts.html">
                <i className="menu-icon icon-gavel"></i>
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

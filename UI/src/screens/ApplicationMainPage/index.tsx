import React from "react";
import MainPageCategoryItem from "./MainPageCategoryItem";

function ApplicationMainPage() {
  return (
    <div className="page-inner">
      <div className="page-title">
        <h3 className="breadcrumb-header">Airspace Page</h3>
      </div>
      <div id="main-wrapper">
        <div className="row" style={{ marginBottom: "5px" }}>
          <MainPageCategoryItem lgWidth={6} mdWidth={6} />
          <div className="col-lg-6 col-md-6">
            <div className="panel panel-white stats-widget">
              <div className="panel-body">
                <div className="pull-left">
                  <span className="stats-number">$781,876</span>
                  <p className="stats-info">Total Income</p>
                </div>
                <div className="pull-right">
                  <i className="icon-arrow_upward stats-icon"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="row" style={{ marginBottom: "5px" }}>
          <div className="col-lg-6 col-md-6">
            <div className="panel panel-white stats-widget">
              <div className="panel-body">
                <div className="pull-left">
                  <span className="stats-number">$781,876</span>
                  <p className="stats-info">Total Income</p>
                </div>
                <div className="pull-right">
                  <i className="icon-arrow_upward stats-icon"></i>
                </div>
              </div>
            </div>
          </div>
          <div className="col-lg-6 col-md-6">
            <div className="panel panel-white stats-widget">
              <div className="panel-body">
                <div className="pull-left">
                  <span className="stats-number">$781,876</span>
                  <p className="stats-info">Total Income</p>
                </div>
                <div className="pull-right">
                  <i className="icon-arrow_upward stats-icon"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ApplicationMainPage;

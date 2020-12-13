import React from "react";

function MainPageCategoryItem(props: any) {
  return (
    <div className={`col-lg-${props.lgWidth} col-md-${props.mdWidth}`}>
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
  );
}

export default MainPageCategoryItem;

import React from "react";
import { Link, Route, Switch, useRouteMatch } from "react-router-dom";
import CreateReserve from "./CreateReserve/CreateReserve";
import MainPageCategoryItem from "./MainPageCategoryItem";

function ApplicationMainPage() {
  let { path, url } = useRouteMatch();
  return (
    <div className="page-inner">
      <div className="page-title">
        <h3 className="breadcrumb-header">Airspace Tools</h3>
      </div>
      <div id="main-wrapper">
        <div className="row" style={{ marginBottom: "5px" }}>
          <Link to={`${url}/create`}>
            <MainPageCategoryItem
              lgWidth={6}
              mdWidth={6}
              title="Apply for a Reserve "
              subTitle="Apply"
              backgroundColor="#00C0EF"
            />
          </Link>
          <Link to={`${path}/history`}>
            <MainPageCategoryItem
              lgWidth={6}
              mdWidth={6}
              title="My Reserves History "
              subTitle="View All"
              backgroundColor="#00A65A"
            />
          </Link>
        </div>

        <div className="row" style={{ marginBottom: "5px" }}>
          <Link to={`${path}/approval-letters`}>
            <MainPageCategoryItem
              lgWidth={6}
              mdWidth={6}
              title="Approval Letters "
              subTitle="View All"
              backgroundColor="#DD4B39"
            />
          </Link>
          <Link to={`${url}/airspace`}>
            <MainPageCategoryItem
              lgWidth={6}
              mdWidth={6}
              title="View Airspace "
            />
          </Link>
        </div>
      </div>
    </div>
  );
}

export default ApplicationMainPage;

import React from "react";
import { Link, useRouteMatch } from "react-router-dom";
import MainPageCategoryItem from "../screens/ApplicationMainPage/MainPageCategoryItem";

function UASMainPage() {
  let { path, url } = useRouteMatch();

  return (
    <div className="page-inner">
      <div className="page-title">
        <h3 className="breadcrumb-header">Airspace Tools</h3>
      </div>
      <div id="main-wrapper">
        <div className="row" style={{ marginBottom: "5px" }}>
          <Link to={`${path}/list`}>
            <MainPageCategoryItem
              lgWidth={6}
              mdWidth={6}
              title="MY UAS "
              subTitle="View All"
              backgroundColor="#00C0EF"
            />
          </Link>
          <Link to={`${path}/create`}>
            <MainPageCategoryItem
              lgWidth={6}
              mdWidth={6}
              title="Create"
              //   subTitle="View All"
              backgroundColor="#00A65A"
            />
          </Link>
        </div>

        <div className="row" style={{ marginBottom: "5px" }}>
          <Link to={`${path}/register`}>
            <MainPageCategoryItem
              lgWidth={6}
              mdWidth={6}
              title="Register "
              //   subTitle="For new UAS"
              backgroundColor="#DD4B39"
            />
          </Link>
          <Link to={`${path}/update`}>
            <MainPageCategoryItem lgWidth={6} mdWidth={6} title="Update " />
          </Link>
        </div>
      </div>
    </div>
  );
}

export default UASMainPage;

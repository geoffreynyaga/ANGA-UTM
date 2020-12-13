import React from "react";

import SideBar from "./sideBar";
import LandingPageMap from "./LandingPageMap";
import Header from "./Header";
import { Route, Switch } from "react-router-dom";
function LandingPage() {
  return (
    <>
      <SideBar />

      <div className="page-content">
        {/* Page Header */}
        <Header />

        <Switch>
          <Route exact path="/">
            <LandingPageMap />
          </Route>
          <Route exact path="/applications">
            {/* <ApplicationMainPage /> */}
            <LandingPageMap />
          </Route>
        </Switch>
      </div>
    </>
  );
}

export default LandingPage;

import React from "react";

import SideBar from "./sideBar";
import LandingPageMap from "./LandingPageMap";
import Header from "./Header";
import { Route, Switch } from "react-router-dom";
import ApplicationMainPage from "./ApplicationMainPage";
import CreateReserve from "./ApplicationMainPage/CreateReserve/CreateReserve";
import ReservesHistory from "./ApplicationMainPage/ReservesHistory";
import ApprovalLetters from "./ApplicationMainPage/ApprovalLetters";
import Airspace from "./ApplicationMainPage/Airspace";
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
            <ApplicationMainPage />
          </Route>
          <Route path="/applications/create">
            <CreateReserve />
          </Route>
          <Route path="/applications/history">
            <ReservesHistory />
          </Route>
          <Route path="/applications/approval-letters">
            <ApprovalLetters />
          </Route>
          <Route path="/applications/airspace">
            <Airspace />
          </Route>
        </Switch>
      </div>
    </>
  );
}

export default LandingPage;

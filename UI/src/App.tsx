import React from "react";

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import AuthScreen from "./screens/AuthScreen";
import SignUp from "./authentication/SignUp";

function App() {
  return (
    <Router>
      <div className="page-container">
        <Switch>
          <Route exact path="/signup">
            <SignUp />
          </Route>
          <Route path="/">
            <AuthScreen />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;

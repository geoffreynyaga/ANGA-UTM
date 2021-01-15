import React from "react";

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import SignUp from "./authentication/SignUp";

import AuthScreen from "./screens/AuthScreen";

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

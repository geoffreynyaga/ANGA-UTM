import React, { useEffect, useState } from "react";
import Login from "../authentication/Login";
import LandingPage from "./LandingPage";

function AuthScreen() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState<null | string>(null);

  const getToken = async () => {
    //   await fetch
    return "";
  };

  useEffect(() => {
    getToken().then((result) => {
      if (result !== null && result !== "") {
        setToken(result);
        setIsAuthenticated(true);
      } else {
        setIsAuthenticated(false);
      }
    });
  }, [token]);
  return (
    <div className="page-container">
      {isAuthenticated ? <Login /> : <LandingPage />}
    </div>
  );
}

export default AuthScreen;

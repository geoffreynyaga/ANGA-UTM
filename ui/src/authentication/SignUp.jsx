import React, { useState } from "react";
import { Link } from "react-router-dom";

function SignUp() {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function handleSignUp(e) {
    e.preventDefault;
    alert("Hi");
    console.log("sign Up");
  }
  return (
    <div style={{ width: "100%", backgroundColor: "white" }}>
      <div className="login-page">
        <div id="main-wrapper" className="container-fluid">
          <div className="row">
            <div className="col-sm-6 col-md-3 login-box">
              <h4 className="login-title">Create an account</h4>
              <form onSubmit={handleSignUp}>
                <div className="form-group">
                  <label htmlFor="exampleInputFirstName">First name</label>
                  <input
                    type="text"
                    className="form-control"
                    id="exampleInputFirstName"
                    value={firstName}
                    onChange={(e) => {
                      setFirstName(e.target.value);
                    }}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="exampleInputLastName">Last name</label>
                  <input
                    type="text"
                    className="form-control"
                    id="exampleInputLastName"
                    value={lastName}
                    onChange={(e) => {
                      setLastName(e.target.value);
                    }}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="exampleInputEmail">Email address</label>
                  <input
                    type="email"
                    className="form-control"
                    id="exampleInputEmail"
                    value={email}
                    onChange={(e) => {
                      setEmail(e.target.value);
                    }}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="exampleInputPassword">Password</label>
                  <input
                    type="password"
                    className="form-control"
                    id="exampleInputPassword"
                    value={password}
                    onChange={(e) => {
                      setPassword(e.target.value);
                    }}
                  />
                </div>
                <button className="btn btn-primary" type="submit">
                  Register
                </button>
              </form>

              <hr />
              <p>Already have an account </p>
              <br />
              <Link to="/login">
                <button className="btn btn-default">Login</button>
              </Link>

              <br />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SignUp;

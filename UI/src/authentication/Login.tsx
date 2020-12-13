import React from "react";

// import { Link } from "react-router-dom";

function Login() {
  return (
    // <div>
    //   <p>Login Page</p>
    //   <input value="" placeholder="Username/email" />
    //   <br />
    //   <br />

    //   <input value="" placeholder="Password" />
    //   <br />
    //   <br />

    //   <button>Submit</button>
    //   <hr></hr>
    //   <br />

    //   <p>No account?</p>
    //   <br />

    //   <Link to="/signup">Sign Up here</Link>
    // </div>

    <div style={{ width: "100%", backgroundColor: "white" }}>
      <div className="login-page">
        <div className="row">
          <div className="col-sm-6 col-md-6 login-box">
            <h4 className="login-title">Sign in to your account</h4>
            <form>
              <div className="form-group">
                <label htmlFor="exampleInputEmail1">Email address</label>
                <input
                  type="email"
                  className="form-control"
                  id="exampleInputEmail1"
                />
              </div>
              <div className="form-group">
                <label htmlFor="exampleInputPassword1">Password</label>
                <input
                  type="password"
                  className="form-control"
                  id="exampleInputPassword1"
                />
              </div>
              <a href="index.html" className="btn btn-primary">
                Login
              </a>
              <br />
              <a
                href="/forgot-password"
                className="forgot-link"
                style={{ color: "blue" }}
              >
                Forgot password?
              </a>
              <hr />
              <a href="/signup" className="btn btn-default">
                Register
              </a>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;

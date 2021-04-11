import React, { useEffect, useState } from "react";

interface UserProfile {
  full_name: string;
  username: string;
  phone_number: string;
  bio: string;
  location: string;
  birth_date: null | string;
  profile_pic: string;
  organization: {
    organization_details: {
      name: string;
      city: string;
      website: string;
      logo: string;
    };
    caa_no: string;
  };
}

interface ReserveAirspace {
  id: number;
  date_created: string;
  application_number: null | string;
}

interface UAS {
  id: number;
  rpas_serial: string;
  rpas_nickname: string;
}

function ProfileMainPage() {
  const [logs, setLogs] = useState<[ReserveAirspace] | null>(null);
  const [userProfileData, setUserProfileData] = useState<UserProfile | null>(
    null
  );
  const [uas, setUAS] = useState<[UAS] | null>(null);

  const fetchUserProfile = async (pk: number) => {
    console.log("called");
    return fetch(`http://localhost:8000/api/accounts/profile/${pk}/`, {
      method: "GET", // or 'PUT'
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Authorization: "Token b363791c3baa5ac7b7023f2f2189ea2e6794f820",
      },
      // body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        // console.log("fetchUserProfile:", data);
        setUserProfileData(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const fetchLogs = async (pk: number) => {
    console.log("called");
    return fetch(`http://localhost:8000/api/accounts/profile/${pk}/logs/`, {
      method: "GET", // or 'PUT'
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Authorization: "Token b363791c3baa5ac7b7023f2f2189ea2e6794f820",
      },
      // body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        // console.log("fetchLogs:", data);
        setLogs(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const fetchUAS = async (pk: number) => {
    console.log("called");
    return fetch(`http://localhost:8000/api/accounts/profile/${pk}/uas/`, {
      method: "GET", // or 'PUT'
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Authorization: "Token b363791c3baa5ac7b7023f2f2189ea2e6794f820",
      },
      // body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        // console.log("fetchUAS:", data);
        setUAS(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  useEffect(() => {
    fetchUserProfile(1);
    fetchLogs(1);
    fetchUAS(1);
  }, []);
  return (
    <div className="page-inner">
      <hr />
      {/* <h5>Flight Logs Detail</h5> */}
      <div id="main-wrapper"></div>
      <div className="content-header">
        <h5>
          Hey <b>{userProfileData?.full_name}</b>,
          <small> Welcome To Your Profile!</small>{" "}
        </h5>
      </div>

      <div className="row">
        <div className="col-lg-4 col-md-4 col-sm-12">
          <div
            className="panel panel-default"
            style={{ padding: 5, margin: 10 }}
          >
            <div className="panel-body">
              <div className="media-center">
                <img
                  className="img-responsive"
                  src={userProfileData?.profile_pic}
                  alt="Profile Pic Missing!"
                />
              </div>
              <hr />
              <h4 className="card-title">{userProfileData?.full_name}</h4>
              <h6 className="card-title">
                Phone No: {userProfileData?.phone_number}
              </h6>
              <p className="card-text">
                Bio: {userProfileData?.bio}
                <p></p>
              </p>
            </div>

            <div className="panel-footer">
              <a
                className="btn btn-primary"
                href="/account/profile/1/update/"
                role="button"
              >
                <i className="fa fa-user-o" aria-hidden="true"></i>
                Edit Profile
              </a>
            </div>
          </div>
        </div>
        {/* <p></p> */}
        {/* <!-- To give spacing to next card in mobile --> */}

        <div className="col-lg-4 col-md-4 col-sm-12">
          {/* MY Flight Logs  */}

          <div className="list-group">
            <a href="" className="list-group-item active">
              My Flight Logs
            </a>

            <li className="list-group-item">
              <small> Includes Flights even as co-pilot</small>
            </li>

            {logs !== null ? (
              logs.map((log, index) => (
                <li key={log.id} className="list-group-item">
                  <span className="badge">{log.date_created}</span>
                  <a href="/flight_plans/logs/1/">
                    {log.application_number ? log.application_number : "None"}
                  </a>
                </li>
              ))
            ) : (
              <p>No logs</p>
            )}
          </div>

          {/* MY UAS  */}
          <div className="list-group">
            <a href="" className="list-group-item active">
              My UAS
            </a>
            <li className="list-group-item">
              <small> Includes All Rpas by your Organization</small>
            </li>
            {uas !== null ? (
              uas.map((ua) => (
                <li className="list-group-item" key={ua.id}>
                  <span className="badge">{ua.rpas_serial}</span>
                  <a href="/rpas/2/"> {ua.rpas_nickname}</a>
                </li>
              ))
            ) : (
              <p>no UAS</p>
            )}
          </div>

          {/* FLIGHTS  */}

          <div className="list-group">
            <a href="" className="list-group-item active">
              Flights
            </a>
            <a href="#" className="list-group-item">
              <i className="fa fa-clock-o" aria-hidden="true"></i>
              Total Hours: xx
            </a>
            <a href="#" className="list-group-item">
              <i className="fa fa-plane" aria-hidden="true"></i>
              Rated Aircrafts: xx
            </a>
            <a href="#" className="list-group-item">
              <i className="fa fa-certificate" aria-hidden="true"></i>
              Certificates: xx
            </a>
          </div>
        </div>

        <div className="col-lg-4 col-md-4 col-sm-12">
          {/* Info */}
          <div className="list-group">
            <a href="" className="list-group-item active">
              Info
            </a>
            <li className="list-group-item">
              Username: {userProfileData?.username}
            </li>
            <li className="list-group-item">
              <i className="fa fa-map-marker" aria-hidden="true"></i>
              Location: {userProfileData?.location}
            </li>
            {/* <li className="list-group-item">
              <i className="fa fa-calendar" aria-hidden="true"></i>
              Birth Date: {userProfileData?.birth_date}
            </li> */}
          </div>

          {/* Organization */}
          <div className="list-group">
            <a href="" className="list-group-item active">
              Organization
            </a>
            <li className="list-group-item">
              <i className="fa fa-building" aria-hidden="true"></i>
              Company: {userProfileData?.organization.organization_details.name}
            </li>
            <li className="list-group-item">
              <i className="fa fa-certificate" aria-hidden="true"></i>
              ROC No: {userProfileData?.organization.caa_no}
            </li>
            <li className="list-group-item">
              <i className="fa fa-map-marker" aria-hidden="true"></i>
              Location:{" "}
              {userProfileData?.organization.organization_details.city}
              <p></p>
            </li>

            <a
              href={userProfileData?.organization.organization_details.website}
              className="list-group-item "
            >
              <i className="fa fa-external-link" aria-hidden="true"></i>
              {userProfileData?.organization.organization_details.website}
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProfileMainPage;

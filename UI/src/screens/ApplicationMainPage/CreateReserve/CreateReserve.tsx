import React, { useEffect, useState } from "react";
import { DatePicker, TimePicker } from "antd";
import moment from "moment";

import { Upload, message } from "antd";
import { CloudUploadOutlined } from "@ant-design/icons";

import AirspaceMapComponent from "../../Airspace/AirspaceMapComponent";

interface MyUASInterface {
  id: number;
  rpas_name: string;
}

const { Dragger } = Upload;

const props = {
  name: "file",
  multiple: true,
  action: "https://www.mocky.io/v2/5cc8019d300000980a055e76",
  onChange(info: any) {
    const { status } = info.file;
    if (status !== "uploading") {
      console.log(info.file, info.fileList);
    }
    if (status === "done") {
      message.success(`${info.file.name} file uploaded successfully.`);
    } else if (status === "error") {
      message.error(`${info.file.name} file upload failed.`);
    }
  },
};

function CreateReserve() {
  const [missionName, setMissionName] = useState("");
  const [rpas, setRpas] = useState<any | number | null>(null);
  const [myUASList, setMyUASList] = useState<MyUASInterface[] | null>(null);

  const [dateTimeValue, setDateTimeValue] = useState<Date | null>(null);
  const [timeString, setTimeString] = useState<string | null>(null);
  const [dateString, setDateString] = useState<string | null>(null);

  useEffect(() => {
    //
    fetchUserUAS();
  }, []);

  const fetchUserUAS = async () => {
    console.log("called");
    return fetch("http://localhost:8000/api/rpas/v1/my-rpas/list/", {
      method: "GET", // or 'PUT'
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Authorization: "Token b363791c3baa5ac7b7023f2f2189ea2e6794f820",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // console.log("Success: fetchUserUAS", data);
        setMyUASList(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  function handleMissionNameInput(e: any) {
    e.preventDefault();
    setMissionName(e.target.value);
  }
  function handleRPASSelection(e: any) {
    e.preventDefault();
    setRpas(e.target.value);
  }
  function handleStartDateInput(e: any) {
    e.preventDefault();
    setMissionName(e.target.value);
  }
  function handleStartTimeInput(e: any) {
    e.preventDefault();
    setMissionName(e.target.value);
  }
  function handleLogInput(e: any) {
    e.preventDefault();
    setMissionName(e.target.value);
  }

  function handleSubmit(e: any) {
    e.preventDefault();
    setMissionName(e.target.value);
  }

  // function handleDateChange(date: any) {
  //   setValue(JSON.stringify(date));
  // }

  return (
    <div className="page-inner">
      <hr />

      <pre>
        dateTimeValue:{" "}
        {dateTimeValue ? JSON.stringify(dateTimeValue) : "no date"}
      </pre>
      <pre>
        {dateTimeValue ? JSON.stringify(new Date(dateTimeValue)) : "no date"}
      </pre>

      <pre>newDate: {JSON.stringify(new Date())}</pre>

      <div id="main-wrapper">
        <div className="row">
          {/*  */}
          <div
            className="col-lg-8 col-md-12 col-xs-12"
            style={{ marginLeft: "0px" }}
          >
            <AirspaceMapComponent draw={true} />
          </div>
          {/*  */}
          <div className="col-lg-4 col-md-12 col-xs-12">
            <h4
              style={{
                color: "#0083E6",
                fontWeight: "bold",
                textAlign: "center",
              }}
            >
              Mission Details
            </h4>
            <div className="panel-body">
              <form className="form-horizontal" onSubmit={handleSubmit}>
                {/* Mission Name */}

                <div className="form-group">
                  <label
                    htmlFor="input-Default"
                    className="col-sm-3 control-label"
                  >
                    Mission Name
                  </label>
                  <div className="col-sm-9">
                    <input
                      type="text"
                      className="form-control"
                      maxLength={140}
                      placeholder={"Mission Name"}
                      id={"reserve_name"}
                      required={true}
                      onChange={handleMissionNameInput}
                    />
                  </div>
                </div>
                {/* RPAS  */}

                <div className="form-group">
                  <label className="col-sm-3 control-label">RPAS</label>
                  <div className="col-sm-9">
                    <select
                      style={{ marginBottom: "15px" }}
                      className="form-control"
                      required={true}
                      onChange={handleRPASSelection}
                    >
                      <option value="" selected={rpas ? false : true}>
                        ---------
                      </option>

                      {myUASList !== null &&
                        myUASList.map((myUAS, index) => (
                          <option key={myUAS.id} value={myUAS.id}>
                            {myUAS.rpas_name}
                          </option>
                        ))}
                    </select>
                  </div>
                </div>

                {/* Start Day  */}

                <div className="form-group">
                  <label className="col-sm-3 control-label">Start Date</label>
                  <div className="col-sm-9">
                    <input
                      type="text"
                      className="form-control date-picker"
                      required={true}
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="col-sm-3 control-label">Start Date</label>
                  <div className="col-sm-9" style={{ zIndex: 9999 }}>
                    <DatePicker
                      onChange={(moment, dateString) => {
                        console.log(dateString, "dateString");
                        setDateString(dateString);
                      }}
                    />
                  </div>
                </div>

                {/* Start Time  */}

                <div className="form-group">
                  <label className="col-sm-3 control-label">Start Time</label>
                  <div className="col-sm-9">
                    <TimePicker
                      defaultValue={moment(new Date().getTime())}
                      // bordered={false}
                      minuteStep={10}
                      secondStep={60}
                      onChange={(moment, timeString) => {
                        console.log(timeString, "timeString");
                        setTimeString(timeString);
                      }}
                    />
                  </div>
                </div>

                {/* File upload  */}
                <label className="col-sm-3 control-label">Log (optional)</label>
                <div className="col-sm-9">
                  <div className="panel panel-white">
                    <div className="panel-heading clearfix">
                      <h4 className="panel-title">
                        Alternatively, you can upload a mission planner log
                        instead of drawing on the map
                      </h4>
                    </div>
                    <div className="panel-body">
                      <input type="file" id="myfile" name="myfile" />
                    </div>
                  </div>

                  <Dragger {...props}>
                    <p className="ant-upload-drag-icon">
                      <CloudUploadOutlined />
                    </p>
                    <p className="ant-upload-text">Upload a Mission </p>
                    <p className="ant-upload-hint">
                      *Alternatively, you can upload a mission planner log
                      instead of drawing on the map
                    </p>
                  </Dragger>
                </div>

                {/*  */}
                <hr />

                {/* Submit */}

                <div className="col-sm-12">
                  <button
                    type="submit"
                    className="btn btn-primary "
                    style={{ width: "100%" }}
                  >
                    Submit
                  </button>
                </div>

                <hr />
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CreateReserve;

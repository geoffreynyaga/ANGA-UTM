import React from "react";

interface Props {
  lgWidth: number;
  mdWidth: number;
  title: string;
  subTitle?: string;
  backgroundColor?: string;
}
function MainPageCategoryItem(props: Props) {
  return (
    <div className={`col-lg-${props.lgWidth} col-md-${props.mdWidth}`}>
      <div
        className="panel panel-white stats-widget"
        style={{
          backgroundColor: props.backgroundColor
            ? props.backgroundColor
            : "white",
        }}
      >
        <div className="panel-body">
          <div className="pull-left">
            <span
              className="stats-number"
              style={{ color: props.backgroundColor ? "white" : "#637282" }}
            >
              {props.title}
            </span>
            {props.subTitle ? (
              <p
                className="stats-info"
                style={{ color: props.backgroundColor ? "#fff4e3" : "#637282" }}
              >
                {props.subTitle}
              </p>
            ) : (
              ""
            )}
          </div>
          <div className="pull-right">
            <i
              className="icon-arrow_forward stats-icon"
              style={{ color: props.backgroundColor ? "white" : "#63CB89" }}
            ></i>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MainPageCategoryItem;

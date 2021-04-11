import React, { useEffect } from "react";
import Calendar from "@toast-ui/react-calendar";
import "tui-calendar/dist/tui-calendar.css";

function CalendarMainScreen() {
  const today = new Date();
  const start = new Date();
  return (
    <div className="page-inner">
      <hr />

      <div id="main-wrapper">
        <ol className="breadcrumb">
          <li>
            <a href="#">
              <i className="fa fa-dashboard"></i> Home
            </a>
          </li>
          <li className="active">Calendar</li>
        </ol>

        {/* <!-- Main content --> */}
        <Calendar
          usageStatistics={false}
          height="900px"
          calendars={[
            {
              id: "0",
              name: "Private",
              bgColor: "#9e5fff",
              borderColor: "#9e5fff",
            },
            {
              id: "1",
              name: "Company",
              bgColor: "#00a9ff",
              borderColor: "#00a9ff",
            },
          ]}
          disableDblClick={true}
          disableClick={false}
          isReadOnly={false}
          month={{
            startDayOfWeek: 0,
          }}
          schedules={[
            {
              id: "1",
              calendarId: "0",
              title: "TOAST UI Calendar Study",
              category: "time",
              dueDateClass: "",
              start: today.toISOString(),
              // end: getDate("hours", today, 3, "+").toISOString(),
              end: new Date(new Date().setHours(start.getHours() + 2)),
            },
            // {
            //   id: "2",
            //   calendarId: "0",
            //   title: "Practice",
            //   category: "milestone",
            //   dueDateClass: "",
            //   start: getDate("date", today, 1, "+").toISOString(),
            //   end: getDate("date", today, 1, "+").toISOString(),
            //   isReadOnly: true,
            // },
            // {
            //   id: "3",
            //   calendarId: "0",
            //   title: "FE Workshop",
            //   category: "allday",
            //   dueDateClass: "",
            //   start: getDate("date", today, 2, "-").toISOString(),
            //   end: getDate("date", today, 1, "-").toISOString(),
            //   isReadOnly: true,
            // },
            // {
            //   id: "4",
            //   calendarId: "0",
            //   title: "Report",
            //   category: "time",
            //   dueDateClass: "",
            //   start: today.toISOString(),
            //   end: getDate("hours", today, 1, "+").toISOString(),
            // },
          ]}
          scheduleView
          taskView
          template={{
            milestone(schedule) {
              return `<span style="color:#fff;background-color: ${schedule.bgColor};">${schedule.title}</span>`;
            },
            milestoneTitle() {
              return "Milestone";
            },
            allday(schedule) {
              return `${schedule.title}<i class="fa fa-refresh"></i>`;
            },
            alldayTitle() {
              return "All Day";
            },
          }}
          // theme={myTheme}
          timezones={[
            {
              timezoneOffset: 540,
              displayLabel: "GMT+03:00",
              tooltip: "Nairobi",
              timezoneName: "Africa/Nairobi",
            },
          ]}
          useDetailPopup
          useCreationPopup
          // view={selectedView} // You can also set the `defaultView` option.
          week={{
            showTimezoneCollapseButton: true,
            timezonesCollapsed: true,
          }}
        />
      </div>
      {/* <!-- /.row --> */}
    </div>

    //<!-- /.content -->
  );
}

export default CalendarMainScreen;

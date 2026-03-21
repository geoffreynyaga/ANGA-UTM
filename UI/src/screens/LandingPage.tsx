import {Route, Routes} from "react-router-dom";

import ApplicationMainPage from "./ApplicationMainPage";
import ApprovalLetters from "./ApplicationMainPage/ApprovalLetters";
import CreateReserve from "./ApplicationMainPage/CreateReserve/CreateReserve";
import FlightLogDetail from "./FlightLogs/FlightLogDetail";
import FlightLogUpdate from "./FlightLogs/FlightLogUpdate";
import FlightLogsMainPage from "./FlightLogs";
import Header from "./Header";
import LandingPageMap from "./LandingPageMap";
import MailMainScreen from "./Mail";
import OrganizationsMainScreen from "./Organizations";
import ProfileMainPage from "./Profile";
import ReservesHistory from "./ApplicationMainPage/ReservesHistory";
import SideBar from "./sideBar";
import Signup from "../authentication/SignUp";
import UASDetails from "../routes/UAS/UASDetails";
import UASList from "../routes/UAS/UASList";
import UASMainPage from "../routes/uas/index.tsx";
import UASRegister from "../routes/UAS/UASRegister";
import UASUpdate from "../routes/UAS/UASUpdate";

// import CalendarMainScreen from "./Calendar";

export default function LandingPage() {
    return (
        <div>
            <SideBar />

            <div className="page-content">
                {/* Page Header */}
                <Header />

                <Routes>
                    <Route path="/ui/" element={<LandingPageMap />} />

                    <Route path="/ui/signup/" element={<Signup />} />

                    <Route path="/profile/" element={<ProfileMainPage />} />
                    <Route path="/ui/applications/" element={<ApplicationMainPage />} />
                    <Route path="/applications/create/" element={<CreateReserve />} />
                    <Route
                        path="/applications/history/"
                        element={<ReservesHistory />}
                    />
                    <Route
                        path="/applications/approval-letters/"
                        element={<ApprovalLetters />}
                    />
                    <Route
                        path="/flight-plans/logs/"
                        element={<FlightLogsMainPage />}
                    />
                    <Route
                        path="/flight-plans/logs/:id/"
                        element={<FlightLogDetail />}
                    />
                    <Route
                        path="/flight-plans/logs/:id/update/"
                        element={<FlightLogUpdate />}
                    />
                    <Route
                        path="/flight-plans/logs/"
                        element={<FlightLogsMainPage />}
                    />

                    <Route path="/uas/" element={<UASMainPage />} />
                    <Route path="/uas/list/" element={<UASList />} />
                    <Route path="/uas/register/" element={<UASRegister />} />
                    <Route path="/uas/register/" element={<UASRegister />} />
                    <Route path="/uas/:id/" element={<UASDetails />} />
                    <Route path="/uas/:id/update/" element={<UASUpdate />} />

                    <Route
                        path="/organizations/"
                        element={<OrganizationsMainScreen />}
                    />
                    <Route path="/mail/" element={<MailMainScreen />} />

                    {/* <Route exact path="/calendar">
            <CalendarMainScreen />
          </Route> */}
                </Routes>
            </div>
        </div>
    );
}

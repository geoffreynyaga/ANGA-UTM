import { Route, Routes } from "react-router-dom";
import { Suspense, lazy } from "react";

import About from "./about";
import ChecklistBuilder from "../screens/Checklists";
import RootLayout from "./navbar";

function RoutesApp() {
	return (
			<Routes>
			{/*	<Route path="/ui/" element={<RootLayout />}>

					 <Route path="/ui/uas_index/" element={<UASMainPage />} />
					// <Route path="/ui/uas_index/list/" element={<UASList />} />
					<Route path="/ui/uas_index/create/" element={<UASCreate />} />
					<Route path="/ui/uas_index/register/" element={<UASRegister />} />
					<Route path="/ui/uas_index/update/" element={<UASUpdate />} />
					<Route path="/ui/uas_index/details/" element={<UASDetails />} />

				</Route>
                */}
                    <Route path="/ui/about/" element={<About />} />
					<Route path="/ui/checklists/" element={<ChecklistBuilder />} />
			</Routes>
	);
}

export default RoutesApp;

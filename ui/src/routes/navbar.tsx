import {Link, NavLink, Outlet} from "react-router-dom";

export default function Navbar() {
    return (
        <>
            <div className="flex gap-2 p-2">
                <NavLink
                    to="/ui/"
                    className={({ isActive }) => isActive ? "font-bold" : ""}
                >
                    Home
                </NavLink>{" "}
                <NavLink
                    to="/ui/about/"
                    className={({ isActive }) => isActive ? "font-bold" : ""}
                >
                    About
                </NavLink>
                <NavLink
                    to="/ui/uas_index/"
                    className={({ isActive }) => isActive ? "font-bold" : ""}
                >
                    UAS
                </NavLink>
                <NavLink
                    to="/ui/checklists/"
                    className={({ isActive }) => isActive ? "font-bold" : ""}
                >
                    Checklists
                </NavLink>
            </div>
            <hr />
            <Outlet />
        </>
    );
}

export function NotFound() {
    return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] p-4 text-center">
            <h1 className="mb-2 text-4xl font-black text-gray-900">404</h1>
            <p className="mb-6 font-medium text-gray-500">Oops! The page you're looking for doesn't exist.</p>
            <Link
                to="/"
                className="px-6 py-2 font-bold text-white transition-colors bg-blue-600 shadow-lg rounded-xl hover:bg-blue-700 shadow-blue-200"
            >
                Back to Safety
            </Link>
        </div>
    );
}

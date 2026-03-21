import {Link, Outlet, createRootRoute} from "@tanstack/react-router";

import {TanStackRouterDevtools} from "@tanstack/router-devtools";

export const Route = createRootRoute({
    component: () => (
        <>
            <div className="flex gap-2 p-2">
                <Link to="/" className="[&.active]:font-bold">
                    Home
                </Link>{" "}
                <Link to="/about" className="[&.active]:font-bold">
                    About
                </Link>
                <Link to="/uas_index" className="[&.active]:font-bold">
                    UAS
                </Link>
            </div>
            <hr />
            <Outlet />
            <TanStackRouterDevtools />
        </>
    ),
    notFoundComponent: () => {
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
        )
    }
});

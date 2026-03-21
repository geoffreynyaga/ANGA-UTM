import "./index.css";

import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import {RouterProvider, createRouter} from "@tanstack/react-router";

import {BrowserRouter} from "react-router-dom";
import ReactDOM from "react-dom/client";
import {ReactQueryDevtools} from "@tanstack/react-query-devtools";
import {StrictMode} from "react";
import {routeTree} from "./routeTree.gen";

// Create a client
const queryClient = new QueryClient();

// Create a new router instance
const router = createRouter({routeTree});

// Register the router instance for type safety
declare module "@tanstack/react-router" {
    interface Register {
        router: typeof router;
    }
}

// Render the app
const rootElement = document.getElementById("root")!;
if (!rootElement.innerHTML) {
    const root = ReactDOM.createRoot(rootElement);
    root.render(
        <StrictMode>
            <BrowserRouter>
                <QueryClientProvider client={queryClient}>
                    {/* <App /> */}
                    <RouterProvider router={router} />
                    <ReactQueryDevtools initialIsOpen={false} />
                </QueryClientProvider>
            </BrowserRouter>
        </StrictMode>,
    );
}

import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import React from "react";
import "./index.css";
import App from "./App";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { CookiesProvider } from "react-cookie";

// Create a client
const queryClient = new QueryClient();

const container = document.getElementById("root");
if (!container) throw new Error("Could not find root element");
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <CookiesProvider>
      <BrowserRouter>
        <QueryClientProvider client={queryClient}>
          <App />
        </QueryClientProvider>
      </BrowserRouter>
    </CookiesProvider>
  </React.StrictMode>,
);

import React from "react";
import ReactDOM from "react-dom/client";
import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { RouterProvider } from "react-router-dom";

import { router } from "./routes/router";
import "./styles.css";
import "./i18n/config";
import { registerSW } from "./pwa/registerSW";

const queryClient = new QueryClient();

const theme = createTheme({
  direction: "rtl",
  typography: {
    fontFamily: "Cairo, sans-serif"
  }
});

document.documentElement.lang = "ar";
document.documentElement.dir = "rtl";

registerSW();

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <RouterProvider router={router} />
      </ThemeProvider>
    </QueryClientProvider>
  </React.StrictMode>
);

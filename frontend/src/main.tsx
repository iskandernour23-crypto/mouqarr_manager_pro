import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import AppLayout from "./layouts/AppLayout";
import DashboardPage from "./pages/Dashboard";
import ResidentsPage from "./pages/Residents";
import GuestsPage from "./pages/Guests";
import BookingsPage from "./pages/Bookings";
import CalendarPage from "./pages/Calendar";
import PaymentsPage from "./pages/Payments";
import ReportsPage from "./pages/Reports";
import SettingsPage from "./pages/Settings";
import LoginPage from "./pages/Login";
import "./styles.css";
import "react-big-calendar/lib/css/react-big-calendar.css";
import { Toaster } from "sonner";
import { AuthProvider } from "./store/auth";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<AppLayout />}>
            <Route index element={<DashboardPage />} />
            <Route path="residents" element={<ResidentsPage />} />
            <Route path="guests" element={<GuestsPage />} />
            <Route path="bookings" element={<BookingsPage />} />
            <Route path="calendar" element={<CalendarPage />} />
            <Route path="payments" element={<PaymentsPage />} />
            <Route path="reports" element={<ReportsPage />} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
      <Toaster position="top-left" richColors dir="rtl" />
    </AuthProvider>
  </React.StrictMode>
);

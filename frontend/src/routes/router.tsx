import { createBrowserRouter } from "react-router-dom";

import { DashboardPage } from "../pages/Dashboard";
import { Layout } from "../layouts/Layout";
import { LoginPage } from "../pages/Login";
import { ResidentsPage } from "../pages/Residents";
import { GuestsPage } from "../pages/Guests";
import { BookingsPage } from "../pages/Bookings";
import { PaymentsPage } from "../pages/Payments";
import { ReportsPage } from "../pages/Reports";
import { SettingsPage } from "../pages/Settings";
import { CalendarPage } from "../pages/Calendar";
import { AdminPage } from "../pages/Admin";
import { MobileLayout } from "../m/MobileLayout";
import { MobileCheckin } from "../m/Checkin";
import { MobilePayment } from "../m/Payment";
import { MobileExtend } from "../m/Extend";

export const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginPage />
  },
  {
    path: "/",
    element: <Layout />,
    children: [
      { path: "/", element: <DashboardPage /> },
      { path: "/residents", element: <ResidentsPage /> },
      { path: "/guests", element: <GuestsPage /> },
      { path: "/bookings", element: <BookingsPage /> },
      { path: "/payments", element: <PaymentsPage /> },
      { path: "/reports", element: <ReportsPage /> },
      { path: "/settings", element: <SettingsPage /> },
      { path: "/calendar", element: <CalendarPage /> },
      { path: "/admin", element: <AdminPage /> }
    ]
  },
  {
    path: "/m",
    element: <MobileLayout />,
    children: [
      { path: "checkin", element: <MobileCheckin /> },
      { path: "payment", element: <MobilePayment /> },
      { path: "extend", element: <MobileExtend /> }
    ]
  }
]);

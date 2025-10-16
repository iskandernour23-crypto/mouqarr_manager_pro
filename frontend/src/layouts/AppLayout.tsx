import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { useAuth, useAuthGuard } from "../store/auth";

const AppLayout = () => {
  const isAuthenticated = useAuthGuard();
  const { logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/login");
    }
  }, [isAuthenticated, navigate]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-slate-900">مدير مقار فليكس</h1>
          <button
            className="px-3 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
            onClick={logout}
          >
            تسجيل الخروج
          </button>
        </div>
      </header>
      <div className="max-w-6xl mx-auto px-4 py-6 grid grid-cols-1 md:grid-cols-[240px_1fr] gap-6">
        <aside className="bg-white border rounded-xl p-4 space-y-2">
          <nav className="flex flex-col gap-1">
            <NavLink to="/" end className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
              لوحة التحكم
            </NavLink>
            <NavLink to="/residents" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
              المقيمون
            </NavLink>
            <NavLink to="/guests" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
              الضيوف
            </NavLink>
            <NavLink to="/bookings" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
              الحجوزات
            </NavLink>
            <NavLink to="/calendar" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
              التقويم
            </NavLink>
            <NavLink to="/payments" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
              الدفعات
            </NavLink>
            <NavLink to="/reports" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
              التقارير
            </NavLink>
            <NavLink to="/settings" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
              الإعدادات
            </NavLink>
          </nav>
        </aside>
        <main className="space-y-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default AppLayout;

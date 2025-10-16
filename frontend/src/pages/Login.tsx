import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../store/auth";

const LoginPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const username = String(form.get("username"));
    const password = String(form.get("password"));
    setLoading(true);
    try {
      await login(username, password);
      navigate("/");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-xl shadow-sm w-full max-w-md space-y-4">
        <h2 className="text-2xl font-bold text-center text-slate-900">تسجيل الدخول</h2>
        <div className="space-y-2">
          <label className="block text-sm text-slate-600" htmlFor="username">
            اسم المستخدم
          </label>
          <input
            id="username"
            name="username"
            className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring"
            placeholder="admin"
            required
          />
        </div>
        <div className="space-y-2">
          <label className="block text-sm text-slate-600" htmlFor="password">
            كلمة المرور
          </label>
          <input
            id="password"
            name="password"
            type="password"
            className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring"
            placeholder="admin"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-slate-900 text-white py-2 rounded-lg hover:bg-slate-800 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "جاري الدخول..." : "دخول"}
        </button>
      </form>
    </div>
  );
};

export default LoginPage;

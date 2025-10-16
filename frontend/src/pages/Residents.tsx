import { useEffect, useState } from "react";
import axios from "axios";
import { toast } from "sonner";

interface Resident {
  id: number;
  name: string;
  gender: string;
  start_date?: string;
  end_date?: string;
}

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const ResidentsPage = () => {
  const [residents, setResidents] = useState<Resident[]>([]);

  useEffect(() => {
    axios
      .get<Resident[]>(`${API_URL}/residents/`)
      .then((response) => setResidents(response.data))
      .catch(() => toast.error("تعذر تحميل بيانات المقيمين"));
  }, []);

  return (
    <section className="bg-white rounded-xl shadow-sm p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-slate-900">المقيمون</h2>
        <button className="px-3 py-2 rounded-lg bg-slate-900 text-white">إضافة مقيم</button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-slate-500 border-b">
              <th className="py-2">الاسم</th>
              <th>الجنس</th>
              <th>تاريخ البدء</th>
              <th>تاريخ الانتهاء</th>
            </tr>
          </thead>
          <tbody>
            {residents.map((resident) => (
              <tr key={resident.id} className="border-b last:border-0">
                <td className="py-2">{resident.name}</td>
                <td>{resident.gender}</td>
                <td>{resident.start_date ?? "-"}</td>
                <td>{resident.end_date ?? "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
};

export default ResidentsPage;

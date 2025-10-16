import { dayjsLocalizer, Calendar } from "react-big-calendar";
import dayjs from "dayjs";
import "dayjs/locale/ar";
import localizedFormat from "dayjs/plugin/localizedFormat";
import { useMemo } from "react";

dayjs.extend(localizedFormat);
dayjs.locale("ar");
const localizer = dayjsLocalizer(dayjs);

const CalendarPage = () => {
  const events = useMemo(
    () => [
      {
        title: "حجز مقيم",
        start: new Date(),
        end: new Date(),
        resource: { status: "confirmed" }
      }
    ],
    []
  );

  return (
    <section className="bg-white rounded-xl shadow-sm p-6">
      <h2 className="text-xl font-semibold text-slate-900 mb-4">التقويم</h2>
      <Calendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        style={{ height: 500 }}
        culture="ar"
      />
    </section>
  );
};

export default CalendarPage;

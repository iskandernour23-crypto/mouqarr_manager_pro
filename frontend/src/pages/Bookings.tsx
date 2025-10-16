import { Box, Card, CardContent, Typography } from "@mui/material";
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import "moment/locale/ar";
import { useMemo } from "react";

moment.locale("ar");
const localizer = momentLocalizer(moment);

export const BookingsPage = () => {
  const events = useMemo(() => [], []);
  return (
    <Box>
      <Typography variant="h5" mb={2} textAlign="right">
        الحجوزات
      </Typography>
      <Card>
        <CardContent>
          <Calendar
            localizer={localizer}
            events={events}
            startAccessor="start"
            endAccessor="end"
            style={{ height: 500 }}
            rtl
          />
        </CardContent>
      </Card>
    </Box>
  );
};

import { Box, Card, CardContent, Typography } from "@mui/material";

export const CalendarPage = () => (
  <Box>
    <Typography variant="h5" mb={2} textAlign="right">
      التقويم
    </Typography>
    <Card>
      <CardContent>عرض شهري للإشغال سيظهر هنا.</CardContent>
    </Card>
  </Box>
);

import { Box, Card, CardContent, Typography } from "@mui/material";

export const ReportsPage = () => (
  <Box>
    <Typography variant="h5" mb={2} textAlign="right">
      التقارير والتحليلات
    </Typography>
    <Card>
      <CardContent>
        <Typography textAlign="right">
          لوحة تحليلات مع توقعات الإشغال والدخل سيتم تضمينها هنا.
        </Typography>
      </CardContent>
    </Card>
  </Box>
);

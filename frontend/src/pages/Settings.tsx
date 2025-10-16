import { Box, Card, CardContent, Typography } from "@mui/material";

export const SettingsPage = () => (
  <Box>
    <Typography variant="h5" mb={2} textAlign="right">
      الإعدادات
    </Typography>
    <Card>
      <CardContent>
        <Typography textAlign="right">
          إعدادات النظام بما في ذلك تكوين البريد الإلكتروني، التلغرام، وتكامل Google.
        </Typography>
      </CardContent>
    </Card>
  </Box>
);

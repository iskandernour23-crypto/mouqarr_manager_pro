import { Box, Card, CardContent, Typography } from "@mui/material";

export const AdminPage = () => (
  <Box>
    <Typography variant="h5" mb={2} textAlign="right">
      الإدارة
    </Typography>
    <Card>
      <CardContent>
        إدارة المستخدمين، السجلات، والويب هوك ستظهر هنا.
      </CardContent>
    </Card>
  </Box>
);

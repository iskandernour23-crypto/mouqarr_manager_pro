import { Box, Button, Stack, Typography } from "@mui/material";
import { Outlet, useNavigate } from "react-router-dom";

export const MobileLayout = () => {
  const navigate = useNavigate();
  return (
    <Box sx={{ minHeight: "100vh", backgroundColor: "#f1f5f9", p: 2 }}>
      <Stack spacing={2}>
        <Typography variant="h5" textAlign="center">
          إجراءات سريعة
        </Typography>
        <Stack direction="row" spacing={1} justifyContent="space-between">
          <Button variant="contained" sx={{ flex: 1 }} onClick={() => navigate("/m/checkin")}>تسجيل</Button>
          <Button variant="contained" sx={{ flex: 1 }} onClick={() => navigate("/m/payment")}>دفع</Button>
          <Button variant="contained" sx={{ flex: 1 }} onClick={() => navigate("/m/extend")}>تمديد</Button>
        </Stack>
        <Outlet />
      </Stack>
    </Box>
  );
};

import { Button, Card, CardContent, Stack, TextField, Typography } from "@mui/material";
import { useState } from "react";

export const MobileCheckin = () => {
  const [qr, setQr] = useState("");
  return (
    <Card>
      <CardContent>
        <Typography textAlign="center" mb={2}>
          مسح رمز QR أو إدخال المعرف يدوياً
        </Typography>
        <Stack spacing={2}>
          <TextField label="معرف الحجز" value={qr} onChange={(event) => setQr(event.target.value)} fullWidth />
          <Button variant="contained">تأكيد الدخول</Button>
        </Stack>
      </CardContent>
    </Card>
  );
};

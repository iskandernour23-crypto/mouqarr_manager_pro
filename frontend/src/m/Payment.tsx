import { Button, Card, CardContent, Stack, TextField, Typography } from "@mui/material";
import { useState } from "react";

export const MobilePayment = () => {
  const [amount, setAmount] = useState("0");
  const [method, setMethod] = useState("cash");
  return (
    <Card>
      <CardContent>
        <Typography textAlign="center" mb={2}>
          تسجيل دفعة سريعة
        </Typography>
        <Stack spacing={2}>
          <TextField label="المبلغ" value={amount} onChange={(event) => setAmount(event.target.value)} fullWidth />
          <TextField label="طريقة الدفع" value={method} onChange={(event) => setMethod(event.target.value)} fullWidth />
          <Button variant="contained">إصدار إيصال</Button>
        </Stack>
      </CardContent>
    </Card>
  );
};

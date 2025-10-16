import { Box, Button, Paper, TextField, Typography } from "@mui/material";
import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export const LoginPage = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      await axios.post(
        `${__API_URL__}/auth/login`,
        new URLSearchParams({ username, password })
      );
      navigate("/");
    } catch (err) {
      setError("بيانات الدخول غير صحيحة");
    }
  };

  return (
    <Box sx={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", backgroundColor: "#e2e8f0" }}>
      <Paper component="form" onSubmit={onSubmit} sx={{ p: 4, width: 360, textAlign: "right" }}>
        <Typography variant="h5" mb={2}>
          تسجيل الدخول
        </Typography>
        <TextField fullWidth label="المستخدم" value={username} onChange={(event) => setUsername(event.target.value)} margin="normal" />
        <TextField fullWidth label="كلمة المرور" value={password} onChange={(event) => setPassword(event.target.value)} type="password" margin="normal" />
        {error && (
          <Typography color="error" variant="body2" mt={1}>
            {error}
          </Typography>
        )}
        <Button type="submit" variant="contained" fullWidth sx={{ mt: 3 }}>
          دخول
        </Button>
      </Paper>
    </Box>
  );
};

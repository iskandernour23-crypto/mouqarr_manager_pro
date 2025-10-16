import { Alert, AppBar, Box, Button, Drawer, IconButton, List, ListItem, ListItemText, Toolbar, Typography } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import LogoutIcon from "@mui/icons-material/Logout";
import { useState } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useOfflineBanner } from "../hooks/useOfflineBanner";

const links = [
  { labelKey: "dashboard", path: "/" },
  { labelKey: "residents", path: "/residents" },
  { labelKey: "guests", path: "/guests" },
  { labelKey: "bookings", path: "/bookings" },
  { labelKey: "calendar", path: "/calendar" },
  { labelKey: "payments", path: "/payments" },
  { labelKey: "reports", path: "/reports" },
  { labelKey: "settings", path: "/settings" },
  { labelKey: "admin", path: "/admin" }
];

export const Layout = () => {
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();
  const { t } = useTranslation();
  const offline = useOfflineBanner();

  const drawer = (
    <Box sx={{ width: 250 }} role="presentation" onClick={() => setOpen(false)}>
      <List>
        {links.map((link) => (
          <ListItem button key={link.path} onClick={() => navigate(link.path)}>
            <ListItemText primary={t(link.labelKey, link.labelKey)} sx={{ textAlign: "right" }} />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: "flex", minHeight: "100vh", backgroundColor: "#f8fafc" }}>
      <AppBar position="fixed" color="primary" dir="rtl">
        <Toolbar>
          <IconButton color="inherit" edge="start" onClick={() => setOpen(true)}>
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, textAlign: "right" }}>
            موَقَّر فليكس
          </Typography>
          <Button color="inherit" startIcon={<LogoutIcon />}>
            خروج
          </Button>
        </Toolbar>
      </AppBar>
      {offline && (
        <Box sx={{ position: "fixed", top: 64, right: 16, left: 16, zIndex: 1200 }}>
          <Alert severity="warning" sx={{ direction: "rtl" }}>
            الوضع غير متصل - عرض للقراءة فقط
          </Alert>
        </Box>
      )}
      <Drawer anchor="right" open={open} onClose={() => setOpen(false)}>
        {drawer}
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, mt: 8, p: 3 }}>
        <Outlet />
      </Box>
    </Box>
  );
};

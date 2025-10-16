import { Box, Card, CardContent, Grid, Typography } from "@mui/material";
import { useTranslation } from "react-i18next";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { ResponsiveContainer, BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip } from "recharts";

const fetchAnalytics = async () => {
  const { data } = await axios.get(`${__API_URL__}/analytics/overview`);
  return data;
};

export const DashboardPage = () => {
  const { t } = useTranslation();
  const { data } = useQuery({ queryKey: ["analytics"], queryFn: fetchAnalytics });

  const incomeData = Object.entries(data?.income || {}).map(([name, value]) => ({ name, value }));

  return (
    <Box>
      <Typography variant="h4" mb={3} textAlign="right">
        {t("dashboard", "لوحة التحكم")}
      </Typography>
      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" textAlign="right">
                السكان
              </Typography>
              <Typography variant="h5" textAlign="right">
                {data?.residents || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" textAlign="right">
                الضيوف
              </Typography>
              <Typography variant="h5" textAlign="right">
                {data?.guests || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" textAlign="right">
                الدخل الشهري
              </Typography>
              <Typography variant="h5" textAlign="right">
                {incomeData.reduce((acc, cur) => acc + cur.value, 0)} ر.س
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" textAlign="right" mb={2}>
                اتجاه الدخل
              </Typography>
              <Box sx={{ height: 280 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={incomeData} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" hide />
                    <YAxis type="category" dataKey="name" />
                    <Tooltip />
                    <Bar dataKey="value" fill="#2563eb" radius={8} />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

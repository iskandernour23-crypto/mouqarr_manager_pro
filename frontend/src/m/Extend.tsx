import { Button, Card, CardContent, Grid, Typography } from "@mui/material";

const offsets = [1, 3, 7];

export const MobileExtend = () => (
  <Card>
    <CardContent>
      <Typography textAlign="center" mb={2}>
        تعديل مدة الإقامة
      </Typography>
      <Grid container spacing={2}>
        {offsets.map((days) => (
          <Grid item xs={4} key={`extend-${days}`}>
            <Button variant="contained" fullWidth>{`+${days}`}</Button>
          </Grid>
        ))}
        {offsets.map((days) => (
          <Grid item xs={4} key={`shorten-${days}`}>
            <Button variant="outlined" fullWidth>{`-${days}`}</Button>
          </Grid>
        ))}
      </Grid>
    </CardContent>
  </Card>
);

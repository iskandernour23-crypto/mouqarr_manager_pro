import { Box, Button, Card, CardContent, Typography } from "@mui/material";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { ColumnDef, getCoreRowModel, useReactTable } from "@tanstack/react-table";

import { DataTable } from "../components/DataTable";

export type Resident = {
  id: number;
  name: string;
  status: string;
  amount: number;
  plan_type: string;
};

const columns: ColumnDef<Resident>[] = [
  { header: "الاسم", accessorKey: "name" },
  { header: "الحالة", accessorKey: "status" },
  { header: "الخطة", accessorKey: "plan_type" },
  { header: "المبلغ", accessorKey: "amount" }
];

const fetchResidents = async () => {
  const { data } = await axios.get<Resident[]>(`${__API_URL__}/residents/`);
  return data;
};

export const ResidentsPage = () => {
  const { data = [] } = useQuery({ queryKey: ["residents"], queryFn: fetchResidents });
  const table = useReactTable({ columns, data, getCoreRowModel: getCoreRowModel() });

  return (
    <Box>
      <Typography variant="h5" mb={2} textAlign="right">
        المقيمون
      </Typography>
      <Card>
        <CardContent>
          <Button variant="contained" sx={{ mb: 2 }}>
            إضافة مقيم
          </Button>
          <DataTable table={table} />
        </CardContent>
      </Card>
    </Box>
  );
};

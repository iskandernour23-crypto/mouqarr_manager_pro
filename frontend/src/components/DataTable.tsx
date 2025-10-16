import { Table, TableBody, TableCell, TableHead, TableRow } from "@mui/material";
import { Table as ReactTable } from "@tanstack/react-table";

export const DataTable = <T,>({ table }: { table: ReactTable<T> }) => {
  return (
    <Table dir="rtl">
      <TableHead>
        {table.getHeaderGroups().map((headerGroup) => (
          <TableRow key={headerGroup.id}>
            {headerGroup.headers.map((header) => (
              <TableCell key={header.id} align="right">
                {header.isPlaceholder ? null : header.column.columnDef.header as string}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableHead>
      <TableBody>
        {table.getRowModel().rows.map((row) => (
          <TableRow key={row.id}>
            {row.getVisibleCells().map((cell) => (
              <TableCell key={cell.id} align="right">
                {cell.getValue() as string}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { DataGrid, GridColDef, GridPaginationModel } from '@mui/x-data-grid';
import { Add as AddIcon } from '@mui/icons-material';

const Students: React.FC = () => {
  const [paginationModel, setPaginationModel] = React.useState<GridPaginationModel>({
    pageSize: 5,
    page: 0,
  });

  // Sample data - replace with actual data from API
  const rows = [
    { id: 1, name: 'John Doe', email: 'john@example.com', grade: 'A', status: 'Active' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', grade: 'B+', status: 'Active' },
    { id: 3, name: 'Bob Johnson', email: 'bob@example.com', grade: 'A-', status: 'Inactive' },
    { id: 4, name: 'Alice Brown', email: 'alice@example.com', grade: 'B', status: 'Active' },
  ];

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Name', width: 200 },
    { field: 'email', headerName: 'Email', width: 250 },
    { field: 'grade', headerName: 'Grade', width: 100 },
    { field: 'status', headerName: 'Status', width: 100 },
  ];

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h4">Students</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            // TODO: Implement add student functionality
          }}
        >
          Add Student
        </Button>
      </Box>
      <Box sx={{ height: 400, width: '100%' }}>
        <DataGrid
          rows={rows}
          columns={columns}
          paginationModel={paginationModel}
          onPaginationModelChange={setPaginationModel}
          pageSizeOptions={[5, 10, 25]}
          checkboxSelection
          disableRowSelectionOnClick
        />
      </Box>
    </Box>
  );
};

export default Students; 
import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { DataGrid, GridColDef, GridPaginationModel } from '@mui/x-data-grid';
import { Add as AddIcon } from '@mui/icons-material';

const Courses: React.FC = () => {
  const [paginationModel, setPaginationModel] = React.useState<GridPaginationModel>({
    pageSize: 5,
    page: 0,
  });

  // Sample data - replace with actual data from API
  const rows = [
    { id: 1, name: 'Mathematics 101', code: 'MATH101', instructor: 'Dr. Smith', students: 45, status: 'Active' },
    { id: 2, name: 'Physics 101', code: 'PHYS101', instructor: 'Dr. Johnson', students: 38, status: 'Active' },
    { id: 3, name: 'Chemistry 101', code: 'CHEM101', instructor: 'Dr. Brown', students: 42, status: 'Active' },
    { id: 4, name: 'Biology 101', code: 'BIO101', instructor: 'Dr. Davis', students: 35, status: 'Inactive' },
  ];

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Course Name', width: 200 },
    { field: 'code', headerName: 'Course Code', width: 130 },
    { field: 'instructor', headerName: 'Instructor', width: 150 },
    { field: 'students', headerName: 'Students', width: 100 },
    { field: 'status', headerName: 'Status', width: 100 },
  ];

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h4">Courses</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            // TODO: Implement add course functionality
          }}
        >
          Add Course
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

export default Courses; 
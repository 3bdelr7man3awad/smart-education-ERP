import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { DataGrid, GridColDef, GridPaginationModel } from '@mui/x-data-grid';
import { Add as AddIcon } from '@mui/icons-material';

const Assignments: React.FC = () => {
  const [paginationModel, setPaginationModel] = React.useState<GridPaginationModel>({
    pageSize: 5,
    page: 0,
  });

  // Sample data - replace with actual data from API
  const rows = [
    { id: 1, title: 'Math Homework', course: 'Mathematics 101', dueDate: '2024-04-20', status: 'Pending', submissions: 35 },
    { id: 2, title: 'Physics Lab Report', course: 'Physics 101', dueDate: '2024-04-22', status: 'Pending', submissions: 28 },
    { id: 3, title: 'Chemistry Quiz', course: 'Chemistry 101', dueDate: '2024-04-25', status: 'Pending', submissions: 40 },
    { id: 4, title: 'Biology Project', course: 'Biology 101', dueDate: '2024-04-28', status: 'Completed', submissions: 30 },
  ];

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'title', headerName: 'Title', width: 200 },
    { field: 'course', headerName: 'Course', width: 150 },
    { field: 'dueDate', headerName: 'Due Date', width: 130 },
    { field: 'status', headerName: 'Status', width: 100 },
    { field: 'submissions', headerName: 'Submissions', width: 100 },
  ];

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h4">Assignments</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            // TODO: Implement add assignment functionality
          }}
        >
          Add Assignment
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

export default Assignments; 
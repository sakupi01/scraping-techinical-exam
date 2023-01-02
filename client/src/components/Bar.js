import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import FastfoodIcon from '@mui/icons-material/Fastfood';
import { purple, red } from '@mui/material/colors';


export default function DenseAppBar() {
  const primary = '#F2EDEB'; 
  const accent = '#F25041';
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" style={{ background: primary }}>
        <Toolbar variant="dense">
          <FastfoodIcon style={{ color: accent }} />
          <Typography variant="h6" component="div" style={{ color: accent }}>
            ScraPI
          </Typography>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
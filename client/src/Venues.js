import React from "react";
import {Grid, Box, Button} from "@mui/material";
import VenueCard from './components/VenueCard'
import AppBar from './components/Bar'
import {useLocation} from "react-router-dom";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import {useNavigate} from 'react-router-dom';


export const Venues = () => {

  const navigate = useNavigate();
  const handleClick = () => {
    navigate('/', {replace: true});
  };

  const primary = '#F2EDEB';
  const accent = '#F25041';

  // to get the data from backend
  console.log(useLocation());
  const location = useLocation().state;

  return ( 
    <div>
      <AppBar></AppBar>
      <div  style={{display:'flex', justifyContent: 'flex-start', alignItems: 'center', padding: 10 }}>
        <Button 
                variant="contained"
                startIcon={<ArrowBackIcon />}
                onClick={handleClick}
                sx = {{
                  backgroundColor: primary,
                  color: accent,
                  textAlign: "center",
                  ':hover': {
                    backgroundColor: primary, // theme.palette.primary.main
                    color: accent,
                  },
                  ':click': {
                    backgroundColor: primary, // theme.palette.primary.main
                    color: accent,
                  }
                }}
              >Back
              </Button>

      </div>
      { location ? <Box sx={{ flexGrow: 1, margin: 5 }} gap={2}>
                <Grid container
                spacing={4}
                direction="row"
                justifyContent="center"
                alignItems="stretch"
                >
                {location.map((venue, index) => (
                  <Grid item xs={12} sm={4} key={index}>
                      <VenueCard venue = {venue}></VenueCard>
                  </Grid>
                ))}

            </Grid>
          </Box> 
          : <h2> Nothing found.</h2>
          }
    </div>
   
    );
}
import React from "react";
import {Grid, Box} from "@mui/material";
import VenueCard from './components/VenueCard'
import {useLocation} from "react-router-dom";


export const Venues = () => {

  // to get the data from backend
  console.log(useLocation());
  const location = useLocation().state;

  return ( 
    <div>
    { location ? <Box sx={{ flexGrow: 1 }} gap={2}>
              <Grid container 
              spacing={2}
              direction="row"
              justifyContent="center"
              alignItems="stretch"
              >
                  <Grid item xs={12} sm={4}>
                    <VenueCard venue = {location[0]} color = {"#e57373"}></VenueCard>
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <VenueCard venue = {location[1]} color = {'#ef9a9a'}></VenueCard>
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <VenueCard venue = {location[2]} color = {"#ffcdd2"}></VenueCard>
                  </Grid>
              </Grid>

              <Grid container
              spacing={4}
              direction="row"
              justifyContent="flex-start"
              alignItems="stretch"
              >
              {location.slice(3).map((venue, index) => (
                <Grid item xs={12} sm={4} key={index}>
                    <VenueCard venue = {venue} color = {'#ffebee'}></VenueCard>
                </Grid>
              ))}

          </Grid>
        </Box> 
        : <h2> Nothing found.</h2>
        }
    </div>
   
    );
}
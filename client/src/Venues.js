import React from "react";
import {Grid, Box} from "@mui/material";
import VenueCard from './components/VenueCard'
import {useState, useEffect, useLayoutEffect} from 'react';
import {useLocation} from "react-router-dom";


export const Venues = () => {

const [data, setData] = useState([{}])
// const [query, setQuery] = useState("")


//   useLayoutEffect((location) => {
        
//   },[])

  // to get the data from back
  console.log(useLocation());
  data = useLocation().state
  // useEffect(() => {
  //   const quelist = [ location[0], location[1], location[2], location[3], location[4]];
  //   let query_str= "/search?"
  //       quelist.forEach(el => {
  //         if (el[0] !== false) {
  //           query_str = query_str + el[1] + "=" + el[2] + "&";
  //         }
  //       });
        
  //   setQuery(query_str);

  //   if(query !== ""){
  //     console.log(query);
  //     fetch(query).then(
  //       res => res.json()
  //     ).then(
  //       response => {
  //         setData(response)
  //         console.log(response)
  //       }
  //     )
  //   }
  // }, [query])

  return ( 
    <Box sx={{ flexGrow: 1 }}>
          <Grid item xs={5}>
            <VenueCard venue = {data[0]}></VenueCard>
          </Grid>
          <Grid item xs={4}>
            <VenueCard venue = {data[1]}></VenueCard>
          </Grid>
          <Grid item xs={3}>
            <VenueCard venue = {data[2]}></VenueCard>
          </Grid>
        <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
          {data.slice(3).map((venue, index) => (
            <Grid item xs={2} key={index}>
                <VenueCard venue = {venue}></VenueCard>
            </Grid>
          ))}
        </Grid>
    </Box>
    );
}
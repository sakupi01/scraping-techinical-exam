import { Button } from "@mui/material";
import SearchIcon from '@mui/icons-material/Search';
import {useState, useEffect} from 'react';
import AppBar from './components/Bar';
import NameSearchField from './components/NameSearchField';
import RatingSetField from './components/RatingSetField';
import PriceSelectField from './components/PriceSelectField';
import Map from './components/Map';
import { useNavigate } from "react-router-dom";
import Container from '@mui/material/Container';

export default function Search() {
    const navigate = useNavigate()
    const [query, setQuery] = useState("")
    const [name, setName] = useState([false, "name", ""])
    const [rating, setRating] = useState([false, "rating", 0]);
    const [price, setPrice] = useState([false, "price_type", ""]);
    const [lat, setLat] = useState([false, "latitude", 0.0]);
    const [lon, setLon] = useState([false, "longtitude", 0.0]);
    
    const handleClick = () => {
      const quelist = [name, rating, price, lat, lon];
      let query_str= "/search?"
        quelist.forEach(el => {
          if (el[0] !== false) {
            query_str = query_str + el[1] + "=" + el[2] + "&";
          }
        });
        
      setQuery(query_str);
    }

    useEffect(() => {
      if(query !== ""){
          console.log(query);
          // (In the Development Phase)The configuration established by create-react-app, the Webpack dev server will infer what traffic to proxy. 
          // It will proxy a request if the URL is not recognized or if the request is not loading static assets (like HTML/CSS/JS).
          fetch(query).then( 
            res => 
                res.json()
            ).then(
              response => {
                console.log(response)
                navigate("/result", { state: response })
              }
              )
        }
      }, [query])

      const primary = '#F2EDEB'; // #f44336
      const accent = '#F25041'; // #e040fb

  return (
    <div>
      <AppBar></AppBar>
      <Container maxWidth="sm">
        <div style={{display:'flex', flexDirection: "column", justifyContent: 'center', alignItems: 'center' }}>
            
            <NameSearchField setName = {setName}/>
            <RatingSetField setRating = {setRating}/>
            <PriceSelectField setPrice = {setPrice}/>
            <Map setLat = {setLat} setLon = {setLon} />
            <br/> 
            <Button 
              variant="contained"
              startIcon={<SearchIcon />}
              onClick = {handleClick}
              sx = {{
                backgroundColor: primary,
                color: accent,
                margin: 10,
                textAlign: "center"
              }}
            >Search
            </Button>
        </div>
      </Container>
    </div>
  );
}
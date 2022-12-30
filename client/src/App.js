import { Box, TextField, InputLabel, MenuItem, FormControl, Select, Button, styled, Typography, Rating } from "@mui/material";
import { Add, Settings } from "@mui/icons-material";
import AcUnitIcon from '@mui/icons-material/AcUnit';
import {useState, useEffect} from 'react';
import {Venues} from './components/Venues';
// import {Map} from './components/Map';


function App() {
  // to render the data I get
  const [data, setData] = useState([{}])
  const [query, setQuery] = useState("")
  const [value, setValue] = useState(0);
  const [age, setAge] = useState('');

  const handleChange = (event) => {
    setAge(event.target.value);
  };
  const getQuery = () => setQuery("/search?" + "rating=" + "4.5");

  // to get the data from back
  useEffect(() => {
    if(query != ""){
      fetch(query).then(
        res => res.json()
      ).then(
        response => {
          setData(response)
          console.log(response)
        }
      )
    }
  }, [query])

  
  const BlueButton =  styled(Button)(({theme})=>({
    backgroundColor: theme.palette.primary,
    color: "#888",
    margin:5,
    "&:hover":{
      backgroundColor: "primary",
    },
    "&:disabled":{
      backgroundColor: "gray",
      color:'white'
    }
  }))

  return (
    <div>
      <Box
        sx={{
          '& .MuiTextField-root': { m: 1, width: '25ch' },
        }}
      >
        <TextField
          id="standard-search"
          label="Search field"
          type="search"
          variant="standard"
          helperText="Input the venue name"
        />

        <Typography component="legend">Rating</Typography>
        <Rating
        name="simple-controlled"
        value={value}
        onChange={(event, newValue) => {
          setValue(newValue);
        }}
      />

        <Typography component="legend">Price</Typography>
            <FormControl sx={{ m: 1, minWidth: 120 }}>
              <InputLabel id="demo-simple-select-label">Age</InputLabel>
                <Select
                  labelId="demo-simple-select-label"
                  id="demo-simple-select"
                  value={age}
                  label="Age"
                  onChange={handleChange}
                >
                  <MenuItem value={10}>Ten</MenuItem>
                  <MenuItem value={20}>Twenty</MenuItem>
                  <MenuItem value={30}>Thirty</MenuItem>
                </Select>
            </FormControl>

        <Typography component="legend">Pick up venues with in 5km radius from the point.</Typography>
        {/* <Map></Map> */}
    </Box>
      <Venues venues = {data}></Venues>
      <BlueButton 
        variant="contained"
        startIcon={<AcUnitIcon />}
        onClick={getQuery}
        >getQUery</BlueButton>
      {/* <BlueButton
      variant="contained"
      >here</BlueButton>
      <BlueButton
      variant="contained"
      >here</BlueButton>
      <BlueButton
      variant="contained"
      >here</BlueButton>
      <Button variant="contained" color="secondary">Contained</Button>
      <Button variant="outlined" color="secondary">Outlined</Button>
      <Typography variant="h1" component="p">
        This is p tag but with h1 font.
      </Typography>; */}
    </div>
  );
}

export default App;

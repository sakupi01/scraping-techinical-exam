import {InputLabel, MenuItem, FormControl, Select, Typography} from "@mui/material";
import {useState} from 'react';

export default function NameSearchField(props) {
  const[value, setValue] = useState("")

  const handlePrice = (event) => {
    setValue(event.target.value)
    props.setPrice([true, "price_type", event.target.value]);
  };

  return (
    <div>
      <Typography component="legend">Price</Typography>
            <FormControl sx={{ m: 1, minWidth: 120 }}>
              <InputLabel id="simple-select">Price</InputLabel>
                <Select
                  labelId="simple-select"
                  value={value}
                  label="Price"
                  onChange={handlePrice}
                >
                  <MenuItem value={"$"}>$</MenuItem>
                  <MenuItem value={"$$"}>$$</MenuItem>
                  <MenuItem value={"$$$"}>$$$</MenuItem>
                  <MenuItem value={"$$$$"}>$$$$</MenuItem>
                </Select>
            </FormControl>
    </div>
  );
}
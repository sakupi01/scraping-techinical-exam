import {TextField} from "@mui/material";

export default function NameSearchField(props) {
  const handleName = (event) => {
    props.setName([true, "name", event.target.value]);
  };
  return (
    <TextField
          id="standard-search"
          label="Search field"
          type="search"
          variant="standard"
          helperText="Input the venue name"
          onChange={handleName}
          sx = {{
            margin: 5
          }}
        />
  );
}
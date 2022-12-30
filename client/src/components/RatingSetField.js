import {Rating, Typography} from "@mui/material";

export default function NameSearchField(props) {
  const handleRating = (event) => {
    props.setRating([true , "rating", event.target.value]);
  };
  return (
    <div>
      <Typography component="legend">Rating</Typography>
        <Rating
        name="simple-controlled"
        onChange={handleRating}
        sx = {{
          margin: 5
        }}
      />
    </div>
  );
}
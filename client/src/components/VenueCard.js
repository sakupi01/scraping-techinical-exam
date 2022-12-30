import * as React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

// const bull = (
//   <Box
//     component="span"
//     sx={{ display: 'inline-block', mx: '2px', transform: 'scale(0.8)' }}
//   >
//     •
//   </Box>
// );

export default function VenueCard(props) {
  console.log(props.venue)
  return (
    <Card sx={{ minWidth: 275 }}>
      <CardContent>
        <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
          {props.venue.name}
        </Typography>
        <Typography variant="h5" component="div">
          {props.venue.rating}
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          {props.venue.price}
        </Typography>
        <Typography variant="body2">
          {props.venue.address}
          <br />
          {'"a benevolent smile"'}
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small" href={props.venue.url}>Learn More</Button>
      </CardActions>
    </Card>
  );
}
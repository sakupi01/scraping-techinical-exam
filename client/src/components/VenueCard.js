import * as React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';


export default function VenueCard(props) {
  console.log(props.venue)
  const primary = '#F2EDEB';
  const accent = '#F25041';

  return (
    <Card sx={{ minWidth: 275 }} style={{backgroundColor: primary, color: accent}}>
      <CardContent>
        <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
          Price : {props.venue.price}
        </Typography>
        <Typography variant="h5" component="div">
          {props.venue.name}
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          Rating : {props.venue.rating}
        </Typography>
        <Typography variant="body2">
          {props.venue.address}
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small" href={props.venue.url}>Go to Yelp</Button>
      </CardActions>
    </Card>
  );
}
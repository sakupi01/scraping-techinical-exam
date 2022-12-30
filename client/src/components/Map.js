import GoogleMapReact from 'google-map-react';
import {Typography} from "@mui/material";

export default function Map(props) {
  const defaultLatLng = {
    lat: 35.7022589,
    lng: 139.7744733,
  };

  const setLatLng = ({ x, y, lat, lng, event }) => {
    console.log(lat);
    console.log(lng);
    props.setLat([true, "latitude", lat]);
    props.setLon([true, "longtitude", lng]);
  };

  return (
    <div style={{ height: '300px', width: '300px' , margin:'10px'}}>
      <Typography component="legend">Pick up venues with in 5km radius from the point.</Typography>
      <GoogleMapReact
        bootstrapURLKeys={{ key: "AIzaSyBgcU7jcXKTAPKA3pEHAn0Ie9Vrili52WA" }}
        defaultCenter={defaultLatLng}
        defaultZoom={16}
        onClick={setLatLng}
       />
    </div>
  );
}
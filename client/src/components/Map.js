import GoogleMapReact from 'google-map-react';
import {Typography} from "@mui/material";
import { useState } from 'react';

export default function Map(props) {

  const [map, setMap] = useState(null);
  const [maps, setMaps] = useState(null);
  const [marker, setMarker] = useState(null);

  const defaultLatLng = {
    lat: -33.88238357028154,
    lng: 151.20588590459812,
  };

  // map, maps で受け取ると変数が被るので object で受け取っています
  const handleApiLoaded = (object) => {
    setMap(object.map);
    setMaps(object.maps);
  };


  const setLatLng = ({ x, y, lat, lng, event }) => {
    if (marker) {
      marker.setMap(null);
    }
    const latLng = {
      lat,
      lng,
    };
    setMarker(new maps.Marker({
      map,
      position: latLng,
    }));
    map.panTo(latLng);
    console.log(lat);
    console.log(lng);
    props.setLat([true, "latitude", lat]);
    props.setLon([true, "longtitude", lng]);
  };

  return (
    <div style={{ height: '300px', width: '300px' , marginTop:'30px'}}>
      <Typography component="legend">Pick up venues with in 5km radius from the point.</Typography>
      <GoogleMapReact
        bootstrapURLKeys={{ key: "AIzaSyBgcU7jcXKTAPKA3pEHAn0Ie9Vrili52WA" }}
        defaultCenter={defaultLatLng}
        defaultZoom={16}
        onClick={setLatLng}
        onGoogleApiLoaded={handleApiLoaded}
       />
    </div>
  );
}
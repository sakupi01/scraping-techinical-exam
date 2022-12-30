import React from "react";

export const Venues = ({ venues }) => {
  return (
    <ul>
      {venues.map((venue) => (
        <li key={venue.name}>{venue.name}</li>
      ))}
    </ul>
    )
}
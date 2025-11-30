import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icon missing in Leaflet + Webpack/Vite
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

function ChangeView({ center, zoom }) {
  const map = useMap();
  map.setView(center, zoom);
  return null;
}

const SafeMap = ({ center, markers, policeStations = [], restaurants = [], stores = [] }) => {
  return (
    <div className="map-container">
      <MapContainer center={center} zoom={15} scrollWheelZoom={true} style={{ height: "100%", width: "100%" }}>
        <ChangeView center={center} zoom={15} />
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {markers.map((marker, idx) => (
          <Marker key={`marker-${idx}`} position={marker.position}>
            <Popup>
              {marker.content}
            </Popup>
          </Marker>
        ))}

        {/* Police Stations */}
        {policeStations.map((station, idx) => (
          <Marker
            key={`police-${idx}`}
            position={[station.lat, station.lng]}
            icon={new L.Icon({
              iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
              shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
              iconSize: [25, 41],
              iconAnchor: [12, 41],
              popupAnchor: [1, -34],
              shadowSize: [41, 41]
            })}
          >
            <Popup>
              <strong>{station.name}</strong><br />
              {station.type}<br />
              {station.address}
            </Popup>
          </Marker>
        ))}

        {/* Restaurants */}
        {restaurants.map((place, idx) => (
          <Marker
            key={`restaurant-${idx}`}
            position={[place.lat, place.lng]}
            icon={new L.Icon({
              iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
              shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
              iconSize: [25, 41],
              iconAnchor: [12, 41],
              popupAnchor: [1, -34],
              shadowSize: [41, 41]
            })}
          >
            <Popup>
              <strong>{place.name}</strong><br />
              {place.type}<br />
              Rating: {place.rating}
            </Popup>
          </Marker>
        ))}

        {/* Convenience Stores */}
        {stores.map((store, idx) => (
          <Marker
            key={`store-${idx}`}
            position={[store.lat, store.lng]}
            icon={new L.Icon({
              iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png',
              shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
              iconSize: [25, 41],
              iconAnchor: [12, 41],
              popupAnchor: [1, -34],
              shadowSize: [41, 41]
            })}
          >
            <Popup>
              <strong>{store.name}</strong><br />
              {store.type}
            </Popup>
          </Marker>
        ))}

        {/* Current Location Marker */}
        <Marker position={center} icon={new L.Icon({
          iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
          shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
          iconSize: [25, 41],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowSize: [41, 41]
        })}>
          <Popup>Target Location</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
};

export default SafeMap;

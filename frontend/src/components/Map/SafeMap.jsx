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

const SafeMap = ({ center, markers }) => {
  return (
    <div className="map-container">
      <MapContainer center={center} zoom={15} scrollWheelZoom={true} style={{ height: "100%", width: "100%" }}>
        <ChangeView center={center} zoom={15} />
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {markers.map((marker, idx) => (
          <Marker key={idx} position={marker.position}>
            <Popup>
              {marker.content}
            </Popup>
          </Marker>
        ))}
        
        {/* Current Location Marker */}
        <Marker position={center}>
            <Popup>Target Location</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
};

export default SafeMap;

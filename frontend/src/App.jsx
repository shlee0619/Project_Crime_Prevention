import React, { useState, useEffect } from 'react';
import SafeMap from './components/Map/SafeMap';
import ScoreCard from './components/ScoreCard';
import SurroundingInfo from './components/SurroundingInfo';
import './index.css';

function App() {
    const [center, setCenter] = useState([37.5665, 126.9780]); // Seoul City Hall
    const [markers, setMarkers] = useState([]);
    const [policeStations, setPoliceStations] = useState([]);
    const [restaurants, setRestaurants] = useState([]);
    const [stores, setStores] = useState([]);
    const [scoreData, setScoreData] = useState(null);
    const [address, setAddress] = useState('');

    // Mock data for initial display
    useEffect(() => {
        // Example initial data
        setPoliceStations([
            { name: 'Seoul Jongno Police Station', lat: 37.5756, lng: 126.9848, type: 'Police Station', address: 'Jongno-gu, Seoul' }
        ]);
        setRestaurants([
            { name: 'Gwangjang Market', lat: 37.5701, lng: 126.9997, type: 'Korean Food', rating: 4.5 }
        ]);
        setStores([
            { name: 'CU Jongno', lat: 37.5705, lng: 126.9900, type: 'Convenience Store' }
        ]);
    }, []);

    const handleSearch = (e) => {
        e.preventDefault();
        // TODO: Implement address search and fetch data from backend
        console.log('Searching for:', address);
        // Mock update for demo
        setScoreData({
            risk_score: 45,
            safety_index: 82,
            details: {
                building_name: 'Example Officetel',
                main_purpose: 'Residential',
                police_count_in_region: 3,
                nearest_store_km: 0.2
            }
        });
    };

    return (
        <div className="app-container">
            <header className="header">
                <h1>Safe-Housing Map 🛡️</h1>
                <form onSubmit={handleSearch} className="search-form">
                    <input
                        type="text"
                        placeholder="Enter address..."
                        className="search-input"
                        value={address}
                        onChange={(e) => setAddress(e.target.value)}
                    />
                    <button type="submit" className="search-btn">Search</button>
                </form>
            </header>

            <main className="main-content">
                <aside className="sidebar">
                    {scoreData ? (
                        <ScoreCard data={scoreData} />
                    ) : (
                        <div className="placeholder-info">
                            <p>Search for an address or click on the map to analyze safety.</p>
                        </div>
                    )}

                    <SurroundingInfo
                        policeStations={policeStations}
                        restaurants={restaurants}
                        stores={stores}
                    />
                </aside>

                <div className="map-wrapper">
                    <SafeMap
                        center={center}
                        markers={markers}
                        policeStations={policeStations}
                        restaurants={restaurants}
                        stores={stores}
                    />
                </div>
            </main>
        </div>
    );
}

export default App;

import React, { useState } from 'react';
import axios from 'axios';
import SafeMap from './components/Map/SafeMap';
import ScoreCard from './components/ScoreCard';
import './index.css';

function App() {
    const [address, setAddress] = useState('');
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [center, setCenter] = useState([37.5665, 126.9780]); // Default Seoul

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!address) return;

        setLoading(true);
        try {
            // In production, use env var for API URL
            const response = await axios.get(`http://localhost:8000/api/risk-score?address=${address}`);
            setData(response.data);

            // Mock center update based on search (in real app, use geocoded lat/lon from response)
            // For now, we keep default or random shift to show effect if we had real geocoding
            // But response doesn't return lat/lon yet in main.py, let's add it or assume it's there.
            // I'll assume response has lat/lon or I'll just keep center for now.

        } catch (error) {
            console.error("Error fetching data:", error);
            alert("Failed to fetch data. Ensure backend is running.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">
            <header className="header">
                <h1>Safe-Housing Map</h1>
                <p>Protecting single-person households & students</p>
            </header>

            <main className="main-content">
                <div className="sidebar">
                    <form onSubmit={handleSearch} className="search-form">
                        <input
                            type="text"
                            placeholder="Enter Address (e.g., Gangnam-gu Samsung-dong)"
                            value={address}
                            onChange={(e) => setAddress(e.target.value)}
                            className="search-input"
                        />
                        <button type="submit" className="search-btn" disabled={loading}>
                            {loading ? 'Analyzing...' : 'Check Safety'}
                        </button>
                    </form>

                    {data && <ScoreCard data={data} />}

                    {!data && (
                        <div className="placeholder-info">
                            <p>Enter an address to analyze Jeonse fraud risk and safety index.</p>
                        </div>
                    )}
                </div>

                <div className="map-wrapper">
                    <SafeMap center={center} markers={[]} />
                </div>
            </main>
        </div>
    );
}

export default App;

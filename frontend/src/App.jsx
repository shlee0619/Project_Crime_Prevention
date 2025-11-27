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
            alert("데이터를 가져오는데 실패했습니다. 백엔드가 실행 중인지 확인하세요.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">
            <header className="header">
                <h1>안심 주거 지도</h1>
                <p>1인 가구 및 대학생을 위한 안전한 주거 찾기</p>
            </header>

            <main className="main-content">
                <div className="sidebar">
                    <form onSubmit={handleSearch} className="search-form">
                        <input
                            type="text"
                            placeholder="주소를 입력하세요 (예: 강남구 삼성동)"
                            value={address}
                            onChange={(e) => setAddress(e.target.value)}
                            className="search-input"
                        />
                        <button type="submit" className="search-btn" disabled={loading}>
                            {loading ? '분석 중...' : '안전도 확인'}
                        </button>
                    </form>

                    {data && <ScoreCard data={data} />}

                    {!data && (
                        <div className="placeholder-info">
                            <p>주소를 입력하여 전세 사기 위험도와 안전 지수를 확인하세요.</p>
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

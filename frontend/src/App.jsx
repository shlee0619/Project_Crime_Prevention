import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SafeMap from './components/Map/SafeMap';
import ScoreCard from './components/ScoreCard';
import './index.css';

function App() {
    const [address, setAddress] = useState('');
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [center, setCenter] = useState([37.5665, 126.9780]); // Default Seoul
    const [policeStations, setPoliceStations] = useState([]);
    const [recentSearches, setRecentSearches] = useState([]);

    useEffect(() => {
        const savedSearches = localStorage.getItem('recentSearches');
        if (savedSearches) {
            setRecentSearches(JSON.parse(savedSearches));
        }
    }, []);

    const saveSearch = (query) => {
        let searches = [...recentSearches];
        if (!searches.includes(query)) {
            searches.unshift(query);
            if (searches.length > 5) searches.pop();
            setRecentSearches(searches);
            localStorage.setItem('recentSearches', JSON.stringify(searches));
        }
    };

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!address) return;
        performSearch(address);
    };

    const performSearch = async (query) => {
        setLoading(true);
        setError(null);
        setAddress(query);

        try {
            // In production, use env var for API URL
            const response = await axios.get(`http://localhost:8000/api/risk-score?address=${query}`);
            setData(response.data);

            if (response.data.lat && response.data.lng) {
                setCenter([response.data.lat, response.data.lng]);
            }

            if (response.data.police_stations) {
                setPoliceStations(response.data.police_stations);
            } else {
                setPoliceStations([]);
            }

            saveSearch(query);

        } catch (error) {
            console.error("Error fetching data:", error);
            setError("데이터를 가져오는데 실패했습니다. 주소를 확인하거나 잠시 후 다시 시도해주세요.");
            setData(null);
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

                    {error && <div className="error-message text-red-500 mb-4 p-3 bg-red-100 rounded">{error}</div>}

                    {recentSearches.length > 0 && !data && (
                        <div className="recent-searches mb-6">
                            <h3 className="text-sm text-gray-400 mb-2">최근 검색어</h3>
                            <div className="flex flex-wrap gap-2">
                                {recentSearches.map((search, idx) => (
                                    <button
                                        key={idx}
                                        onClick={() => performSearch(search)}
                                        className="text-xs bg-gray-700 hover:bg-gray-600 px-3 py-1 rounded-full text-gray-200 transition"
                                    >
                                        {search}
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {loading && (
                        <div className="loading-spinner flex justify-center py-10">
                            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
                        </div>
                    )}

                    {data && !loading && <ScoreCard data={data} />}

                    {!data && !loading && !error && (
                        <div className="placeholder-info">
                            <p>주소를 입력하여 전세 사기 위험도와 안전 지수를 확인하세요.</p>
                        </div>
                    )}
                </div>

                <div className="map-wrapper">
                    <SafeMap center={center} markers={[]} policeStations={policeStations} />
                </div>
            </main>
        </div>
    );
}

export default App;

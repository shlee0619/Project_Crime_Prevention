import React from 'react';

const ScoreCard = ({ data }) => {
    if (!data) return null;

    const { risk_score, safety_index, details } = data;

    // Color coding
    const getRiskColor = (score) => {
        if (score < 30) return 'text-green-500';
        if (score < 70) return 'text-yellow-500';
        return 'text-red-500';
    };

    const getSafetyColor = (score) => {
        if (score > 70) return 'text-green-500';
        if (score > 30) return 'text-yellow-500';
        return 'text-red-500';
    };

    return (
        <div className="score-card glass-panel">
            <h2 className="text-xl font-bold mb-4">Safety Analysis</h2>

            <div className="score-row mb-6">
                <div className="flex justify-between items-center mb-2">
                    <span>Jeonse Fraud Risk</span>
                    <span className={`font-bold text-2xl ${getRiskColor(risk_score)}`}>{risk_score}/100</span>
                </div>
                <div className="w-full bg-gray-700 h-2 rounded-full">
                    <div className={`h-2 rounded-full ${risk_score < 30 ? 'bg-green-500' : risk_score < 70 ? 'bg-yellow-500' : 'bg-red-500'}`} style={{ width: `${risk_score}%` }}></div>
                </div>
                <p className="text-xs text-gray-400 mt-1">Higher score = Higher Risk</p>
            </div>

            <div className="score-row mb-6">
                <div className="flex justify-between items-center mb-2">
                    <span>Safety Index</span>
                    <span className={`font-bold text-2xl ${getSafetyColor(safety_index)}`}>{safety_index}/100</span>
                </div>
                <div className="w-full bg-gray-700 h-2 rounded-full">
                    <div className={`h-2 rounded-full ${safety_index > 70 ? 'bg-green-500' : safety_index > 30 ? 'bg-yellow-500' : 'bg-red-500'}`} style={{ width: `${safety_index}%` }}></div>
                </div>
                <p className="text-xs text-gray-400 mt-1">Higher score = Safer</p>
            </div>

            <div className="details text-sm text-gray-300">
                <h3 className="font-semibold mb-2 border-b border-gray-600 pb-1">Details</h3>
                <p>Building: {details.building_name}</p>
                <p>Type: {details.main_purpose}</p>
                <p>Nearest Police: {details.nearest_police_station_km} km</p>
                <p>Nearest Store: {details.nearest_store_km} km</p>
            </div>
        </div>
    );
};

export default ScoreCard;

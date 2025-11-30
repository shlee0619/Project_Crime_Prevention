import React from 'react';

const SurroundingInfo = ({ policeStations, restaurants, stores }) => {
    return (
        <div className="surrounding-info text-gray-200">
            <h2 className="text-xl font-bold mb-4">주변 정보</h2>

            <div className="mb-6">
                <h3 className="font-semibold text-blue-400 mb-2 border-b border-blue-900 pb-1">
                    👮 경찰서 / 파출소 ({policeStations.length})
                </h3>
                <ul className="space-y-2 text-sm">
                    {policeStations.length > 0 ? (
                        policeStations.map((station, idx) => (
                            <li key={idx} className="bg-gray-800 p-2 rounded">
                                <div className="font-bold">{station.name}</div>
                                <div className="text-xs text-gray-400">{station.address}</div>
                            </li>
                        ))
                    ) : (
                        <li className="text-gray-500">주변 정보 없음</li>
                    )}
                </ul>
            </div>

            <div className="mb-6">
                <h3 className="font-semibold text-green-400 mb-2 border-b border-green-900 pb-1">
                    🍽️ 맛집 ({restaurants.length})
                </h3>
                <ul className="space-y-2 text-sm">
                    {restaurants.length > 0 ? (
                        restaurants.map((place, idx) => (
                            <li key={idx} className="bg-gray-800 p-2 rounded flex justify-between items-center">
                                <div>
                                    <div className="font-bold">{place.name}</div>
                                    <div className="text-xs text-gray-400">추천 맛집</div>
                                </div>
                                <div className="text-yellow-400 font-bold">★ {place.rating}</div>
                            </li>
                        ))
                    ) : (
                        <li className="text-gray-500">주변 정보 없음</li>
                    )}
                </ul>
            </div>

            <div className="mb-6">
                <h3 className="font-semibold text-orange-400 mb-2 border-b border-orange-900 pb-1">
                    🏪 안심 편의점 ({stores.length})
                </h3>
                <ul className="space-y-2 text-sm">
                    {stores.length > 0 ? (
                        stores.map((store, idx) => (
                            <li key={idx} className="bg-gray-800 p-2 rounded">
                                <div className="font-bold">{store.name}</div>
                                <div className="text-xs text-gray-400">24시간 운영</div>
                            </li>
                        ))
                    ) : (
                        <li className="text-gray-500">주변 정보 없음</li>
                    )}
                </ul>
            </div>
        </div>
    );
};

export default SurroundingInfo;

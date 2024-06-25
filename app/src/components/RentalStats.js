import React, { useState, useEffect } from 'react';
import { getCarRentalStats } from '../services/api';
import './styles/RentalStats.css'; // Ensure your global styles are imported

const RentalStats = () => {
  const [stats, setStats] = useState([]);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await getCarRentalStats();
        setStats(response.data);
      } catch (error) {
        console.error('Error fetching rental statistics:', error);
      }
    };

    fetchStats();
  }, []);

  return (
    <div className="main-container">
      <h1>Car Rental Statistics</h1>
      <table className="stats-table">
        <thead>
          <tr>
            <th>Car Model</th>
            <th>Brand</th>
            <th>Rental Count</th>
            <th>Total Duration (days)</th>
            <th>Total Profit</th>
          </tr>
        </thead>
        <tbody>
          {stats.map((stat) => (
            <tr key={stat.car_id}>
              <td>{stat.model_name}</td>
              <td>{stat.brand_name}</td>
              <td>{stat.rental_count}</td>
              <td>{stat.total_duration}</td>
              <td>{stat.total_profit}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RentalStats;

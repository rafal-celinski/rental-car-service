// src/components/CarList.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCars } from '../services/api';
import './styles/CarList.css'; // Ensure your global styles are imported

const CarList = () => {
  const [cars, setCars] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCars = async () => {
      try {
        const response = await getCars();
        setCars(response.data);
      } catch (error) {
        console.error('Error fetching cars:', error);
      }
    };

    fetchCars();
  }, []);

  const handleRent = (carId) => {
    navigate(`/rent-car/${carId}`);
  };

  return (
    <div className="main-container">
      {cars.map((car) => (
        <div key={car.id} className="car-container">
          <h2>{car.model_name} ({car.brand_name})</h2>
          {car.photo ? <img src={car.photo} alt={`${car.model_name} image`} className="car-image" /> : <p>No image available</p>}
          <p>Segment: {car.segment_name}</p>
          <p>Production Date: {car.production_date}</p>
          <p>Mileage: {car.mileage}</p>
          <p>License Plate: {car.license_plate}</p>
          <p>VIN: {car.vin}</p>
          {car.is_rented ? (
            <button disabled>Car currently rented</button>
          ) : (
            <button onClick={() => handleRent(car.id)}>Rent this Car</button>
          )}
        </div>
      ))}
    </div>
  );
};

export default CarList;

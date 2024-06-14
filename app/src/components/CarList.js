import React, { useState, useEffect } from 'react';
import { getCars } from '../services/api';

const CarList = () => {
  const [cars, setCars] = useState([]);

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

  const handleRent = async (carId) => {
    // Logic to rent the car
  };

  return (
    <div>
      {cars.map((car) => (
        <div key={car.id}>
          <h2>{car.model_name} ({car.brand_name})</h2>
          <img src={car.photo_url} alt={`${car.model_name} image`} />
          <p>Segment: {car.segment_name}</p>
          <p>Production Date: {car.production_date}</p>
          <p>Mileage: {car.mileage}</p>
          <p>License Plate: {car.license_plate}</p>
          <p>VIN: {car.vin}</p>
          <button onClick={() => handleRent(car.id)}>Rent this Car</button>
        </div>
      ))}
    </div>
  );
};

export default CarList;

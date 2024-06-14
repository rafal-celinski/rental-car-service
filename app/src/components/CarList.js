import React, { useEffect, useState } from 'react';
import { getCars } from '../services/api';

const CarList = () => {
  const [cars, setCars] = useState([]);

  useEffect(() => {
    const fetchCars = async () => {
      try {
        const response = await getCars();
        setCars(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchCars();
  }, []);

  return (
    <div>
      <h1>Car List</h1>
      <ul>
        {cars.map(car => (
          <li key={car.id}>{car.model_name} - {car.brand_name}</li>
        ))}
      </ul>
    </div>
  );
};

export default CarList;

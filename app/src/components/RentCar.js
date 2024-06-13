import React, { useState } from 'react';
import { rentCar } from '../services/api';

const RentCar = () => {
  const [rentalData, setRentalData] = useState({
    client_id: '',
    car_id: '',
    estimated_end_date: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setRentalData({
      ...rentalData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await rentCar(rentalData);
      alert('Car rented successfully');
    } catch (error) {
      console.error(error);
      alert('Failed to rent car');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" name="client_id" placeholder="Client ID" onChange={handleChange} required />
      <input type="text" name="car_id" placeholder="Car ID" onChange={handleChange} required />
      <input type="date" name="estimated_end_date" placeholder="Estimated End Date" onChange={handleChange} required />
      <button type="submit">Rent Car</button>
    </form>
  );
};

export default RentCar;

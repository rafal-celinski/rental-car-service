import React, { useState } from 'react';
import { returnCar } from '../services/api';

const ReturnCar = () => {
  const [rentalId, setRentalId] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await returnCar(rentalId);
      alert('Car returned successfully');
    } catch (error) {
      console.error(error);
      alert('Failed to return car');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="Rental ID" value={rentalId} onChange={(e) => setRentalId(e.target.value)} required />
      <button type="submit">Return Car</button>
    </form>
  );
};

export default ReturnCar;

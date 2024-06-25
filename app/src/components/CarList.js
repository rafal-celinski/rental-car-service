import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCars, editCar, deleteCar } from '../services/api';
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

  const handleEdit = (carId) => {
    const newMileage = prompt("Enter new mileage:");
    const newLicensePlate = prompt("Enter new license plate:");
    const newVin = prompt("Enter new VIN:");

    if (newMileage && newLicensePlate && newVin) {
      const updatedCar = {
        mileage: parseInt(newMileage),
        license_plate: newLicensePlate,
        vin: newVin
      };

      editCar(carId, updatedCar)
        .then(() => {
          setCars((prevCars) => prevCars.map((car) => (car.id === carId ? { ...car, ...updatedCar } : car)));
        })
        .catch((error) => {
          console.error('Error updating car:', error);
        });
    }
  };

  const handleDelete = (carId) => {
    if (window.confirm('Are you sure you want to delete this car?')) {
      deleteCar(carId)
        .then(() => {
          setCars((prevCars) => prevCars.filter((car) => car.id !== carId));
        })
        .catch((error) => {
          console.error('Error deleting car:', error);
        });
    }
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
          <div class="button-container">
          {car.is_rented ? (
            <button disabled>Car currently rented</button>
          ) : (
            <button onClick={() => handleRent(car.id)}>Rent this Car</button>
          ) }
          <button onClick={() => handleEdit(car.id)}>Edit</button>
          {car.is_rented ? (
          <button disabled>Cannot delete</button>
          ) : 
           (<button onClick={() => handleDelete(car.id)}>Delete</button>)
          }
          </div>
        </div>
      ))}
    </div>
  );
};

export default CarList;

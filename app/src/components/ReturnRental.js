// src/components/ReturnRentalPage.js
import React, { useState, useEffect } from 'react';
import { getAllClients, getRentalsByClient, endRental, getCarDetails } from '../services/api';
import { useNavigate } from 'react-router-dom';
import './styles/ReturnRental.css';

const ReturnRentalPage = () => {
  const [clientType, setClientType] = useState('person'); // 'person' or 'company'
  const [clientIdentifier, setClientIdentifier] = useState(''); // PESEL or NIP based on clientType
  const [clients, setClients] = useState([]);
  const [client, setClient] = useState(null);
  const [rentals, setRentals] = useState([]);
  const [carDetails, setCarDetails] = useState({});

  const navigate = useNavigate();

  useEffect(() => {
    const fetchClients = async () => {
      try {
        const response = await getAllClients();
        setClients(response.data);
      } catch (error) {
        console.error('Error fetching clients:', error);
      }
    };

    fetchClients();
  }, []);

  const handleClientSearch = () => {
    let foundClient;
    if (clientType === 'person') {
      foundClient = clients.find(c => c.pesel === clientIdentifier);
    } else {
      foundClient = clients.find(c => c.nip === clientIdentifier);
    }

    if (!foundClient) {
      alert('Client not found');
      return;
    }

    setClient(foundClient);
  };

  useEffect(() => {
    if (client) {
      const fetchRentals = async () => {
        try {
          const response = await getRentalsByClient(client.id);
          setRentals(response.data);
        } catch (error) {
          console.error('Error fetching rentals:', error);
        }
      };

      fetchRentals();
    }
  }, [client]);

  useEffect(() => {
    const fetchCarDetails = async () => {
      const carDetailsMap = {};
      for (const rental of rentals) {
        try {
          const response = await getCarDetails(rental.car_id);
          carDetailsMap[rental.car_id] = response.data;
        } catch (error) {
          console.error('Error fetching car details:', error);
        }
      }
      setCarDetails(carDetailsMap);
    };

    if (rentals.length > 0) {
      fetchCarDetails();
    }
  }, [rentals]);

  const handleReturn = async (rentalId) => {
    try {
      await endRental(rentalId);
      alert('Rental ended successfully');
      navigate('/return-rental');
    } catch (error) {
      console.error('Error ending rental:', error);
      alert('Failed to end rental');
    }
  };

  return (
    <div className="return-rental-container">
      <h2>Return Rental</h2>
      <div className="client-search">
        <label>Client Type:</label>
        <select value={clientType} onChange={(e) => setClientType(e.target.value)}>
          <option value="person">Person</option>
          <option value="company">Company</option>
        </select>
      </div>
      <div className="client-search">
        <label>{clientType === 'person' ? 'PESEL' : 'NIP'}:</label>
        <input
          type="text"
          value={clientIdentifier}
          onChange={(e) => setClientIdentifier(e.target.value)}
        />
      </div>
      <button onClick={handleClientSearch}>Search Client</button>

      {client && (
        <div>
          <h3>Active Rentals for {client.name}</h3>
          {rentals.length > 0 ? (
            rentals.map((rental) => (
              <div key={rental.id} className="rental-details">
                {carDetails[rental.car_id] ? (
                  <div className="car-container">
                    <h2>{carDetails[rental.car_id].model_name} ({carDetails[rental.car_id].brand_name})</h2>
                    {carDetails[rental.car_id].photo ? (
                      <img
                        src={carDetails[rental.car_id].photo}
                        alt={`${carDetails[rental.car_id].model_name} image`}
                        className="car-image"
                      />
                    ) : (
                      <p>No image available</p>
                    )}
                    <p>Segment: {carDetails[rental.car_id].segment_name}</p>
                    <p>Production Date: {carDetails[rental.car_id].production_date}</p>
                    <p>Mileage: {carDetails[rental.car_id].mileage}</p>
                    <p>License Plate: {carDetails[rental.car_id].license_plate}</p>
                    <p>VIN: {carDetails[rental.car_id].vin}</p>
                  </div>
                ) : (
                  <p>Loading car details...</p>
                )}
                <p>Start Date: {rental.start_date}</p>
                <p>Estimated End Date: {rental.end_date}</p>
                <button onClick={() => handleReturn(rental.id)}>Return this Car</button>
              </div>
            ))
          ) : (
            <p>No active rentals found for this client.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default ReturnRentalPage;

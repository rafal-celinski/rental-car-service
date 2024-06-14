// src/components/ReturnRentalPage.js
import React, { useState, useEffect } from 'react';
import { getAllClients, getRentalsByClient, endRental } from '../services/api';
import { useNavigate } from 'react-router-dom';

const ReturnRentalPage = () => {
  const [clientType, setClientType] = useState('person'); // 'person' or 'company'
  const [clientIdentifier, setClientIdentifier] = useState(''); // PESEL or NIP based on clientType
  const [clients, setClients] = useState([]);
  const [client, setClient] = useState(null);
  const [rentals, setRentals] = useState([]);

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

  const handleReturn = async (rentalId) => {
    try {
      await endRental(rentalId);
      alert('Rental ended successfully');
      navigate('/car-list');
    } catch (error) {
      console.error('Error ending rental:', error);
      alert('Failed to end rental');
    }
  };

  return (
    <div>
      <h2>Return Rental</h2>
      <div>
        <label>Client Type:</label>
        <select value={clientType} onChange={(e) => setClientType(e.target.value)}>
          <option value="person">Person</option>
          <option value="company">Company</option>
        </select>
      </div>
      <div>
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
              <div key={rental.id}>
                <p>Car ID: {rental.car_id}</p>
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

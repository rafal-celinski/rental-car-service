import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { rentCar, getAllClients } from '../services/api';

const RentCarPage = () => {
  const { carId } = useParams();
  const navigate = useNavigate();
  const [estimatedEndDate, setEstimatedEndDate] = useState('');
  const [clientType, setClientType] = useState('person'); // 'person' or 'company'
  const [clientIdentifier, setClientIdentifier] = useState(''); // PESEL or NIP based on clientType
  const [clients, setClients] = useState([]);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    let client;
    if (clientType === 'person') {
      client = clients.find(c => c.pesel === clientIdentifier);
    } else {
      client = clients.find(c => c.nip === clientIdentifier);
    }

    if (!client) {
      alert('Client not found');
      return;
    }

    try {
      const rentalData = {
        client_id: client.id,
        car_id: carId,
        estimated_end_date: estimatedEndDate,
      };
      await rentCar(rentalData);
      alert('Car rented successfully');
      navigate('/car-list'); // Navigate back to CarList after successful rental
    } catch (error) {
      console.error('Error renting car:', error);
      alert('Failed to rent car');
    }
  };

  return (
    <div>
      <h2>Rent Car</h2>
      <form onSubmit={handleSubmit}>
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
        <div>
          <label>Estimated End Date:</label>
          <input
            type="date"
            value={estimatedEndDate}
            onChange={(e) => setEstimatedEndDate(e.target.value)}
          />
        </div>
        <button type="submit">Rent Car</button>
      </form>
    </div>
  );
};

export default RentCarPage;

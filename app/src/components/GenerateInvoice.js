import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { generateInvoice, getAllClients } from '../services/api';

const GenerateInvoicePage = () => {
  const [clientType, setClientType] = useState('person'); // 'person' or 'company'
  const [clientIdentifier, setClientIdentifier] = useState(''); // PESEL or NIP based on clientType
  const [clients, setClients] = useState([]);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
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
      const invoiceData = {
        client_id: client.id,
        start_date: startDate,
        end_date: endDate,
      };
      await generateInvoice(invoiceData);
      alert('Invoice generated successfully');
      navigate('/invoices');
    } catch (error) {
      console.error('Error generating invoice:', error);
      alert('Failed to generate invoice');
    }
  };

  return (
    <div>
      <h2>Generate Invoice</h2>
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
          <label>Start Date:</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </div>
        <div>
          <label>End Date:</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </div>
        <button type="submit">Generate Invoice</button>
      </form>
    </div>
  );
};

export default GenerateInvoicePage;

// In src/components/GenerateInvoice.js

import React, { useState } from 'react';
import { generateInvoice, getAllClients } from '../services/api';

const GenerateInvoice = () => {
  const [clientType, setClientType] = useState('person'); // 'person' or 'company'
  const [clientIdentifier, setClientIdentifier] = useState(''); // PESEL or NIP based on clientType
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleGenerateInvoice = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    let client;
    try {
      const clients = await getAllClients();
      if (clientType === 'person') {
        client = clients.data.find(c => c.pesel === clientIdentifier);
      } else {
        client = clients.data.find(c => c.nip === clientIdentifier);
      }

      if (!client) {
        setError('Client not found');
        return;
      }

      const invoiceData = {
        client_id: client.id,
        start_date: startDate,
        end_date: endDate,
      };
      await generateInvoice(invoiceData);
      setSuccess('Invoice generated successfully.');
    } catch (err) {
      if (err.response && err.response.data.detail === "No rentals found in the specified date window.") {
        setError('No rentals found in the specified date window.');
      } else {
        setError('Failed to generate invoice');
      }
    }
  };

  return (
    <div>
      <h2>Generate Invoice</h2>
      <form onSubmit={handleGenerateInvoice}>
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
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}
    </div>
  );
};

export default GenerateInvoice;

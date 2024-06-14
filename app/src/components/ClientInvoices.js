// In src/components/ClientInvoices.js

import React, { useState, useEffect } from 'react';
import { getAllClients, getInvoicesByClient, getInvoiceElements } from '../services/api';

const ClientInvoices = () => {
  const [clientType, setClientType] = useState('person'); // 'person' or 'company'
  const [clientIdentifier, setClientIdentifier] = useState(''); // PESEL or NIP based on clientType
  const [clients, setClients] = useState([]);
  const [invoices, setInvoices] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchClients = async () => {
      try {
        const response = await getAllClients();
        setClients(response.data);
      } catch (err) {
        setError('Error fetching clients');
      }
    };

    fetchClients();
  }, []);

  const handleFetchInvoices = async () => {
    let client;
    if (clientType === 'person') {
      client = clients.find(c => c.pesel === clientIdentifier);
    } else {
      client = clients.find(c => c.nip === clientIdentifier);
    }

    if (!client) {
      setError('Client not found');
      return;
    }

    try {
      const response = await getInvoicesByClient(client.id);
      const invoicesWithElements = await Promise.all(response.data.map(async (invoice) => {
        const elementsResponse = await getInvoiceElements(invoice.id);
        return { ...invoice, elements: elementsResponse.data };
      }));
      setInvoices(invoicesWithElements);
      setError('');
    } catch (err) {
      console.error('Error fetching invoices:', err);
      setError('Error fetching invoices');
    }
  };

  return (
    <div>
      <h2>Client Invoices</h2>
      {error && <p>{error}</p>}
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
        <button onClick={handleFetchInvoices}>Fetch Invoices</button>
      </div>
      <ul>
        {invoices.map((invoice) => (
          <li key={invoice.id}>
            <p>Date: {invoice.date}</p>
            <p>Price Sum Netto: {invoice.price_sum_netto}</p>
            <p>Tax: {invoice.tax}</p>
            <h4>Invoice Elements:</h4>
            <ul>
              {invoice.elements && invoice.elements.map((element) => (
                <li key={element.id}>
                  <p>Price: {element.price}</p>
                  <p>Car: {element.car ? `${element.car.model_name} (${element.car.brand_name})` : 'Car details unavailable'}</p>
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ClientInvoices;

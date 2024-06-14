import React, { useState } from 'react';
import { createClient } from '../services/api';

const ClientAdd = () => {
  const [clientType, setClientType] = useState('person'); // 'person' or 'company'
  const [name, setName] = useState('');
  const [surname, setSurname] = useState('');
  const [address, setAddress] = useState('');
  const [pesel, setPesel] = useState('');
  const [nip, setNip] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    const clientData = {
      name,
      address,
      surname: clientType === 'person' ? surname : undefined,
      pesel: clientType === 'person' ? pesel : undefined,
      nip: clientType === 'company' ? nip : undefined,
    };

    try {
      await createClient(clientData);
      setSuccess('Client created successfully.');
      setName('');
      setSurname('');
      setAddress('');
      setPesel('');
      setNip('');
    } catch (err) {
      setError('Failed to create client');
    }
  };

  return (
    <div>
      <h2>Add Client</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Client Type:</label>
          <select value={clientType} onChange={(e) => setClientType(e.target.value)}>
            <option value="person">Person</option>
            <option value="company">Company</option>
          </select>
        </div>
        <div>
          <label>Name:</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        <div>
          <label>Address:</label>
          <input
            type="text"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
          />
        </div>
        {clientType === 'person' && (
          <>
            <div>
              <label>Surname:</label>
              <input
                type="text"
                value={surname}
                onChange={(e) => setSurname(e.target.value)}
              />
            </div>
            <div>
              <label>PESEL:</label>
              <input
                type="text"
                value={pesel}
                onChange={(e) => setPesel(e.target.value)}
              />
            </div>
          </>
        )}
        {clientType === 'company' && (
          <div>
            <label>NIP:</label>
            <input
              type="text"
              value={nip}
              onChange={(e) => setNip(e.target.value)}
            />
          </div>
        )}
        <button type="submit">Add Client</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}
    </div>
  );
};

export default ClientAdd;

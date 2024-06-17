import React, { useState, useEffect } from 'react';
import { getAllClients, createClient, updateClient, deleteClient } from '../services/api';

const ClientManagement = () => {
  const [clients, setClients] = useState([]);
  const [newClient, setNewClient] = useState({ name: '', surname: '', address: '', pesel: '', nip: '' });
  const [editingClient, setEditingClient] = useState(null);
  const [editClientData, setEditClientData] = useState({ name: '', surname: '', address: '' });

  useEffect(() => {
    const fetchClients = async () => {
      const response = await getAllClients();
      setClients(response.data);
    };
    fetchClients();
  }, []);

  const handleCreateClient = async () => {
    await createClient(newClient);
    setNewClient({ name: '', surname: '', address: '', pesel: '', nip: '' });
    const response = await getAllClients();
    setClients(response.data);
  };

  const handleUpdateClient = async (clientId) => {
    await updateClient(clientId, editClientData);
    setEditingClient(null);
    const response = await getAllClients();
    setClients(response.data);
  };

  const handleDeleteClient = async (clientId) => {
    await deleteClient(clientId);
    const response = await getAllClients();
    setClients(response.data);
  };

  return (
    <div>
      <h2>Client Management</h2>
      <div>
        <h3>Add New Client</h3>
        <input
          type="text"
          placeholder="Name"
          value={newClient.name}
          onChange={(e) => setNewClient({ ...newClient, name: e.target.value })}
        />
        <input
          type="text"
          placeholder="Surname"
          value={newClient.surname}
          onChange={(e) => setNewClient({ ...newClient, surname: e.target.value })}
        />
        <input
          type="text"
          placeholder="Address"
          value={newClient.address}
          onChange={(e) => setNewClient({ ...newClient, address: e.target.value })}
        />
        <input
          type="text"
          placeholder="PESEL"
          value={newClient.pesel}
          onChange={(e) => setNewClient({ ...newClient, pesel: e.target.value })}
        />
        <input
          type="text"
          placeholder="NIP"
          value={newClient.nip}
          onChange={(e) => setNewClient({ ...newClient, nip: e.target.value })}
        />
        <button onClick={handleCreateClient}>Add Client</button>
      </div>
      <div>
        <h3>Clients</h3>
        <ul>
          {clients.map((client) => (
            <li key={client.id}>
              {editingClient === client.id ? (
                <>
                  <input
                    type="text"
                    value={editClientData.name}
                    onChange={(e) => setEditClientData({ ...editClientData, name: e.target.value })}
                  />
                  {client.pesel && (
                    <input
                      type="text"
                      value={editClientData.surname}
                      onChange={(e) => setEditClientData({ ...editClientData, surname: e.target.value })}
                    />
                  )}
                  <input
                    type="text"
                    value={editClientData.address}
                    onChange={(e) => setEditClientData({ ...editClientData, address: e.target.value })}
                  />
                  <button onClick={() => handleUpdateClient(client.id)}>Save</button>
                </>
              ) : (
                <>
                  <p>{client.name} {client.surname && client.surname} - {client.address}</p>
                  <button onClick={() => { setEditingClient(client.id); setEditClientData({ name: client.name, surname: client.surname || '', address: client.address }); }}>Edit</button>
                  <button onClick={() => handleDeleteClient(client.id)}>Delete</button>
                </>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ClientManagement;
  
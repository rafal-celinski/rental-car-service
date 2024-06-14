import React, { useState, useEffect } from 'react';
import { getAllPrices, createOrUpdatePrice, deletePrice } from '../services/api';

const PriceManager = () => {
  const [prices, setPrices] = useState([]);
  const [modelName, setModelName] = useState('');
  const [brandName, setBrandName] = useState('');
  const [price, setPrice] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    const fetchPrices = async () => {
      try {
        const response = await getAllPrices();
        setPrices(response.data);
      } catch (error) {
        setError('Error fetching prices');
      }
    };

    fetchPrices();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    const priceData = {
      model_name: modelName,
      brand_name: brandName,
      price: parseFloat(price),
    };

    try {
      await createOrUpdatePrice(priceData);
      setSuccess('Price updated successfully.');
      setModelName('');
      setBrandName('');
      setPrice('');
      const response = await getAllPrices();
      setPrices(response.data);
    } catch (err) {
      setError('Failed to update price');
    }
  };

  const handleDelete = async (model_name, brand_name) => {
    try {
      await deletePrice(model_name, brand_name);
      setSuccess('Price deleted successfully.');
      const response = await getAllPrices();
      setPrices(response.data);
    } catch (err) {
      setError('Failed to delete price');
    }
  };

  return (
    <div>
      <h2>Manage Rental Prices</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Model Name:</label>
          <input
            type="text"
            value={modelName}
            onChange={(e) => setModelName(e.target.value)}
          />
        </div>
        <div>
          <label>Brand Name:</label>
          <input
            type="text"
            value={brandName}
            onChange={(e) => setBrandName(e.target.value)}
          />
        </div>
        <div>
          <label>Price:</label>
          <input
            type="number"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
          />
        </div>
        <button type="submit">Add/Update Price</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}
      <h3>Existing Prices</h3>
      <ul>
        {prices.map((price) => (
          <li key={`${price.model_name}-${price.brand_name}`}>
            {price.model_name} {price.brand_name} - {price.price}
            <button onClick={() => handleDelete(price.model_name, price.brand_name)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PriceManager;

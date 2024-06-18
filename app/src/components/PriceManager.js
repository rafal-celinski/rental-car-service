// src/components/PriceManager.js
import React, { useState, useEffect } from 'react';
import { getAllPrices, createOrUpdatePrice, deletePrice, getAvailableModels } from '../services/api';
import './styles/PriceManager.css';

const PriceManager = () => {
  const [prices, setPrices] = useState([]);
  const [price, setPrice] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [models, setModels] = useState([]);
  const [segments, setSegments] = useState([]);
  const [brands, setBrands] = useState([]);
  const [filteredModels, setFilteredModels] = useState([]);
  const [priceData, setPriceData] = useState({
    segment_name: '',
    brand_name: '',
    model_name: ''
  });

  useEffect(() => {
    const fetchPrices = async () => {
      try {
        const response = await getAllPrices();
        setPrices(response.data);
      } catch (error) {
        setError('Error fetching prices');
      }
    };

    const fetchModels = async () => {
      try {
        const response = await getAvailableModels();
        setModels(response.data);

        // Extract unique segments
        const uniqueSegments = [...new Set(response.data.map(model => model.segment_name))];
        setSegments(uniqueSegments);
      } catch (error) {
        console.error('Error fetching models:', error);
      }
    };

    fetchPrices();
    fetchModels();
  }, []);

  const handleSegmentChange = (e) => {
    const segment = e.target.value;
    setPriceData({ ...priceData, segment_name: segment, brand_name: '', model_name: '' });

    // Filter brands based on selected segment
    const uniqueBrands = [...new Set(models.filter(model => model.segment_name === segment).map(model => model.brand_name))];
    setBrands(uniqueBrands);
    setFilteredModels([]);
  };

  const handleBrandChange = (e) => {
    const brand = e.target.value;
    setPriceData({ ...priceData, brand_name: brand, model_name: '' });

    // Filter models based on selected segment and brand
    const availableModels = models.filter(model => model.segment_name === priceData.segment_name && model.brand_name === brand);
    setFilteredModels(availableModels);
  };

  const handleModelChange = (e) => {
    const model = e.target.value;
    setPriceData({ ...priceData, model_name: model });
  };

  const handleChange = (e) => {
    setPrice(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    const newPriceData = {
      model_name: priceData.model_name,
      brand_name: priceData.brand_name,
      price: parseFloat(price),
    };

    try {
      await createOrUpdatePrice(newPriceData);
      setSuccess('Price updated successfully.');
      setPriceData({
        segment_name: '',
        brand_name: '',
        model_name: ''
      });
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
    <div className="price-manager-container">
      <h2>Manage Rental Prices</h2>
      <form className="price-manager-form" onSubmit={handleSubmit}>
        <div>
          <label>Segment:</label>
          <select name="segment_name" onChange={handleSegmentChange} value={priceData.segment_name} required>
            <option value="">Select Segment</option>
            {segments.map(segment => (
              <option key={segment} value={segment}>
                {segment}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Brand Name:</label>
          <select name="brand_name" onChange={handleBrandChange} value={priceData.brand_name} disabled={!priceData.segment_name} required>
            <option value="">Select Brand</option>
            {brands.map(brand => (
              <option key={brand} value={brand}>
                {brand}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Model Name:</label>
          <select name="model_name" onChange={handleModelChange} value={priceData.model_name} disabled={!priceData.brand_name} required>
            <option value="">Select Model</option>
            {filteredModels.map(model => (
              <option key={model.model_name} value={model.model_name}>
                {model.model_name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Price:</label>
          <input
            type="number"
            value={price}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Add/Update Price</button>
      </form>
      {error && <p className="error-message">{error}</p>}
      {success && <p className="success-message">{success}</p>}
      <h3>Existing Prices</h3>
      <ul className="price-manager-list">
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

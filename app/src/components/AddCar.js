// src/components/AddCar.js

import React, { useState, useEffect } from 'react';
import { addCar, getAvailableModels } from '../services/api';
import './styles/AddCar.css';
const AddCar = () => {
  const [carData, setCarData] = useState({
    model_name: '',
    brand_name: '',
    segment_name: '',
    production_date: '',
    mileage: '',
    license_plate: '',
    vin: '',
    photo: null,
  });

  const [models, setModels] = useState([]);
  const [segments, setSegments] = useState([]);
  const [brands, setBrands] = useState([]);
  const [filteredModels, setFilteredModels] = useState([]);

  useEffect(() => {
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

    fetchModels();
  }, []);

  const handleSegmentChange = (e) => {
    const segment = e.target.value;
    setCarData({ ...carData, segment_name: segment, brand_name: '', model_name: '' });

    const uniqueBrands = [...new Set(models.filter(model => model.segment_name === segment).map(model => model.brand_name))];
    setBrands(uniqueBrands);
    setFilteredModels([]);
  };

  const handleBrandChange = (e) => {
    const brand = e.target.value;
    setCarData({ ...carData, brand_name: brand, model_name: '' });

    const availableModels = models.filter(model => model.segment_name === carData.segment_name && model.brand_name === brand);
    setFilteredModels(availableModels);
  };

  const handleModelChange = (e) => {
    const model = e.target.value;
    setCarData({ ...carData, model_name: model });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCarData({ ...carData, [name]: value });
  };

  const handleFileChange = (e) => {
    setCarData({ ...carData, photo: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('model_name', carData.model_name);
    formData.append('brand_name', carData.brand_name);
    formData.append('segment_name', carData.segment_name);
    formData.append('production_date', carData.production_date);
    formData.append('mileage', carData.mileage);
    formData.append('license_plate', carData.license_plate);
    formData.append('vin', carData.vin);
    formData.append('photo', carData.photo);

    try {
      await addCar(formData);
      alert('Car added successfully');
    } catch (error) {
      console.error('Error adding car:', error);
      alert('Failed to add car');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <select name="segment_name" onChange={handleSegmentChange} value={carData.segment_name} required>
        <option value="">Select Segment</option>
        {segments.map(segment => (
          <option key={segment} value={segment}>
            {segment}
          </option>
        ))}
      </select>
      
      <select name="brand_name" onChange={handleBrandChange} value={carData.brand_name} disabled={!carData.segment_name} required>
        <option value="">Select Brand</option>
        {brands.map(brand => (
          <option key={brand} value={brand}>
            {brand}
          </option>
        ))}
      </select>
      
      <select name="model_name" onChange={handleModelChange} value={carData.model_name} disabled={!carData.brand_name} required>
        <option value="">Select Model</option>
        {filteredModels.map(model => (
          <option key={model.model_name} value={model.model_name}>
            {model.model_name}
          </option>
        ))}
      </select>

      <input 
        type="date" 
        name="production_date" 
        placeholder="Production Date" 
        onChange={handleChange} 
        required 
      />
      
      <input 
        type="number" 
        name="mileage" 
        placeholder="Mileage" 
        onChange={handleChange} 
        required 
      />
      
      <input 
        type="text" 
        name="license_plate" 
        placeholder="License Plate" 
        onChange={handleChange} 
        required 
      />
      
      <input 
        type="text" 
        name="vin" 
        placeholder="VIN" 
        onChange={handleChange} 
        required 
      />
      
      <input 
        type="file" 
        name="photo" 
        onChange={handleFileChange} 
        required 
      />
      
      <button type="submit">Add Car</button>
    </form>
  );
};

export default AddCar;

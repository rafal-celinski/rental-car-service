import React, { useState, useEffect } from 'react';
import { addCar, getAvailableModels } from '../services/api';

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

  useEffect(() => {
    // Fetch available models from the API
    const fetchModels = async () => {
      try {
        const response = await getAvailableModels();
        setModels(response.data);
      } catch (error) {
        console.error('Error fetching models:', error);
      }
    };

    fetchModels();
  }, []);

  const handleModelChange = (e) => {
    const value = e.target.value;
    const selectedModel = models.find(model => `${model.model_name} ${model.brand_name} (${model.segment_name})` === value);
    
    if (selectedModel) {
      setCarData({
        ...carData,
        model_name: selectedModel.model_name,
        brand_name: selectedModel.brand_name,
        segment_name: selectedModel.segment_name,
      });
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCarData({
      ...carData,
      [name]: value,
    });
  };

  const handleFileChange = (e) => {
    setCarData({
      ...carData,
      photo: e.target.files[0],
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await addCar(carData);
      alert('Car added successfully');
    } catch (error) {
      console.error(error);
      alert('Failed to add car');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <select name="model_name" onChange={handleModelChange} required>
        <option value="">Select Model</option>
        {models.map(model => (
          <option key={`${model.model_name} ${model.brand_name} (${model.segment_name})`} value={`${model.model_name} ${model.brand_name} (${model.segment_name})`}>
            {model.model_name} {model.brand_name} ({model.segment_name})
          </option>
        ))}
      </select>
      <input type="text" name="brand_name" placeholder="Brand Name" value={carData.brand_name} readOnly required />
      <input type="text" name="segment_name" placeholder="Segment Name" value={carData.segment_name} readOnly required />
      <input type="date" name="production_date" placeholder="Production Date" onChange={handleChange} required />
      <input type="number" name="mileage" placeholder="Mileage" onChange={handleChange} required />
      <input type="text" name="license_plate" placeholder="License Plate" onChange={handleChange} required />
      <input type="text" name="vin" placeholder="VIN" onChange={handleChange} required />
      <input type="file" name="photo" onChange={handleFileChange} required />
      <button type="submit">Add Car</button>
    </form>
  );
};

export default AddCar;

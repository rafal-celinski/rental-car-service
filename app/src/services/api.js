import axios from 'axios';

const API_URL = 'http://localhost:8000/api'; // Replace with your backend URL

export const registerClient = (clientData) => axios.post(`${API_URL}/clients`, clientData);
export const getCars = () => axios.get(`${API_URL}/cars/`);
export const getCarDetails = (carId) => axios.get(`${API_URL}/cars/${carId}`);
export const addCar = (carData) => axios.post(`${API_URL}/cars/`, carData, {
  headers: {
    'Content-Type': 'multipart/form-data'
  }
});
export const rentCar = (rentalData) => axios.post(`${API_URL}/rentals/`, rentalData);
export const returnCar = (rentalId) => axios.post(`${API_URL}/rentals/${rentalId}/return`);
export const getReports = (reportType, params) => axios.get(`${API_URL}/reports/${reportType}`, { params });
export const getAvailableModels = () => axios.get(`${API_URL}/models/`);
export const getImage = (filename) => axios.get(`${API_URL}/images/${filename}`);

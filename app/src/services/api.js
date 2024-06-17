import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const addCar = (carData) => axios.post(`${API_URL}/cars/`, carData, {
  headers: {
    'Content-Type': 'multipart/form-data'
  }
});

export const registerClient = (clientData) => axios.post(`${API_URL}/clients`, clientData);
export const getAllClients = () => axios.get(`${API_URL}/clients/`);
export const getCars = () => axios.get(`${API_URL}/cars/`);
export const getCarDetails = (carId) => axios.get(`${API_URL}/cars/${carId}`);
export const rentCar = (rentalData) => axios.post(`${API_URL}/rentals/`, rentalData);
export const returnCar = (rentalId) => axios.post(`${API_URL}/rentals/${rentalId}/return`);
export const getReports = (reportType, params) => axios.get(`${API_URL}/reports/${reportType}/`, { params });
export const getAvailableModels = () => axios.get(`${API_URL}/models/`);
export const getImage = (filename) => axios.get(`${API_URL}/images/${filename}`);
export const getRentalsByClient = (clientId) => axios.get(`${API_URL}/rentals/client/${clientId}`);
export const endRental = (rentalId) => axios.post(`${API_URL}/rentals/${rentalId}/return`);
export const returnRental = async (rentalId) => axios.post(`${API_URL}/rentals/${rentalId}/return`);
export const generateInvoice = (invoiceData) => axios.post(`${API_URL}/invoices/`, invoiceData);
export const getInvoicesByClient = (clientId) => axios.get(`${API_URL}/invoices/client/${clientId}`);
export const getInvoiceElements = (invoiceId) => axios.get(`${API_URL}/invoices/${invoiceId}/elements`);
export const createClient = (clientData) => axios.post(`${API_URL}/clients/`, clientData);
export const createOrUpdatePrice = (priceData) => axios.post(`${API_URL}/prices/`, priceData);
export const deletePrice = (model_name, brand_name) => axios.delete(`${API_URL}/prices/${model_name}/${brand_name}`);
export const getAllPrices = () => axios.get(`${API_URL}/prices/`);
export const getMonthlyReport = (year, month) => {return axios.get(`${API_URL}/reports/monthly/`, {params: { year, month }});};
export const getYearlyReport = (year) => { return axios.get(`${API_URL}/reports/yearly/`, {params: { year }});};

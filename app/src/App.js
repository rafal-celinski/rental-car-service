// In src/App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import AddCar from './components/AddCar';
import CarList from './components/CarList';
import RentCarPage from './components/RentCar';
import ReturnRentalPage from './components/ReturnRental';
import ClientInvoices from './components/ClientInvoices';
import GenerateInvoice from './components/GenerateInvoice';
import PriceManager from './components/PriceManager';
import { MonthlyReportPage, YearlyReportPage } from './components/Report';
import ClientManagement from './components/ClientManagement';
import './components/styles/App.css';
import logo from './components/images/logo.png';



const App = () => {
  return (
    <Router>
      <div className="main-container">
        <header className="header">
        <img src={logo} alt="Company Logo" className="logo" />
          <nav>
            <ul className="nav-links">
              <li><Link to="/add-car">Add Car</Link></li>
              <li><Link to="/car-list">Car List</Link></li>
              <li><Link to="/return-rental">Return Rental</Link></li>
              <li><Link to="/client-invoices/:clientId">Client Invoices</Link></li>
              <li><Link to="/generate-invoice">Generate Invoice</Link></li>
              <li><Link to="/manage-prices">Manage Prices</Link></li>
              <li><Link to="/monthly-report">Monthly Report</Link></li>
              <li><Link to="/yearly-report">Yearly Report</Link></li>
              <li><Link to="/client-management">Client Management</Link></li>
            </ul>
          </nav>

        </header>
        <main>
          <Routes>
            <Route path="/add-car" element={<AddCar />} />
            <Route path="/car-list" element={<CarList />} />
            <Route path="/rent-car/:carId" element={<RentCarPage />} />
            <Route path="/return-rental" element={<ReturnRentalPage />} />
            <Route path="/client-invoices/:clientId" element={<ClientInvoices />} />
            <Route path="/generate-invoice" element={<GenerateInvoice />} />
            <Route path="/manage-prices" element={<PriceManager />} />
            <Route path="/monthly-report" element={<MonthlyReportPage />} />
            <Route path="/yearly-report" element={<YearlyReportPage />} />
            <Route path="/client-management" element={<ClientManagement />} />
          </Routes>
          <img src={logo} alt="Company Logo" className="main-logo" />
        </main>
      </div>
    </Router>
  );
};

export default App;

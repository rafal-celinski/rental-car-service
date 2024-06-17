// In src/App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import AddCar from './components/AddCar';
import CarList from './components/CarList';
import RentCarPage from './components/RentCarPage';
import ReturnRentalPage from './components/ReturnRentalPage';
import Reports from './components/Reports';
import ClientInvoices from './components/ClientInvoices';
import GenerateInvoice from './components/GenerateInvoice';
import PriceManager from './components/PriceManager';
import { MonthlyReportPage, YearlyReportPage } from './components/ReportPage';
import ClientManagement from './components/ClientManagementPage';

const App = () => {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li><Link to="/add-car">Add Car</Link></li>
            <li><Link to="/car-list">Car List</Link></li>
            <li><Link to="/return-rental">Return Rental</Link></li>
            <li><Link to="/reports">Reports</Link></li>
            <li><Link to="/client-invoices/:clientId">Client Invoices</Link></li>
            <li><Link to="/generate-invoice">Generate Invoice</Link></li>
            <li><Link to="/manage-prices">Manage Prices</Link></li>
            <li><Link to="/monthly-report">Monthly Report</Link></li>
            <li><Link to="/yearly-report">Yearly Report</Link></li>
            <li><Link to="/client-management">Client Management</Link></li>
          </ul>
        </nav>
        <Routes>
          <Route path="/add-car" element={<AddCar />} />
          <Route path="/car-list" element={<CarList />} />
          <Route path="/rent-car/:carId" element={<RentCarPage />} />
          <Route path="/return-rental" element={<ReturnRentalPage />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/client-invoices/:clientId" element={<ClientInvoices />} />
          <Route path="/generate-invoice" element={<GenerateInvoice />} />
          <Route path="/manage-prices" element={<PriceManager />} />
          <Route path="/monthly-report" element={<MonthlyReportPage />} />
          <Route path="/yearly-report" element={<YearlyReportPage />} />
          <Route path="/client-management" element={<ClientManagement />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;

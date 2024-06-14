import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import AddCar from './components/AddCar';
import CarList from './components/CarList';
import RentCar from './components/RentCar';
import ReturnCar from './components/ReturnCar';
import Reports from './components/Reports';

const App = () => {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li><Link to="/add-car">Add Car</Link></li>
            <li><Link to="/car-list">Car List</Link></li>
            <li><Link to="/rent-car">Rent Car</Link></li>
            <li><Link to="/return-car">Return Car</Link></li>
            <li><Link to="/reports">Reports</Link></li>
          </ul>
        </nav>
        <Routes>
          <Route path="/add-car" element={<AddCar />} />
          <Route path="/car-list" element={<CarList />} />
          <Route path="/rent-car" element={<RentCar />} />
          <Route path="/return-car" element={<ReturnCar />} />
          <Route path="/reports" element={<Reports />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;

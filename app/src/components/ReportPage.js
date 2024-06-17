import React, { useState } from 'react';
import { getMonthlyReport, getYearlyReport } from '../services/api';

const MonthlyReportPage = () => {
  const [year, setYear] = useState('');
  const [month, setMonth] = useState('');
  const [report, setReport] = useState(null);
  const [error, setError] = useState('');

  const handleFetchReport = async () => {
    try {
      const response = await getMonthlyReport(year, month);
      setReport(response.data);
      setError('');
    } catch (err) {
      setError('No data found for the given month and year');
      setReport(null);
    }
  };

  return (
    <div>
      <h2>Monthly Report</h2>
      <input type="number" placeholder="Year" value={year} onChange={e => setYear(e.target.value)} />
      <input type="number" placeholder="Month" value={month} onChange={e => setMonth(e.target.value)} />
      <button onClick={handleFetchReport}>Get Report</button>
      {error && <p>{error}</p>}
      {report && (
        <div>
          <p>Total Rentals: {report.total_rentals}</p>
          <p>Total Revenue: {report.total_revenue}</p>
          <p>Total Clients: {report.total_clients}</p>
        </div>
      )}
    </div>
  );
};

const YearlyReportPage = () => {
  const [year, setYear] = useState('');
  const [report, setReport] = useState(null);
  const [error, setError] = useState('');

  const handleFetchReport = async () => {
    try {
      const response = await getYearlyReport(year);
      setReport(response.data);
      setError('');
    } catch (err) {
      setError('No data found for the given year');
      setReport(null);
    }
  };

  return (
    <div>
      <h2>Yearly Report</h2>
      <input type="number" placeholder="Year" value={year} onChange={e => setYear(e.target.value)} />
      <button onClick={handleFetchReport}>Get Report</button>
      {error && <p>{error}</p>}
      {report && (
        <div>
          <p>Total Rentals: {report.total_rentals}</p>
          <p>Total Revenue: {report.total_revenue}</p>
          <p>Total Clients: {report.total_clients}</p>
        </div>
      )}
    </div>
  );
};

export { MonthlyReportPage, YearlyReportPage };

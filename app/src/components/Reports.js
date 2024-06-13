import React, { useState, useEffect } from 'react';
import { getReports } from '../services/api';

const Reports = () => {
  const [reportType, setReportType] = useState('monthly');
  const [reports, setReports] = useState([]);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const response = await getReports(reportType);
        setReports(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchReports();
  }, [reportType]);

  return (
    <div>
      <h1>{reportType.charAt(0).toUpperCase() + reportType.slice(1)} Reports</h1>
      <select value={reportType} onChange={(e) => setReportType(e.target.value)}>
        <option value="monthly">Monthly</option>
        <option value="yearly">Yearly</option>
      </select>
      <ul>
        {reports.map(report => (
          <li key={report.id}>{report.description}</li>
        ))}
      </ul>
    </div>
  );
};

export default Reports;

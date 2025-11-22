import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import SectorCard from './SectorCard';
import { useTheme } from '../context/ThemeContext';
import apiService from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const { theme } = useTheme();
  const [sectors, setSectors] = useState([
    { id: 'hr', name: 'HR', icon: '👥' },
    { id: 'sales', name: 'Sales', icon: '💰' },
    { id: 'service', name: 'Customer Service', icon: '🎧' },
    { id: 'finance', name: 'Finance', icon: '💵' }
  ]);
  const [dashboardData, setDashboardData] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const sectorsList = ['hr', 'sales', 'service', 'finance'];
      const data = {};
      
      for (const sector of sectorsList) {
        try {
          const response = await apiService.getDashboardData(sector);
          data[sector] = response.data;
        } catch (error) {
          console.error(`Error loading ${sector} data:`, error);
          // Use default data if API fails
          data[sector] = getDefaultData(sector);
        }
      }
      
      setDashboardData(data);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getDefaultData = (sector) => {
    const defaults = {
      hr: { metrics: { total_employees: 1250, attrition_rate: 8.5 } },
      sales: { metrics: { total_pipeline_value: 2500000, deals_closed: 45 } },
      service: { metrics: { open_tickets: 234, avg_response_time: 2.5 } },
      finance: { metrics: { total_revenue: 4500000, cash_flow: 1250000 } }
    };
    return defaults[sector] || {};
  };

  return (
    <div className={`dashboard ${theme}`}>
      <motion.div
        className="dashboard-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="dashboard-title">
          <span className="title-icon">🚀</span>
          OrchestrateIQ
        </h1>
        <p className="dashboard-subtitle">AI-Powered Business Command Center</p>
      </motion.div>

      {loading ? (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading dashboard data...</p>
        </div>
      ) : (
        <div className="sectors-grid">
          {sectors.map((sector, index) => (
            <motion.div
              key={sector.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <SectorCard
                sector={sector}
                data={dashboardData[sector.id]}
                theme={theme}
              />
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;


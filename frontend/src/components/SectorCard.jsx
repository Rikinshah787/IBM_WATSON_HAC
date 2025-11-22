import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, AlertCircle, Activity } from 'lucide-react';
import Visualizations from './Visualizations';
import './SectorCard.css';

const SectorCard = ({ sector, data, theme }) => {
  const metrics = data?.metrics || {};
  const alerts = data?.alerts || [];
  const trends = data?.trends || [];

  const formatNumber = (num) => {
    if (num >= 1000000) return `$${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `$${(num / 1000).toFixed(1)}K`;
    return num?.toLocaleString() || '0';
  };

  return (
    <motion.div
      className={`sector-card ${theme}`}
      whileHover={{ scale: 1.02, y: -5 }}
      transition={{ duration: 0.2 }}
    >
      <div className="sector-header">
        <div className="sector-icon">{sector.icon}</div>
        <h3 className="sector-name">{sector.name}</h3>
      </div>

      <div className="sector-metrics">
        {Object.entries(metrics).slice(0, 2).map(([key, value]) => (
          <div key={key} className="metric-item">
            <span className="metric-label">{key.replace(/_/g, ' ').toUpperCase()}</span>
            <span className="metric-value">
              {typeof value === 'number' && value > 1000 ? formatNumber(value) : value}
              {key.includes('rate') && '%'}
            </span>
          </div>
        ))}
      </div>

      {alerts.length > 0 && (
        <div className="sector-alerts">
          <AlertCircle size={16} />
          <span>{alerts.length} alert{alerts.length > 1 ? 's' : ''}</span>
        </div>
      )}

      {trends.length > 0 && (
        <div className="sector-trends">
          <TrendingUp size={16} />
          <span>Trending {trends[trends.length - 1]?.period || 'up'}</span>
        </div>
      )}

      <Visualizations data={data} sector={sector.id} theme={theme} />
    </motion.div>
  );
};

export default SectorCard;


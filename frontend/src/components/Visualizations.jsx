import React from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './Visualizations.css';

const Visualizations = ({ data, sector, theme }) => {
  const trends = data?.trends || [];

  if (trends.length === 0) {
    return null;
  }

  // Prepare chart data
  const chartData = trends.map(trend => ({
    period: trend.period || trend.month || 'Period',
    value: trend.revenue || trend.attrition || trend.tickets || trend.cash_flow || 0,
    ...trend
  }));

  return (
    <div className={`visualizations ${theme}`}>
      <h4 className="chart-title">Trends</h4>
      <ResponsiveContainer width="100%" height={150}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke={theme === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'} />
          <XAxis 
            dataKey="period" 
            stroke={theme === 'dark' ? '#ffffff' : '#1a1a1a'}
            fontSize={12}
          />
          <YAxis 
            stroke={theme === 'dark' ? '#ffffff' : '#1a1a1a'}
            fontSize={12}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: theme === 'dark' ? 'rgba(26, 26, 46, 0.9)' : 'rgba(255, 255, 255, 0.9)',
              border: `1px solid ${theme === 'dark' ? 'rgba(102, 126, 234, 0.3)' : 'rgba(240, 147, 251, 0.3)'}`
            }}
          />
          <Line 
            type="monotone" 
            dataKey="value" 
            stroke={theme === 'dark' ? '#667eea' : '#f093fb'} 
            strokeWidth={2}
            dot={{ fill: theme === 'dark' ? '#667eea' : '#f093fb', r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default Visualizations;


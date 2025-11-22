import React, { useState } from 'react';
import {
  LineChart, Line, BarChart, Bar, AreaChart, Area, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { TrendingUp, BarChart2, PieChart as PieIcon, Activity } from 'lucide-react';
import './Visualizations.css';

const Visualizations = ({ data, sector, theme }) => {
  const [chartType, setChartType] = useState('line');
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

  // Colors based on theme
  const strokeColor = theme === 'dark' ? '#667eea' : '#f093fb';
  const fillColor = theme === 'dark' ? 'rgba(102, 126, 234, 0.3)' : 'rgba(240, 147, 251, 0.3)';
  const barColor = theme === 'dark' ? '#764ba2' : '#a18cd1';

  // Pie chart colors
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

  const renderChart = () => {
    switch (chartType) {
      case 'bar':
        return (
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke={theme === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'} />
            <XAxis dataKey="period" stroke={theme === 'dark' ? '#ffffff' : '#1a1a1a'} fontSize={10} tickLine={false} />
            <YAxis stroke={theme === 'dark' ? '#ffffff' : '#1a1a1a'} fontSize={10} tickLine={false} width={30} />
            <Tooltip
              contentStyle={{
                backgroundColor: theme === 'dark' ? 'rgba(26, 26, 46, 0.9)' : 'rgba(255, 255, 255, 0.9)',
                border: `1px solid ${theme === 'dark' ? 'rgba(102, 126, 234, 0.3)' : 'rgba(240, 147, 251, 0.3)'}`,
                borderRadius: '8px'
              }}
            />
            <Bar dataKey="value" fill={barColor} radius={[4, 4, 0, 0]} />
          </BarChart>
        );
      case 'area':
        return (
          <AreaChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke={theme === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'} />
            <XAxis dataKey="period" stroke={theme === 'dark' ? '#ffffff' : '#1a1a1a'} fontSize={10} tickLine={false} />
            <YAxis stroke={theme === 'dark' ? '#ffffff' : '#1a1a1a'} fontSize={10} tickLine={false} width={30} />
            <Tooltip
              contentStyle={{
                backgroundColor: theme === 'dark' ? 'rgba(26, 26, 46, 0.9)' : 'rgba(255, 255, 255, 0.9)',
                border: `1px solid ${theme === 'dark' ? 'rgba(102, 126, 234, 0.3)' : 'rgba(240, 147, 251, 0.3)'}`,
                borderRadius: '8px'
              }}
            />
            <Area type="monotone" dataKey="value" stroke={strokeColor} fill={fillColor} />
          </AreaChart>
        );
      case 'pie':
        // For pie chart, we might want to aggregate or show distribution
        // This is a simplified example using the same data
        return (
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              innerRadius={40}
              outerRadius={60}
              fill="#8884d8"
              paddingAngle={5}
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: theme === 'dark' ? 'rgba(26, 26, 46, 0.9)' : 'rgba(255, 255, 255, 0.9)',
                border: `1px solid ${theme === 'dark' ? 'rgba(102, 126, 234, 0.3)' : 'rgba(240, 147, 251, 0.3)'}`,
                borderRadius: '8px'
              }}
            />
          </PieChart>
        );
      case 'line':
      default:
        return (
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke={theme === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'} />
            <XAxis dataKey="period" stroke={theme === 'dark' ? '#ffffff' : '#1a1a1a'} fontSize={10} tickLine={false} />
            <YAxis stroke={theme === 'dark' ? '#ffffff' : '#1a1a1a'} fontSize={10} tickLine={false} width={30} />
            <Tooltip
              contentStyle={{
                backgroundColor: theme === 'dark' ? 'rgba(26, 26, 46, 0.9)' : 'rgba(255, 255, 255, 0.9)',
                border: `1px solid ${theme === 'dark' ? 'rgba(102, 126, 234, 0.3)' : 'rgba(240, 147, 251, 0.3)'}`,
                borderRadius: '8px'
              }}
            />
            <Line
              type="monotone"
              dataKey="value"
              stroke={strokeColor}
              strokeWidth={2}
              dot={{ fill: strokeColor, r: 3 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        );
    }
  };

  return (
    <div className={`visualizations ${theme}`}>
      <div className="viz-header">
        <h4 className="chart-title">Trends</h4>
        <div className="chart-selector">
          <button
            className={`chart-btn ${chartType === 'line' ? 'active' : ''}`}
            onClick={() => setChartType('line')}
            title="Line Chart"
          >
            <TrendingUp size={14} />
          </button>
          <button
            className={`chart-btn ${chartType === 'area' ? 'active' : ''}`}
            onClick={() => setChartType('area')}
            title="Area Chart"
          >
            <Activity size={14} />
          </button>
          <button
            className={`chart-btn ${chartType === 'bar' ? 'active' : ''}`}
            onClick={() => setChartType('bar')}
            title="Bar Chart"
          >
            <BarChart2 size={14} />
          </button>
          <button
            className={`chart-btn ${chartType === 'pie' ? 'active' : ''}`}
            onClick={() => setChartType('pie')}
            title="Pie Chart"
          >
            <PieIcon size={14} />
          </button>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={160}>
        {renderChart()}
      </ResponsiveContainer>
    </div>
  );
};

export default Visualizations;


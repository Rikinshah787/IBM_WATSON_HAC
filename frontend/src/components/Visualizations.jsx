import React from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
import './Visualizations.css';

const Visualizations = ({ data, sector, theme }) => {
  const trends = data?.trends || [];
  const metrics = data?.metrics || {};

  if (trends.length === 0 && Object.keys(metrics).length === 0) {
    return null;
  }

  // Prepare chart data
  const chartData = trends.map(trend => ({
    period: trend.period || trend.month || trend.quarter || 'Period',
    value: trend.revenue || trend.attrition || trend.tickets || trend.cash_flow || 0,
    ...trend
  }));

  // Color scheme based on theme (Apple colors)
  const primaryColor = theme === 'dark' ? '#007aff' : '#007aff';
  const secondaryColor = theme === 'dark' ? '#af52de' : '#af52de';
  const textColor = theme === 'dark' ? 'rgba(255, 255, 255, 0.7)' : 'rgba(0, 0, 0, 0.7)';
  const gridColor = theme === 'dark' ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.06)';

  // Determine which chart type to show based on sector
  const showBarChart = sector === 'hr' || sector === 'sales';
  const showAreaChart = sector === 'finance';

  return (
    <div className={`visualizations ${theme}`}>
      {chartData.length > 0 && (
        <>
          <h4 className="chart-title">Performance Trends</h4>

          {/* Bar Chart for HR and Sales */}
          {showBarChart && (
            <ResponsiveContainer width="100%" height={180}>
              <BarChart data={chartData}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke={gridColor}
                  vertical={false}
                />
                <XAxis
                  dataKey="period"
                  stroke={textColor}
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  stroke={textColor}
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: theme === 'dark' ? 'rgba(0, 0, 0, 0.8)' : 'rgba(255, 255, 255, 0.95)',
                    border: 'none',
                    borderRadius: '8px',
                    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                    fontSize: '13px',
                    color: theme === 'dark' ? '#ffffff' : '#1d1d1f'
                  }}
                  cursor={{ fill: 'rgba(0, 122, 255, 0.1)' }}
                />
                <Bar
                  dataKey="value"
                  fill={primaryColor}
                  radius={[8, 8, 0, 0]}
                  maxBarSize={40}
                />
              </BarChart>
            </ResponsiveContainer>
          )}

          {/* Area Chart for Finance */}
          {showAreaChart && (
            <ResponsiveContainer width="100%" height={180}>
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={primaryColor} stopOpacity={0.3} />
                    <stop offset="95%" stopColor={primaryColor} stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke={gridColor}
                  vertical={false}
                />
                <XAxis
                  dataKey="period"
                  stroke={textColor}
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  stroke={textColor}
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: theme === 'dark' ? 'rgba(0, 0, 0, 0.8)' : 'rgba(255, 255, 255, 0.95)',
                    border: 'none',
                    borderRadius: '8px',
                    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                    fontSize: '13px',
                    color: theme === 'dark' ? '#ffffff' : '#1d1d1f'
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="value"
                  stroke={primaryColor}
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorValue)"
                />
              </AreaChart>
            </ResponsiveContainer>
          )}

          {/* Line Chart for Service (default) */}
          {!showBarChart && !showAreaChart && (
            <ResponsiveContainer width="100%" height={180}>
              <LineChart data={chartData}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke={gridColor}
                  vertical={false}
                />
                <XAxis
                  dataKey="period"
                  stroke={textColor}
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  stroke={textColor}
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: theme === 'dark' ? 'rgba(0, 0, 0, 0.8)' : 'rgba(255, 255, 255, 0.95)',
                    border: 'none',
                    borderRadius: '8px',
                    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                    fontSize: '13px',
                    color: theme === 'dark' ? '#ffffff' : '#1d1d1f'
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke={primaryColor}
                  strokeWidth={2.5}
                  dot={{ fill: primaryColor, r: 4, strokeWidth: 0 }}
                  activeDot={{ r: 6, fill: primaryColor }}
                />
              </LineChart>
            </ResponsiveContainer>
          )}
        </>
      )}
    </div>
  );
};

export default Visualizations;

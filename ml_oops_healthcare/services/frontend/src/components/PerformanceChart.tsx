import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { useTheme } from '@mui/material';
import { PerformanceMetric } from '../types';

interface PerformanceChartProps {
  data: PerformanceMetric[];
  metrics: string[];
}

export const PerformanceChart: React.FC<PerformanceChartProps> = ({
  data,
  metrics,
}) => {
  const theme = useTheme();

  const formatData = (data: PerformanceMetric[]) => {
    return data.reduce((acc: any[], curr) => {
      const existingEntry = acc.find(
        (entry) => entry.timestamp === curr.timestamp
      );

      if (existingEntry) {
        existingEntry[curr.metricName] = curr.metricValue;
      } else {
        acc.push({
          timestamp: curr.timestamp,
          [curr.metricName]: curr.metricValue,
        });
      }

      return acc;
    }, []);
  };

  const formattedData = formatData(data);

  const colors = [
    theme.palette.primary.main,
    theme.palette.secondary.main,
    theme.palette.error.main,
    theme.palette.warning.main,
  ];

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart
        data={formattedData}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="timestamp"
          tickFormatter={(value) => new Date(value).toLocaleDateString()}
        />
        <YAxis
          domain={[0, 1]}
          tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
        />
        <Tooltip
          formatter={(value: number) => `${(value * 100).toFixed(1)}%`}
          labelFormatter={(label) => new Date(label).toLocaleString()}
        />
        <Legend />
        {metrics.map((metric, index) => (
          <Line
            key={metric}
            type="monotone"
            dataKey={metric}
            stroke={colors[index % colors.length]}
            dot={false}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
};
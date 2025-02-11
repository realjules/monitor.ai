import React from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
} from '@mui/material';
import {
  Assessment,
  Warning,
  CheckCircle,
  Timeline,
} from '@mui/icons-material';
import { MetricsCard } from '../components/MetricsCard';
import { PredictionTable } from '../components/PredictionTable';
import { PerformanceChart } from '../components/PerformanceChart';
import { useAuth } from '../contexts/AuthContext';

// Mock data - replace with actual API calls
const mockPredictions = [
  {
    id: '1',
    modelId: 'model1',
    patientId: 'PAT001',
    prediction: 0.85,
    uncertainty: 0.15,
    timestamp: new Date().toISOString(),
    metadata: {},
    groundTruth: 1,
  },
  // Add more mock predictions...
];

const mockPerformanceData = [
  {
    id: '1',
    modelId: 'model1',
    metricName: 'accuracy',
    metricValue: 0.88,
    timestamp: new Date().toISOString(),
    windowSize: '24h',
    details: {},
  },
  // Add more mock performance data...
];

export const Dashboard: React.FC = () => {
  const { user } = useAuth();

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <MetricsCard
            title="Model Accuracy"
            value={88}
            icon={<Assessment />}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <MetricsCard
            title="High Risk Cases"
            value={12}
            icon={<Warning />}
            unit=" cases"
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <MetricsCard
            title="Success Rate"
            value={95}
            icon={<CheckCircle />}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <MetricsCard
            title="Processing Time"
            value={1.2}
            icon={<Timeline />}
            unit="s"
          />
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Performance Trends
            </Typography>
            <PerformanceChart
              data={mockPerformanceData}
              metrics={['accuracy', 'precision', 'recall']}
            />
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent Predictions
            </Typography>
            <PredictionTable predictions={mockPredictions} />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};
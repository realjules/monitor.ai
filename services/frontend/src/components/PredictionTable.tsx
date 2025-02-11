import React from 'react';
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Chip,
} from '@mui/material';
import { Prediction } from '../types';

interface PredictionTableProps {
  predictions: Prediction[];
}

export const PredictionTable: React.FC<PredictionTableProps> = ({ predictions }) => {
  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Timestamp</TableCell>
            <TableCell>Patient ID</TableCell>
            <TableCell>Prediction</TableCell>
            <TableCell>Uncertainty</TableCell>
            <TableCell>Ground Truth</TableCell>
            <TableCell>Status</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {predictions.map((prediction) => (
            <TableRow key={prediction.id}>
              <TableCell>
                {new Date(prediction.timestamp).toLocaleString()}
              </TableCell>
              <TableCell>{prediction.patientId}</TableCell>
              <TableCell>
                <Typography variant="body2">
                  {(prediction.prediction * 100).toFixed(1)}%
                </Typography>
              </TableCell>
              <TableCell>
                <Typography variant="body2">
                  ±{(prediction.uncertainty * 100).toFixed(1)}%
                </Typography>
              </TableCell>
              <TableCell>
                {prediction.groundTruth !== undefined ? (
                  prediction.groundTruth
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    N/A
                  </Typography>
                )}
              </TableCell>
              <TableCell>
                <Chip
                  label={prediction.uncertainty > 0.2 ? 'High Risk' : 'Normal'}
                  color={prediction.uncertainty > 0.2 ? 'error' : 'success'}
                  size="small"
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
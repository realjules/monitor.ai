import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  LinearProgress,
  useTheme,
} from '@mui/material';

interface MetricsCardProps {
  title: string;
  value: number;
  unit?: string;
  target?: number;
  icon?: React.ReactNode;
}

export const MetricsCard: React.FC<MetricsCardProps> = ({
  title,
  value,
  unit = '%',
  target = 100,
  icon,
}) => {
  const theme = useTheme();
  const progress = (value / target) * 100;

  return (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          {icon && <Box mr={1}>{icon}</Box>}
          <Typography variant="h6" component="div">
            {title}
          </Typography>
        </Box>
        <Typography variant="h4" component="div" gutterBottom>
          {value.toFixed(1)}
          {unit}
        </Typography>
        <Box display="flex" alignItems="center">
          <Box width="100%" mr={1}>
            <LinearProgress
              variant="determinate"
              value={progress}
              sx={{
                height: 8,
                borderRadius: 4,
                backgroundColor: theme.palette.grey[200],
                '& .MuiLinearProgress-bar': {
                  borderRadius: 4,
                },
              }}
            />
          </Box>
          <Box minWidth={35}>
            <Typography variant="body2" color="text.secondary">
              {progress.toFixed(0)}%
            </Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};
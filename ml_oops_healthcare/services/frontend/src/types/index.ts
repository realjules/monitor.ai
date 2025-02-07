export interface User {
  id: string;
  username: string;
  role: 'radiologist' | 'compliance' | 'admin';
  email: string;
}

export interface Prediction {
  id: string;
  modelId: string;
  patientId: string;
  prediction: number;
  uncertainty: number;
  timestamp: string;
  metadata: Record<string, any>;
  groundTruth?: number;
}

export interface AuditLog {
  id: string;
  timestamp: string;
  userId: string;
  action: string;
  resourceType: string;
  resourceId: string;
  details: Record<string, any>;
}

export interface PerformanceMetric {
  id: string;
  modelId: string;
  metricName: string;
  metricValue: number;
  timestamp: string;
  windowSize: string;
  details: Record<string, any>;
}

export interface ModelInfo {
  id: string;
  name: string;
  version: string;
  status: 'active' | 'inactive';
  lastUpdated: string;
  metrics: {
    accuracy: number;
    precision: number;
    recall: number;
  };
}
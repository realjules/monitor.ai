from datetime import datetime, timedelta
from typing import Dict, Any, List
import numpy as np

class MetricsGenerator:
    def __init__(self):
        self.metrics = {}

    def calculate_model_metrics(
        self,
        model_id: str,
        predictions: List[Dict[str, Any]],
        window_size: str = "24h"
    ) -> Dict[str, Any]:
        """Calculate model performance metrics."""
        try:
            # Extract predictions and ground truth
            pred_values = [p["prediction"] for p in predictions if p.get("ground_truth") is not None]
            true_values = [p["ground_truth"] for p in predictions if p.get("ground_truth") is not None]
            
            if not pred_values:
                return {
                    "model_id": model_id,
                    "window_size": window_size,
                    "error": "No predictions with ground truth available"
                }

            # Calculate metrics
            metrics = {
                "model_id": model_id,
                "window_size": window_size,
                "prediction_count": len(predictions),
                "ground_truth_count": len(pred_values),
                "mean_uncertainty": np.mean([p["uncertainty"] for p in predictions]),
                "metrics": {
                    "mse": np.mean(np.square(np.array(pred_values) - np.array(true_values))),
                    "mae": np.mean(np.abs(np.array(pred_values) - np.array(true_values))),
                    "timestamp": datetime.now().isoformat()
                }
            }

            # Store metrics
            self.metrics[model_id] = metrics
            return metrics

        except Exception as e:
            return {
                "model_id": model_id,
                "window_size": window_size,
                "error": str(e)
            }

    def get_model_metrics(
        self,
        model_id: str,
        start_time: datetime = None,
        end_time: datetime = None
    ) -> Dict[str, Any]:
        """Get stored metrics for a model."""
        try:
            if model_id not in self.metrics:
                return {"error": "Model metrics not found"}

            metrics = self.metrics[model_id]
            
            # Filter by time range if provided
            if start_time and end_time:
                metric_time = datetime.fromisoformat(metrics["metrics"]["timestamp"])
                if not (start_time <= metric_time <= end_time):
                    return {"error": "No metrics available for the specified time range"}

            return metrics

        except Exception as e:
            return {"error": str(e)}

    def generate_performance_report(
        self,
        model_id: str,
        time_range: str = "7d"
    ) -> Dict[str, Any]:
        """Generate a comprehensive performance report."""
        try:
            if model_id not in self.metrics:
                return {"error": "Model metrics not found"}

            metrics = self.metrics[model_id]
            
            # Calculate additional statistics
            report = {
                "model_id": model_id,
                "time_range": time_range,
                "summary": {
                    "total_predictions": metrics["prediction_count"],
                    "ground_truth_coverage": metrics["ground_truth_count"] / metrics["prediction_count"],
                    "average_uncertainty": metrics["mean_uncertainty"]
                },
                "performance_metrics": metrics["metrics"],
                "generated_at": datetime.now().isoformat()
            }

            return report

        except Exception as e:
            return {"error": str(e)}
import { api } from '@/lib/api/axios';
import { Prediction, PredictionHistory } from '@/lib/types/prediction';
import { convertStringToDate } from '@/utils';

export async function getPredictions() {
  const { data } = await api.get('/production/predict/next/48');
  const predictions = data.prediction as Prediction[];
  return predictions.map((p) => ({
    date: convertStringToDate(p.date),
    prediction: p.power,
  }));
}

export async function getPredictionsHistory() {
  const { data } = await api.get('/production/prediction/history');
  const predictions = data.history as PredictionHistory[];
  return predictions.map((p) => ({
    date: convertStringToDate(p.date),
    power: p.real,
    prediction: p.prediction,
  }));
}

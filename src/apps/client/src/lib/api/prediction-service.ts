import { api } from '@/lib/api/axios';
import { Prediction } from '@/lib/types/prediction';
import { convertStringToDate } from '@/utils';

export async function getPredictions() {
  const { data } = await api.get('/production/predict/next/48');
  const predictions = data.prediction as Prediction[];
  return predictions.map((p) => ({
    date: convertStringToDate(p.date),
    power: p.power,
  }));
}

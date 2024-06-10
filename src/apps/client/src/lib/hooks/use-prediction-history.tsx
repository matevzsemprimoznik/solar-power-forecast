import { useQuery } from '@tanstack/react-query';
import { getPredictionsHistory } from '@/lib/api/prediction-service';

export const usePredictionHistory = () =>
  useQuery({
    queryKey: ['prediction-history'],
    queryFn: getPredictionsHistory,
  });

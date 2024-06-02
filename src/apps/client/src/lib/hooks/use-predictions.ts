import { useQuery } from '@tanstack/react-query';
import { predictionKeys } from '@/lib/hooks/key-factories';
import { getPredictions } from '@/lib/api/prediction-service';

export const usePredictions = () =>
  useQuery({
    queryKey: predictionKeys.n_next(),
    queryFn: getPredictions,
  });

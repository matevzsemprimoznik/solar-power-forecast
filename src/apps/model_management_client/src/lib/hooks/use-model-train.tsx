import { useMutation, UseMutationOptions } from '@tanstack/react-query';
import { trainModel } from '@/lib/api/models-service';
import { modelsKeys } from '@/lib/hooks/key-factories';

export const useModelTrain = (
  options?: Omit<UseMutationOptions<any, Error, string, unknown>, 'mutationFn' | 'mutationKey'>
) => useMutation<any, Error, string, unknown>({
  mutationKey: modelsKeys.train,
  mutationFn: trainModel,
  ...options
});
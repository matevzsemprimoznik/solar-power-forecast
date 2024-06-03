import { MutationOptions, useMutation } from '@tanstack/react-query';
import { modelsKeys } from '@/lib/hooks/key-factories';
import { moveModelToProduction } from '@/lib/api/models-service';
import { MoveModelToProductionData } from '@/lib/types/models';

export const useMoveModelToProduction = (options: Omit<MutationOptions<any, Error, MoveModelToProductionData, unknown>, 'mutationFn' | 'mutationKey'>) => useMutation({
  mutationKey: modelsKeys.moveToProduction(),
  mutationFn: (data: MoveModelToProductionData ) => moveModelToProduction(data),
  ...options
})
import { useQuery, UseQueryOptions } from '@tanstack/react-query';
import { modelsKeys } from '@/lib/hooks/key-factories';
import { getModel } from '@/lib/api/models-service';

export const useModel = (id: string, options?: Omit<UseQueryOptions, 'queryKey' | 'queryFn'>) => useQuery({
  queryKey: modelsKeys.getById(id),
  queryFn: () => getModel(id)
})
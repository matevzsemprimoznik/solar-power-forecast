import { useQuery } from '@tanstack/react-query';
import { modelsKeys } from '@/lib/hooks/key-factories';
import { getModels } from '@/lib/api/models-service';

export const useModels = () => useQuery({
  queryKey: modelsKeys.all,
  queryFn: getModels
})
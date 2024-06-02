import { useQuery } from '@tanstack/react-query';
import { historyKeys } from '@/lib/hooks/key-factories';
import { getHistory } from '@/lib/api/history-service';

export const useHistory = (startDate?: string, endDate?: string) =>
  useQuery({
    queryKey: historyKeys.range(startDate, endDate),
    queryFn: () => getHistory(startDate, endDate),
  });

import { api } from '@/lib/api/axios';
import { convertStringToDate } from '@/utils';
import { History } from '@/lib/types/history';

export const getHistory = async (startDate?: string, endDate?: string) => {
  const { data } = await api.get('/production/history', {
    params: {
      start_date: startDate,
      end_date: endDate,
    },
  });
  const history = data.history as History[];
  return history.map((h) => ({
    date: convertStringToDate(h.time),
    power: h.power,
  }));
};

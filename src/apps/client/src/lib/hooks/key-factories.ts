export const predictionKeys = {
  all: ['predictions'] as const,
  next: () => [predictionKeys.all, 'next'] as const,
  n_next: (n: number | undefined = 24) =>
    [predictionKeys.all, 'next', n] as const,
};

export const historyKeys = {
  all: ['history'],
  range: (startDate?: string, endDate?: string) => [
    historyKeys.all,
    startDate,
    endDate,
  ],
};

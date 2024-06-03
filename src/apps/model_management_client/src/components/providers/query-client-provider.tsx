'use client';
import { ReactNode } from 'react';
import { QueryClient } from '@tanstack/query-core';
import { QueryClientProvider as QueryClientProviderImpl } from '@tanstack/react-query';

interface QueryClientProviderProps {
  children: ReactNode;
}

const queryClient = new QueryClient();
export default function QueryClientProvider({
  children,
}: QueryClientProviderProps) {
  return (
    <QueryClientProviderImpl client={queryClient}>
      {children}
    </QueryClientProviderImpl>
  );
}

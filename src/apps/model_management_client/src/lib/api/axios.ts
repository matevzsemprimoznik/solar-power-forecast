import axios from 'axios';
import { env } from '@/env.mjs';

export const modelsManagementApi = axios.create({
  baseURL: env.NEXT_PUBLIC_MODELS_MANAGEMENT_API_URI,
  headers: {
    'Content-Type': 'application/json',
  },
});

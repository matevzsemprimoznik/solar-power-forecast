import { createEnv } from '@t3-oss/env-nextjs';
import { z } from 'zod';

export const env = createEnv({
  client: {
    NEXT_PUBLIC_MODELS_MANAGEMENT_API_URI: z.string().url(),
    NEXT_PUBLIC_PUSHER_KEY: z.string(),
  },
  runtimeEnv: {
    NEXT_PUBLIC_MODELS_MANAGEMENT_API_URI: process.env.NEXT_PUBLIC_MODELS_MANAGEMENT_API_URI,
    NEXT_PUBLIC_PUSHER_KEY: process.env.NEXT_PUBLIC_PUSHER_KEY,
  },
});
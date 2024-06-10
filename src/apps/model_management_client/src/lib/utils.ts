import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"
import Pusher from 'pusher-js';
import { env } from '@/env.mjs';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function pretifyString(str: string) {
  const noUnderscore = str.replace(/_/g, ' ')
  return noUnderscore.charAt(0).toUpperCase() + noUnderscore.slice(1)
}

export function formatDate(timestamp: number) {
  const date = new Date(timestamp)
  return `${date.getDate()}-${date.getMonth() + 1}-${date.getFullYear()} ${date.getHours()}:${date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()}`
}

export const pusherClient = new Pusher(env.NEXT_PUBLIC_PUSHER_KEY, {
  cluster: 'eu'
});

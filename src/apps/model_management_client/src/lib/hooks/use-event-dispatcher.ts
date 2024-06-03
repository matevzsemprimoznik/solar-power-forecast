import { create, SetState } from 'zustand';

interface EventDispatcher {
  listeners: Record<string, ((data: any) => void)[]>;

  addListener: (eventName: string, listener: (data: any) => void) => void;
  removeListener: (eventName: string, listener: (data: any) => void) => void;
  dispatchEvent: (eventName: string, data: any) => void;
}

export const useEventDispatcher = create<EventDispatcher>((set, getState) => ({
  listeners: {},

  addListener: (eventName, listener) => {
    set(state => ({
      listeners: {
        ...state.listeners,
        [eventName]: [...(state.listeners[eventName] || []), listener]
      }
    }));
  },

  removeListener: (eventName, listener) => {
    set(state => ({
      listeners: {
        ...state.listeners,
        [eventName]: (state.listeners[eventName] || []).filter(l => l !== listener)
      }
    }));
  },

  dispatchEvent: (eventName, data) => {
    const { listeners } = getState();
    if (listeners[eventName]) {
      listeners[eventName].forEach(listener => {
        listener(data);
      });
    }
  }
}));
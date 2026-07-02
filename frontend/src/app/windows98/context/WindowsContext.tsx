import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';

export interface WindowData {
  id: string;
  title: string;
  icon?: string | ReactNode;
  component: ReactNode;
  isMinimized: boolean;
  isMaximized: boolean;
  zIndex: number;
}

interface WindowsContextType {
  windows: WindowData[];
  openWindow: (windowData: Omit<WindowData, 'isMinimized' | 'isMaximized' | 'zIndex'>) => void;
  closeWindow: (id: string) => void;
  minimizeWindow: (id: string) => void;
  maximizeWindow: (id: string) => void;
  restoreWindow: (id: string) => void;
  focusWindow: (id: string) => void;
}

const WindowsContext = createContext<WindowsContextType | undefined>(undefined);

let highestZIndex = 100;

export function WindowsProvider({ children }: { children: ReactNode }) {
  const [windows, setWindows] = useState<WindowData[]>([]);

  const focusWindow = useCallback((id: string) => {
    highestZIndex += 1;
    setWindows(prev => prev.map(w => 
      w.id === id ? { ...w, zIndex: highestZIndex } : w
    ));
  }, []);

  const openWindow = useCallback((windowData: Omit<WindowData, 'isMinimized' | 'isMaximized' | 'zIndex'>) => {
    setWindows(prev => {
      // Si la ventana ya está abierta, solo le damos el foco y la desminimizamos si es el caso
      const existing = prev.find(w => w.id === windowData.id);
      if (existing) {
        setTimeout(() => focusWindow(windowData.id), 0);
        return prev.map(w => w.id === windowData.id ? { ...w, isMinimized: false } : w);
      }
      
      highestZIndex += 1;
      return [...prev, { 
        ...windowData, 
        isMinimized: false, 
        isMaximized: false, 
        zIndex: highestZIndex 
      }];
    });
  }, [focusWindow]);

  const closeWindow = useCallback((id: string) => {
    setWindows(prev => prev.filter(w => w.id !== id));
  }, []);

  const minimizeWindow = useCallback((id: string) => {
    setWindows(prev => prev.map(w => 
      w.id === id ? { ...w, isMinimized: true } : w
    ));
  }, []);

  const maximizeWindow = useCallback((id: string) => {
    setWindows(prev => prev.map(w => 
      w.id === id ? { ...w, isMaximized: true } : w
    ));
  }, []);

  const restoreWindow = useCallback((id: string) => {
    setWindows(prev => prev.map(w => 
      w.id === id ? { ...w, isMaximized: false, isMinimized: false } : w
    ));
    focusWindow(id);
  }, [focusWindow]);

  return (
    <WindowsContext.Provider value={{
      windows,
      openWindow,
      closeWindow,
      minimizeWindow,
      maximizeWindow,
      restoreWindow,
      focusWindow
    }}>
      {children}
    </WindowsContext.Provider>
  );
}

export function useWindows() {
  const context = useContext(WindowsContext);
  if (!context) {
    throw new Error('useWindows must be used within a WindowsProvider');
  }
  return context;
}

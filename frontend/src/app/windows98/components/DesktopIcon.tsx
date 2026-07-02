import React, { useState, useEffect } from 'react';

interface DesktopIconProps {
  label: string;
  icon: string;
  onDoubleClick: () => void;
}

export function DesktopIcon({ label, icon, onDoubleClick }: DesktopIconProps) {
  const [isSelected, setIsSelected] = useState(false);

  // Deseleccionar si hace clic fuera del icono
  useEffect(() => {
    const handleGlobalClick = () => setIsSelected(false);
    window.addEventListener('click', handleGlobalClick);
    return () => window.removeEventListener('click', handleGlobalClick);
  }, []);

  return (
    <div 
      onDoubleClick={(e) => {
        e.stopPropagation();
        onDoubleClick();
      }}
      onClick={(e) => {
        e.stopPropagation();
        setIsSelected(true);
      }}
      className="w-full h-full flex flex-col items-center cursor-pointer p-[2px] hover:bg-white/10 rounded-sm transition-colors"
      style={{ userSelect: 'none' }}
    >
      <img 
        src={icon} 
        alt={label} 
        className={`w-12 h-12 mb-1 pointer-events-none ${isSelected ? 'contrast-50 brightness-125' : ''}`}
        draggable={false}
      />
      <div className={`px-1 py-[2px] text-center text-sm text-white leading-tight [text-shadow:1px_1px_0_#000] border ${isSelected ? 'bg-[#000080] border-white border-dotted' : 'bg-transparent border-transparent'}`}>
        {label}
      </div>
    </div>
  );
}

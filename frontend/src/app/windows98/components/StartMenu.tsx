import React, { useState } from 'react';
import { useWindows } from '../context/WindowsContext';

interface StartMenuItemProps {
  label: string;
  icon?: string;
  onClick?: () => void;
  subItems?: StartMenuItemProps[];
}

export function StartMenuItem({ label, icon, onClick, subItems }: StartMenuItemProps) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={(e) => {
        if (onClick) {
          e.stopPropagation();
          onClick();
        }
      }}
      className={`relative flex items-center px-2 py-1 cursor-pointer text-xs ${isHovered ? 'bg-[#000080] text-white' : 'bg-transparent text-black'}`}
    >
      <div className="w-6 flex justify-center">
        {icon && <img src={icon} alt="" className="w-4 h-4" />}
      </div>
      <div className="flex-1 pl-2">{label}</div>
      {subItems && subItems.length > 0 && (
        <div className="pl-2">▶</div>
      )}

      {/* Submenú en Cascada */}
      {isHovered && subItems && subItems.length > 0 && (
        <div className="absolute top-[-2px] left-full bg-[#c0c0c0] win98-border min-w-[150px] z-[10000]">
          {subItems.map((item, idx) => (
            <StartMenuItem key={idx} {...item} />
          ))}
        </div>
      )}
    </div>
  );
}

interface StartMenuProps {
  onClose: () => void;
  items: StartMenuItemProps[];
}

export function StartMenu({ onClose, items }: StartMenuProps) {
  return (
    <div className="absolute bottom-[35px] left-0 bg-[#c0c0c0] win98-border flex min-w-[200px] min-h-[300px] z-[10000] font-win98">
      {/* Barra lateral azul oscura estilo Win98 */}
      <div className="w-[30px] bg-gradient-to-b from-[#000080] to-[#1084d0] flex items-end pb-2 pl-1">
        <div className="text-white origin-bottom-left -rotate-90 font-bold text-base whitespace-nowrap tracking-wide">
          Tesis <span className="font-normal">98</span>
        </div>
      </div>
      
      {/* Lista de Items */}
      <div className="flex-1 p-[2px] flex flex-col">
        {items.map((item, idx) => (
          <React.Fragment key={idx}>
            <StartMenuItem 
              {...item} 
              onClick={() => {
                if (item.onClick) item.onClick();
                onClose(); // Cierra el menú al hacer clic en un item final
              }} 
            />
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}

import { useState } from "react";
import {
  LayoutDashboard,
  Clock,
  Settings,
  Shield,
  ChevronRight,
  Zap,
} from "lucide-react";

const navItems = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "history", label: "Scan History", icon: Clock },
  { id: "settings", label: "Settings", icon: Settings },
];

interface SidebarProps {
  activeItem?: string;
  onNavigate?: (id: string) => void;
}

export function Sidebar({ activeItem = "dashboard", onNavigate }: SidebarProps) {
  const [hovered, setHovered] = useState<string | null>(null);

  return (
    <aside
      style={{
        width: "240px",
        minWidth: "240px",
        background: "rgba(4, 9, 18, 0.98)",
        borderRight: "1px solid rgba(255,255,255,0.06)",
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        position: "fixed",
        left: 0,
        top: 0,
        zIndex: 50,
        fontFamily: "'Inter', sans-serif",
      }}
    >
      {/* Logo */}
      <div
        style={{
          padding: "24px 20px 20px",
          borderBottom: "1px solid rgba(255,255,255,0.06)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <div
            style={{
              width: "38px",
              height: "38px",
              background: "linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)",
              borderRadius: "10px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: "0 0 20px rgba(6, 182, 212, 0.35)",
            }}
          >
            <Shield size={20} color="white" />
          </div>
          <div>
            <div
              style={{
                color: "#e2e8f0",
                fontWeight: 700,
                fontSize: "15px",
                letterSpacing: "-0.3px",
              }}
            >
              SecurAudit
            </div>
            <div style={{ fontSize: "10px", color: "#475569", fontWeight: 500, letterSpacing: "0.5px" }}>
              ENTERPRISE
            </div>
          </div>
        </div>
      </div>

      {/* Navigation label */}
      <div style={{ padding: "20px 20px 8px" }}>
        <span
          style={{
            fontSize: "10px",
            fontWeight: 600,
            color: "#334155",
            letterSpacing: "1px",
          }}
        >
          MAIN MENU
        </span>
      </div>

      {/* Nav items */}
      <nav style={{ flex: 1, padding: "0 12px" }}>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeItem === item.id;
          const isHovered = hovered === item.id;

          return (
            <button
              key={item.id}
              onClick={() => onNavigate?.(item.id)}
              onMouseEnter={() => setHovered(item.id)}
              onMouseLeave={() => setHovered(null)}
              style={{
                width: "100%",
                display: "flex",
                alignItems: "center",
                gap: "10px",
                padding: "10px 12px",
                borderRadius: "8px",
                border: isActive ? "1px solid rgba(6, 182, 212, 0.2)" : "1px solid transparent",
                cursor: "pointer",
                marginBottom: "3px",
                background: isActive
                  ? "rgba(6, 182, 212, 0.1)"
                  : isHovered
                    ? "rgba(255,255,255,0.04)"
                    : "transparent",
                color: isActive ? "#06b6d4" : isHovered ? "#94a3b8" : "#64748b",
                transition: "all 0.15s ease",
                textAlign: "left",
                position: "relative",
              }}
            >
              {isActive && (
                <div
                  style={{
                    position: "absolute",
                    left: 0,
                    top: "50%",
                    transform: "translateY(-50%)",
                    width: "3px",
                    height: "60%",
                    background: "#06b6d4",
                    borderRadius: "0 3px 3px 0",
                    boxShadow: "0 0 8px rgba(6, 182, 212, 0.6)",
                  }}
                />
              )}
              <Icon size={17} />
              <span
                style={{
                  fontSize: "13.5px",
                  fontWeight: isActive ? 600 : 400,
                  flex: 1,
                }}
              >
                {item.label}
              </span>
              {isActive && <ChevronRight size={13} />}
            </button>
          );
        })}
      </nav>
    </aside>
  );
}

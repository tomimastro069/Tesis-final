import { useEffect, useState } from "react";
import { Sidebar } from "./components/Sidebar";
import { ScanReport } from "./components/ScanReport";
import { DomainsDashboard } from "./components/DomainsDashboard";
import { ScanForm } from "./components/ScanForm";
import { Domain } from "../services/api";
import { Download, Bell, Search } from "lucide-react";

export default function App() {
  const [activeNav, setActiveNav] = useState("dashboard");
  const [headerHover, setHeaderHover] = useState(false);
  const [selectedDomain, setSelectedDomain] = useState<Domain | null>(null);

  useEffect(() => {
    document.documentElement.classList.add("dark");
    document.documentElement.style.fontFamily = "'Inter', sans-serif";
    return () => {
      document.documentElement.classList.remove("dark");
    };
  }, []);

  return (
    <div
      className="size-full"
      style={{
        background: "#040912",
        fontFamily: "'Inter', sans-serif",
        minHeight: "100vh",
        position: "relative",
      }}
    >
      {/* Subtle background gradient blobs */}
      <div
        style={{
          position: "fixed",
          top: "-200px",
          right: "-100px",
          width: "500px",
          height: "500px",
          background: "radial-gradient(circle, rgba(6,182,212,0.04) 0%, transparent 70%)",
          pointerEvents: "none",
          zIndex: 0,
        }}
      />
      <div
        style={{
          position: "fixed",
          bottom: "-150px",
          left: "200px",
          width: "400px",
          height: "400px",
          background: "radial-gradient(circle, rgba(59,130,246,0.03) 0%, transparent 70%)",
          pointerEvents: "none",
          zIndex: 0,
        }}
      />

      {/* Sidebar */}
      <Sidebar
        activeItem={activeNav}
        onNavigate={(item) => {
          setActiveNav(item);
          if (item === "dashboard") {
            setSelectedDomain(null);
          }
        }}
      />

      {/* Main content */}
      <main
        style={{
          marginLeft: "240px",
          minHeight: "100vh",
          position: "relative",
          zIndex: 1,
        }}
      >
        {/* Header */}
        <header
          style={{
            position: "sticky",
            top: 0,
            zIndex: 40,
            background: "rgba(4, 9, 18, 0.9)",
            backdropFilter: "blur(20px)",
            WebkitBackdropFilter: "blur(20px)",
            borderBottom: "1px solid rgba(255,255,255,0.06)",
            padding: "14px 28px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: "16px",
          }}
        >
          {/* Left: welcome */}
          <div>
            <div style={{ fontSize: "18px", fontWeight: 600, color: "#e2e8f0", letterSpacing: "-0.3px" }}>
              {selectedDomain ? `Dominio: ${selectedDomain.target}` : "Panel de Seguridad"}
            </div>
            <div style={{ fontSize: "12px", color: "#475569", marginTop: "1px" }}>
              {selectedDomain ? `Viendo resultados del análisis para ${selectedDomain.target}` : "Resumen de tus dominios objetivo"}
            </div>
          </div>

          {/* Right: status + actions */}
          <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
            {/* Search */}
            <button
              style={{
                display: "flex",
                alignItems: "center",
                gap: "8px",
                padding: "8px 14px",
                background: "rgba(255,255,255,0.04)",
                border: "1px solid rgba(255,255,255,0.08)",
                borderRadius: "8px",
                color: "#64748b",
                cursor: "pointer",
                fontSize: "13px",
                transition: "all 0.15s ease",
              }}
            >
              <Search size={14} />
              Buscar...
            </button>

            {/* Scan mode status — read-only, set by backend */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "7px",
                padding: "7px 14px",
                background: "rgba(16, 185, 129, 0.07)",
                border: "1px solid rgba(16, 185, 129, 0.18)",
                borderRadius: "8px",
                userSelect: "none",
                cursor: "default",
              }}
            >
              <div
                style={{
                  width: "7px",
                  height: "7px",
                  borderRadius: "50%",
                  background: "#10b981",
                  boxShadow: "0 0 6px rgba(16,185,129,0.7)",
                  flexShrink: 0,
                }}
              />
              <span style={{ fontSize: "11px", color: "#64748b", fontWeight: 500 }}>
                Sistema:
              </span>
              <span style={{ fontSize: "12px", fontWeight: 600, color: "#10b981" }}>
                En línea
              </span>
            </div>

            {/* Download PDF */}
            {selectedDomain && (
              <button
                onMouseEnter={() => setHeaderHover(true)}
                onMouseLeave={() => setHeaderHover(false)}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  padding: "8px 18px",
                  background: headerHover
                    ? "linear-gradient(135deg, #0891b2, #2563eb)"
                    : "linear-gradient(135deg, #06b6d4, #3b82f6)",
                  border: "none",
                  borderRadius: "8px",
                  color: "white",
                  cursor: "pointer",
                  fontSize: "13px",
                  fontWeight: 600,
                  transition: "all 0.2s ease",
                  boxShadow: "0 4px 16px rgba(6, 182, 212, 0.25)",
                  transform: headerHover ? "translateY(-1px)" : "none",
                }}
              >
                <Download size={14} />
                Descargar PDF
              </button>
            )}
          </div>
        </header>

        {/* Dynamic Page Content */}
        {activeNav === "dashboard" ? (
          selectedDomain ? (
            <div>
              <div style={{ padding: "16px 28px", paddingBottom: 0 }}>
                <button
                  onClick={() => setSelectedDomain(null)}
                  style={{
                    background: "transparent",
                    border: "none",
                    color: "#a78bfa",
                    cursor: "pointer",
                    fontSize: "14px",
                  }}
                >
                  ← Volver a Dominios
                </button>
              </div>
              <ScanReport domain={selectedDomain} />
            </div>
          ) : (
            <DomainsDashboard onSelectDomain={setSelectedDomain} />
          )
        ) : activeNav === "new-scan" ? (
          <ScanForm onCancel={() => setActiveNav("dashboard")} onSuccess={(domain) => { setActiveNav("dashboard"); setSelectedDomain(domain); }} />
        ) : (
          <div style={{ padding: "40px", color: "white" }}>Próximamente...</div>
        )}
      </main>
    </div>
  );
}

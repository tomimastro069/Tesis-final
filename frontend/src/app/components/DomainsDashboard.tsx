import { useState, useEffect } from "react";
import { Plus, Shield, ArrowRight, Server, Trash2 } from "lucide-react";
import { ScanForm } from "./ScanForm";
import { useDomains } from "../../hooks/useDomains";
import type { Domain } from "../../services/api";

export function DomainsDashboard({ onSelectDomain }: { onSelectDomain: (domain: Domain) => void }) {
  const { domains, handleAddDomain, handleDeleteDomain } = useDomains();
  const [showForm, setShowForm] = useState(false);


  const glassCard = {
    background: "rgba(255, 255, 255, 0.025)",
    backdropFilter: "blur(20px)",
    WebkitBackdropFilter: "blur(20px)",
    border: "1px solid rgba(255, 255, 255, 0.07)",
    borderRadius: "16px",
    padding: "24px",
    position: "relative" as const,
    cursor: "pointer",
    transition: "all 0.2s ease"
  };

  return (
    <div style={{ padding: "24px 28px", maxWidth: "1400px", margin: "0 auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "32px" }}>
        <div>
          <h1 style={{ fontSize: "24px", color: "#e2e8f0", fontWeight: 700 }}>Mis Dominios</h1>
          <p style={{ color: "#64748b", marginTop: "4px" }}>Gestiona y analiza la seguridad de tus sitios web</p>
        </div>
        <button
          onClick={() => setShowForm(true)}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            padding: "8px 18px",
            background: "linear-gradient(135deg, #06b6d4, #3b82f6)",
            border: "none",
            borderRadius: "8px",
            color: "white",
            cursor: "pointer",
            fontWeight: 600,
            boxShadow: "0 4px 16px rgba(6, 182, 212, 0.25)",
          }}
        >
          <Plus size={16} />
          Nuevo Análisis
        </button>
      </div>

      {showForm && (
        <div style={{ marginBottom: "32px" }}>
          <ScanForm onScanStarted={(scanId: string) => setShowForm(false)} />
        </div>
      )}

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: "24px" }}>
        {domains.map((domain) => (
          <div 
            key={domain.id} 
            style={{ ...glassCard, cursor: domain.status === 'scanning' ? 'wait' : 'pointer', opacity: domain.status === 'scanning' ? 0.7 : 1 }}
            onClick={() => {
              if (domain.status !== 'scanning') {
                onSelectDomain(domain);
              }
            }}
            onMouseEnter={(e) => { 
              if (domain.status !== 'scanning') {
                e.currentTarget.style.transform = "translateY(-4px)"; 
                e.currentTarget.style.borderColor = "rgba(59,130,246,0.3)"; 
              }
            }}
            onMouseLeave={(e) => { 
              if (domain.status !== 'scanning') {
                e.currentTarget.style.transform = "none"; 
                e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.07)"; 
              }
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "16px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                <div style={{ width: "40px", height: "40px", borderRadius: "10px", background: "rgba(59, 130, 246, 0.1)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                  <Server size={20} color="#3b82f6" />
                </div>
                <div>
                  <h3 style={{ color: "#e2e8f0", fontSize: "16px", fontWeight: 600 }}>{domain.target.replace(/^https?:\/\//, '')}</h3>
                  <span style={{ fontSize: "12px", color: domain.status === 'scanning' ? '#d97706' : '#64748b' }}>
                    {domain.status === 'scanning' ? `Analizando... ${domain.progress ?? 0}%` : domain.status === 'completed' ? 'Análisis Completado' : 'Pendiente'}
                  </span>
                </div>
              </div>
              <button
                onClick={(e) => { e.stopPropagation(); handleDeleteDomain(domain); }}
                style={{
                  background: "transparent",
                  border: "none",
                  cursor: "pointer",
                  color: "#64748b",
                  padding: "4px",
                  borderRadius: "4px",
                  transition: "color 0.2s, background 0.2s"
                }}
                onMouseEnter={(e) => { e.currentTarget.style.color = "#ef4444"; e.currentTarget.style.background = "rgba(239, 68, 68, 0.1)"; }}
                onMouseLeave={(e) => { e.currentTarget.style.color = "#64748b"; e.currentTarget.style.background = "transparent"; }}
                title="Eliminar dominio"
              >
                <Trash2 size={18} />
              </button>
            </div>
            
            <div style={{ display: "flex", gap: "16px", marginBottom: "20px" }}>
              <div style={{ flex: 1, background: "rgba(0,0,0,0.2)", borderRadius: "8px", padding: "12px" }}>
                <div style={{ fontSize: "11px", color: "#64748b", marginBottom: "4px" }}>NIVEL DE RIESGO</div>
                <div style={{ fontSize: "18px", fontWeight: 700, color: domain.score && domain.score < 50 ? "#dc2626" : domain.score && domain.score < 80 ? "#ea580c" : "#10b981" }}>
                  {domain.riskLevel || "-"}
                </div>
              </div>
              <div style={{ flex: 1, background: "rgba(0,0,0,0.2)", borderRadius: "8px", padding: "12px" }}>
                <div style={{ fontSize: "11px", color: "#64748b", marginBottom: "4px" }}>ÚLTIMO ESCANEO</div>
                <div style={{ fontSize: "14px", fontWeight: 600, color: "#cbd5e1" }}>
                  {domain.lastScan ? new Date(domain.lastScan).toLocaleDateString() : "-"}
                </div>
              </div>
            </div>

            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", borderTop: "1px solid rgba(255,255,255,0.05)", paddingTop: "16px" }}>
              <span style={{ fontSize: "13px", color: domain.status === 'scanning' ? "#94a3b8" : "#3b82f6", fontWeight: 500 }}>
                {domain.status === 'scanning' ? (domain.progressMessage || "Análisis en progreso...") : "Ver detalles"}
              </span>
              {domain.status !== 'scanning' && <ArrowRight size={16} color="#3b82f6" />}
            </div>
          </div>
        ))}
        {domains.length === 0 && !showForm && (
          <div style={{ gridColumn: "1 / -1", textAlign: "center", padding: "64px 20px", background: "rgba(255,255,255,0.02)", borderRadius: "16px", border: "1px dashed rgba(255,255,255,0.1)" }}>
            <Shield size={48} color="#475569" style={{ margin: "0 auto 16px" }} />
            <h3 style={{ color: "#e2e8f0", fontSize: "18px", fontWeight: 600, marginBottom: "8px" }}>No hay dominios guardados</h3>
            <p style={{ color: "#64748b", maxWidth: "400px", margin: "0 auto" }}>Agrega tu primer dominio para comenzar a analizar vulnerabilidades y obtener recomendaciones de IA.</p>
          </div>
        )}
      </div>
    </div>
  );
}

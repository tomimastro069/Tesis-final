import { useState, useEffect } from "react";
import { Plus, Shield, ArrowRight, Server } from "lucide-react";
import { ScanForm } from "./ScanForm";
import { fetchScanResults } from "../../services/api";
import { parseSecurityResults } from "../../utils/parser";
import type { Domain } from "../../services/api";

export function DomainsDashboard({ onSelectDomain }: { onSelectDomain: (domain: Domain) => void }) {
  const [domains, setDomains] = useState<Domain[]>([]);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    // Para la migración a base de datos, limpiamos el caché viejo
    const isMigrated = localStorage.getItem("securAudit_migrated_db");
    if (!isMigrated) {
      localStorage.removeItem("securAudit_domains");
      localStorage.setItem("securAudit_migrated_db", "true");
    }

    const saved = localStorage.getItem("securAudit_domains");
    if (saved) {
      setDomains(JSON.parse(saved));
    }
  }, []);

  // Polling para dominios en estado 'scanning'
  useEffect(() => {
    let interval: number;
    const hasScanning = domains.some(d => d.status === 'scanning');
    
    if (hasScanning) {
      interval = window.setInterval(async () => {
        try {
          const scanningDomains = domains.filter(d => d.status === 'scanning' && d.scanId);
          for (const d of scanningDomains) {
            const results = await fetchScanResults(d.scanId!);
            if (results && results.status === 'completed' && results.results) {
              const parsed = parseSecurityResults(results.results);
              if (parsed) {
                setDomains(prev => {
                  const updated = prev.map(pd => pd.id === d.id ? { ...pd, status: 'completed' as const, score: parsed.score, riskLevel: parsed.riskLevel } : pd);
                  localStorage.setItem("securAudit_domains", JSON.stringify(updated));
                  return updated;
                });
              }
            } else if (results && results.status === 'failed') {
              setDomains(prev => {
                const updated = prev.map(pd => pd.id === d.id ? { ...pd, status: 'error' as const } : pd);
                localStorage.setItem("securAudit_domains", JSON.stringify(updated));
                return updated;
              });
            }
          }
        } catch (error) {
          console.error("Error durante el polling:", error);
        }
      }, 10000); // Consulta cada 10 segundos
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [domains]);

  const handleAddDomain = (domain: Domain) => {
    const updated = [...domains, domain];
    setDomains(updated);
    localStorage.setItem("securAudit_domains", JSON.stringify(updated));
    setShowForm(false);
  };

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
          <ScanForm onCancel={() => setShowForm(false)} onSuccess={handleAddDomain} />
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
                    {domain.status === 'scanning' ? 'Analizando...' : domain.status === 'completed' ? 'Análisis Completado' : 'Pendiente'}
                  </span>
                </div>
              </div>
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
                {domain.status === 'scanning' ? "Análisis en progreso..." : "Ver detalles"}
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

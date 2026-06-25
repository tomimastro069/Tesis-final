import { useEffect, useState } from "react";
import { ChartsSection } from "./ChartsSection";
import { VulnerabilityTable, Vulnerability } from "./VulnerabilityTable";
import { fetchScanResults } from "../../services/api";
import { parseSecurityResults } from "../../utils/parser";
import {
  Download,
  AlertCircle,
  CheckCircle2,
  TrendingDown,
  TrendingUp,
  Search,
  Link,
  Shield,
  Activity,
  Settings,
} from "lucide-react";

const glassCard = {
  background: "rgba(255, 255, 255, 0.025)",
  backdropFilter: "blur(20px)",
  WebkitBackdropFilter: "blur(20px)",
  border: "1px solid rgba(255, 255, 255, 0.07)",
  borderRadius: "16px",
  padding: "24px",
  fontFamily: "'Inter', sans-serif",
  position: "relative" as const,
  overflow: "hidden" as const,
};

function ScoreRing({ score, color }: { score: number; color: string }) {
  const radius = 44;
  const stroke = 6;
  const normalizedRadius = radius - stroke / 2;
  const circumference = 2 * Math.PI * normalizedRadius;
  const offset = circumference - (score / 100) * circumference;

  return (
    <svg width={radius * 2} height={radius * 2} style={{ transform: "rotate(-90deg)" }}>
      <circle
        cx={radius}
        cy={radius}
        r={normalizedRadius}
        fill="none"
        stroke="rgba(255,255,255,0.06)"
        strokeWidth={stroke}
      />
      <circle
        cx={radius}
        cy={radius}
        r={normalizedRadius}
        fill="none"
        stroke={color}
        strokeWidth={stroke}
        strokeDasharray={`${circumference} ${circumference}`}
        strokeDashoffset={offset}
        strokeLinecap="round"
        style={{
          filter: `drop-shadow(0 0 8px ${color}80)`,
          transition: "stroke-dashoffset 1s ease-in-out",
        }}
      />
    </svg>
  );
}

import { Domain } from "../../services/api";

export function ScanReport({ domain }: { domain: Domain }) {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    async function loadData() {
      if (!domain.scanId) {
        setLoading(false);
        return;
      }
      setLoading(true);
      try {
        const result = await fetchScanResults(domain.scanId);
        if (result && result.results) {
          const parsed = parseSecurityResults(result.results);
          setData(parsed);
        } else {
          setData(null);
        }
      } catch (e) {
        console.error("Failed to load results", e);
        setData(null);
      }
      setLoading(false);
    }
    loadData();
  }, [domain]);

  if (loading) {
    return (
      <div style={{ padding: "40px", color: "#94a3b8", textAlign: "center" }}>
        Cargando reporte de análisis para {domain.target}...
      </div>
    );
  }

  if (!data) {
    return (
      <div style={{ padding: "40px", color: "#ef4444", textAlign: "center" }}>
        Error al cargar datos. ¿Se ha completado un análisis para {domain.target}?
      </div>
    );
  }

  const GRADE = data.score >= 85 ? "A" : data.score >= 65 ? "B" : data.score >= 45 ? "C" : "D";
  const GRADE_COLOR =
    data.score >= 85 ? "#10b981" : data.score >= 65 ? "#d97706" : data.score >= 45 ? "#ea580c" : "#dc2626";

  return (
    <div style={{ padding: "24px 28px", maxWidth: "1400px" }}>
      {/* Header controls inside report */}
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "24px" }}>
        <div>
          <h2 style={{ fontSize: "20px", color: "#f8fafc", margin: 0, marginBottom: "4px" }}>Resumen de Seguridad</h2>
          <div style={{ fontSize: "13px", color: "#94a3b8" }}>Objetivo: {domain.target}</div>
        </div>
      </div>

      {/* KPI Cards */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr 1fr",
          gap: "16px",
          marginBottom: "16px",
        }}
      >
        {/* Card 1: Global Risk Level */}
        <div style={glassCard}>
          <div
            style={{
              position: "absolute",
              top: 0,
              right: 0,
              width: "120px",
              height: "120px",
              background: `radial-gradient(circle at 70% 30%, ${GRADE_COLOR}15 0%, transparent 70%)`,
              pointerEvents: "none",
            }}
          />
          <div style={{ fontSize: "11px", fontWeight: 600, color: "#475569", letterSpacing: "0.8px", marginBottom: "16px" }}>
            NIVEL DE RIESGO GLOBAL
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "20px" }}>
            <div style={{ position: "relative", flexShrink: 0 }}>
              <ScoreRing score={data.score} color={GRADE_COLOR} />
              <div
                style={{
                  position: "absolute",
                  inset: 0,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  flexDirection: "column",
                }}
              >
                <span
                  style={{
                    fontSize: "22px",
                    fontWeight: 800,
                    color: GRADE_COLOR,
                    lineHeight: 1,
                  }}
                >
                  {GRADE}
                </span>
              </div>
            </div>
            <div>
              <div style={{ fontSize: "36px", fontWeight: 800, color: GRADE_COLOR, lineHeight: 1, marginBottom: "4px" }}>
                {data.score}
                <span style={{ fontSize: "16px", fontWeight: 500, color: "#64748b" }}>/100</span>
              </div>
              <div style={{ fontSize: "12px", color: "#64748b", marginBottom: "8px" }}>
                Puntuación de Seguridad
              </div>
            </div>
          </div>
          <div
            style={{
              marginTop: "16px",
              paddingTop: "14px",
              borderTop: "1px solid rgba(255,255,255,0.05)",
              display: "flex",
              justifyContent: "space-between",
            }}
          >
            {data.severityData.map((item: any) => (
              <div key={item.name} style={{ textAlign: "center" }}>
                <div style={{ fontSize: "16px", fontWeight: 700, color: item.color }}>
                  {item.count}
                </div>
                <div style={{ fontSize: "10px", color: "#334155", marginTop: "2px" }}>
                  {item.name}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Card 2: Total Vulnerabilities */}
        <div style={glassCard}>
          <div
            style={{
              position: "absolute",
              top: 0,
              right: 0,
              width: "120px",
              height: "120px",
              background: "radial-gradient(circle at 70% 30%, rgba(234,88,12,0.08) 0%, transparent 70%)",
              pointerEvents: "none",
            }}
          />
          <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: "16px" }}>
            <span style={{ fontSize: "11px", fontWeight: 600, color: "#475569", letterSpacing: "0.8px" }}>
              TOTAL DE VULNERABILIDADES
            </span>
            <div
              style={{
                width: "36px",
                height: "36px",
                borderRadius: "10px",
                background: "rgba(234, 88, 12, 0.1)",
                border: "1px solid rgba(234, 88, 12, 0.2)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <AlertCircle size={18} color="#ea580c" />
            </div>
          </div>
          <div style={{ fontSize: "52px", fontWeight: 800, color: "#e2e8f0", lineHeight: 1, marginBottom: "6px", letterSpacing: "-2px" }}>
            {data.total}
          </div>
          <div style={{ fontSize: "12px", color: "#64748b", marginBottom: "16px" }}>
            Detectado en{" "}
            <span style={{ color: "#94a3b8", fontWeight: 500 }}>{domain.target}</span>
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "12px", marginTop: "12px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "10px", background: "rgba(255,255,255,0.02)", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)" }}>
              <Link size={16} color="#94a3b8" />
              <div>
                <div style={{ fontSize: "11px", color: "#64748b", fontWeight: 500 }}>Endpoints Vulnerables</div>
                <div style={{ fontSize: "14px", color: "#f8fafc", fontWeight: 600 }}>{data.scanMetrics?.uniqueEndpoints || 0}</div>
              </div>
            </div>
            
            <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "10px", background: "rgba(255,255,255,0.02)", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)" }}>
              <Shield size={16} color="#94a3b8" />
              <div>
                <div style={{ fontSize: "11px", color: "#64748b", fontWeight: 500 }}>Herramientas de Análisis</div>
                <div style={{ fontSize: "14px", color: "#f8fafc", fontWeight: 600 }}>{data.scanMetrics?.scanners || "Desconocido"}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Card 3: Threat Nature */}
        <div style={glassCard}>
          <div
            style={{
              position: "absolute",
              top: 0,
              right: 0,
              width: "120px",
              height: "120px",
              background: "radial-gradient(circle at 70% 30%, rgba(139, 92, 246, 0.08) 0%, transparent 70%)",
              pointerEvents: "none",
            }}
          />
          <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: "16px" }}>
            <span style={{ fontSize: "11px", fontWeight: 600, color: "#475569", letterSpacing: "0.8px" }}>
              NATURALEZA DE LA AMENAZA
            </span>
            <div
              style={{
                width: "36px",
                height: "36px",
                borderRadius: "10px",
                background: "rgba(139, 92, 246, 0.1)",
                border: "1px solid rgba(139, 92, 246, 0.2)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Activity size={18} color="#8b5cf6" />
            </div>
          </div>
          
          <div style={{ display: "flex", flexDirection: "column", gap: "12px", marginTop: "4px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "10px", background: "rgba(255,255,255,0.02)", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)" }}>
              <div style={{ padding: "6px", background: "rgba(220, 38, 38, 0.1)", borderRadius: "6px" }}>
                <Activity size={14} color="#ef4444" />
              </div>
              <div>
                <div style={{ fontSize: "11px", color: "#64748b", fontWeight: 500 }}>Fallas de Inyección</div>
                <div style={{ fontSize: "14px", color: "#f8fafc", fontWeight: 600 }}>{data.scanMetrics?.threatNature?.injection || 0}</div>
              </div>
            </div>
            
            <div style={{ display: "flex", alignItems: "center", gap: "12px", padding: "10px", background: "rgba(255,255,255,0.02)", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.05)" }}>
              <div style={{ padding: "6px", background: "rgba(59, 130, 246, 0.1)", borderRadius: "6px" }}>
                <Settings size={14} color="#3b82f6" />
              </div>
              <div>
                <div style={{ fontSize: "11px", color: "#64748b", fontWeight: 500 }}>Fallas de Configuración</div>
                <div style={{ fontSize: "14px", color: "#f8fafc", fontWeight: 600 }}>{data.scanMetrics?.threatNature?.configuration || 0}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <ChartsSection 
        typesData={data.typesData} 
        topVulnerableUrls={data.scanMetrics?.topVulnerableUrls} 
        stackedSeverityByType={data.scanMetrics?.stackedSeverityByType}
      />

      {/* Vulnerability Table */}
      <div style={{ marginTop: "24px" }}>
        <VulnerabilityTable vulnerabilities={data.allVulnerabilities} targetUrl={domain.target} />
      </div>

    </div>
  );
}

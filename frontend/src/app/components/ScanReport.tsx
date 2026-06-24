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

export function ScanReport({ targetUrl }: { targetUrl: string }) {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const raw = await fetchScanResults();
        // Since we only scan one domain, we just use the raw result (assuming it corresponds to targetUrl)
        const parsed = parseSecurityResults(raw);
        setData(parsed);
      } catch (e) {
        console.error("Failed to load results", e);
      }
      setLoading(false);
    }
    loadData();
  }, [targetUrl]);

  if (loading) {
    return (
      <div style={{ padding: "40px", color: "#94a3b8", textAlign: "center" }}>
        Cargando reporte de análisis para {targetUrl}...
      </div>
    );
  }

  if (!data) {
    return (
      <div style={{ padding: "40px", color: "#ef4444", textAlign: "center" }}>
        Error al cargar datos. ¿Se ha completado un análisis para {targetUrl}?
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
          <div style={{ fontSize: "13px", color: "#94a3b8" }}>Objetivo: {targetUrl}</div>
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
            <span style={{ color: "#94a3b8", fontWeight: 500 }}>{targetUrl}</span>
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            {data.severityData.map((item: any) => {
              const perc = data.total > 0 ? (item.count / data.total) * 100 : 0;
              return (
                <div key={item.name} style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                  <div style={{ width: "48px", fontSize: "10px", color: "#475569", fontWeight: 500 }}>
                    {item.name}
                  </div>
                  <div style={{ flex: 1, height: "4px", background: "rgba(255,255,255,0.06)", borderRadius: "4px" }}>
                    <div
                      style={{
                        width: `${perc}%`,
                        height: "100%",
                        background: item.color,
                        borderRadius: "4px",
                        boxShadow: `0 0 6px ${item.color}60`,
                      }}
                    />
                  </div>
                  <div style={{ width: "24px", fontSize: "11px", fontWeight: 600, color: item.color, textAlign: "right" }}>
                    {item.count}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Card 3: Resolved Vulnerabilities (Mocked for single scan) */}
        <div style={glassCard}>
          <div
            style={{
              position: "absolute",
              top: 0,
              right: 0,
              width: "120px",
              height: "120px",
              background: "radial-gradient(circle at 70% 30%, rgba(16,185,129,0.07) 0%, transparent 70%)",
              pointerEvents: "none",
            }}
          />
          <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: "16px" }}>
            <span style={{ fontSize: "11px", fontWeight: 600, color: "#475569", letterSpacing: "0.8px" }}>
              ELEMENTOS DE ACCIÓN
            </span>
            <div
              style={{
                width: "36px",
                height: "36px",
                borderRadius: "10px",
                background: "rgba(16, 185, 129, 0.1)",
                border: "1px solid rgba(16, 185, 129, 0.2)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <CheckCircle2 size={18} color="#10b981" />
            </div>
          </div>
          <div style={{ fontSize: "52px", fontWeight: 800, color: "#e2e8f0", lineHeight: 1, marginBottom: "6px", letterSpacing: "-2px" }}>
            {data.severityData.find((s:any)=>s.name==="High")?.count + data.severityData.find((s:any)=>s.name==="Critical")?.count}
          </div>
          <div style={{ fontSize: "12px", color: "#64748b", marginBottom: "16px" }}>
            Requieren Acción Inmediata
          </div>

        </div>
      </div>

      {/* Charts Row */}
      <ChartsSection typesData={data.typesData} severityData={data.severityData} />

      {/* Vulnerability Table */}
      <div style={{ marginTop: "24px" }}>
        <VulnerabilityTable vulnerabilities={data.allVulnerabilities} />
      </div>

    </div>
  );
}

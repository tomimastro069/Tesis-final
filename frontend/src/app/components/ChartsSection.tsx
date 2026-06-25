import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { ScrollArea } from "./ui/scroll-area";

const TIMELINE_DATA = [
  { month: "Jan", total: 187, resolved: 44 },
  { month: "Feb", total: 175, resolved: 62 },
  { month: "Mar", total: 163, resolved: 78 },
  { month: "Apr", total: 154, resolved: 83 },
  { month: "May", total: 147, resolved: 89 },
  { month: "Jun", total: 134, resolved: 97 },
];

const glassCard = {
  background: "rgba(255, 255, 255, 0.025)",
  backdropFilter: "blur(20px)",
  WebkitBackdropFilter: "blur(20px)",
  border: "1px solid rgba(255, 255, 255, 0.07)",
  borderRadius: "16px",
  padding: "24px",
  fontFamily: "'Inter', sans-serif",
};

interface ChartsSectionProps {
  typesData: { name: string; value: number; color: string }[];
  topVulnerableUrls?: { url: string; count: number }[];
  stackedSeverityByType?: { name: string; Critical: number; High: number; Medium: number; Low: number }[];
}

export function ChartsSection({ typesData, topVulnerableUrls, stackedSeverityByType }: ChartsSectionProps) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
        gap: "24px",
      }}
    >
      {/* 1. Vulnerability Types Distribution */}
      <div style={glassCard}>
        <div style={{ marginBottom: "20px" }}>
          <h3
            style={{
              color: "#e2e8f0",
              fontSize: "14px",
              fontWeight: 600,
              margin: 0,
              marginBottom: "4px",
            }}
          >
            Tipos de Vulnerabilidad
          </h3>
          <p style={{ fontSize: "11px", color: "#64748b", margin: 0 }}>
            Distribución de riesgos de seguridad identificados por categoría
          </p>
        </div>
        <div style={{ height: "220px" }}>
          {typesData.length > 0 ? (
            <ScrollArea style={{ height: "100%" }}>
              <div
                style={{
                  paddingRight: "10px",
                  display: "flex",
                  flexDirection: "column",
                  gap: "8px",
                }}
              >
                {typesData.map((entry, index) => (
                  <div
                    key={`list-item-${index}`}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      padding: "8px 12px",
                      background: "rgba(255, 255, 255, 0.02)",
                      border: "1px solid rgba(255, 255, 255, 0.05)",
                      borderRadius: "8px",
                      fontSize: "12px",
                      transition: "background 0.2s ease",
                    }}
                  >
                    <div style={{ display: "flex", alignItems: "center", gap: "10px", minWidth: 0, marginRight: "12px" }}>
                      <span
                        style={{
                          width: "8px",
                          height: "8px",
                          borderRadius: "50%",
                          background: entry.color,
                          flexShrink: 0,
                        }}
                      />
                      <span style={{ color: "#f8fafc", fontWeight: 500, wordBreak: "break-word" }}>
                        {entry.name}
                      </span>
                    </div>
                    <span
                      style={{
                        color: entry.color,
                        fontWeight: 600,
                        background: `${entry.color}15`,
                        padding: "2px 8px",
                        borderRadius: "12px",
                        fontSize: "10px",
                        border: `1px solid ${entry.color}30`,
                        whiteSpace: "nowrap",
                        flexShrink: 0,
                      }}
                    >
                      {entry.value} {entry.value === 1 ? 'hallazgo' : 'hallazgos'}
                    </span>
                  </div>
                ))}
              </div>
            </ScrollArea>
          ) : (
             <div style={{ height: "100%", display: "flex", alignItems: "center", justifyContent: "center", color: "#64748b" }}>
               No hay datos disponibles
             </div>
          )}
        </div>
      </div>

      {/* 2. Severity Breakdown */}
      <div style={glassCard}>
        <div style={{ marginBottom: "20px" }}>
          <h3
            style={{
              color: "#e2e8f0",
              fontSize: "14px",
              fontWeight: 600,
              margin: 0,
              marginBottom: "4px",
            }}
          >
            Top URLs Vulnerables
          </h3>
          <p style={{ fontSize: "11px", color: "#64748b", margin: 0 }}>
            Endpoints con mayor cantidad de hallazgos
          </p>
        </div>
        <div style={{ height: "220px" }}>
          {topVulnerableUrls && topVulnerableUrls.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={topVulnerableUrls}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 10, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={false} />
                <XAxis type="number" stroke="#475569" fontSize={10} tickLine={false} axisLine={false} />
                <YAxis
                  dataKey="url"
                  type="category"
                  stroke="#64748b"
                  fontSize={10}
                  tickLine={false}
                  axisLine={false}
                  width={120}
                  tickFormatter={(val) => val.length > 20 ? "..." + val.slice(-17) : val}
                />
                <Tooltip
                  cursor={{ fill: "rgba(255,255,255,0.02)" }}
                  contentStyle={{
                    background: "rgba(10, 8, 28, 0.9)",
                    border: "1px solid rgba(255,255,255,0.1)",
                    borderRadius: "8px",
                    color: "#e2e8f0",
                    fontSize: "12px",
                  }}
                  formatter={(value: number) => [`${value} vulnerabilidades`, "Cantidad"]}
                />
                <Bar dataKey="count" radius={[0, 4, 4, 0]} barSize={20} fill="#ea580c" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div style={{ display: "flex", height: "100%", alignItems: "center", justifyContent: "center", color: "#64748b", fontSize: "12px" }}>
              No hay suficientes datos de URLs
            </div>
          )}
        </div>
      </div>

      {/* 3. Severity by Type (Stacked Bar Chart) */}
      <div style={glassCard}>
        <div style={{ marginBottom: "20px" }}>
          <h3
            style={{
              color: "#e2e8f0",
              fontSize: "14px",
              fontWeight: 600,
              margin: 0,
              marginBottom: "4px",
            }}
          >
            Gravedad por Tipo de Vulnerabilidad
          </h3>
          <p style={{ fontSize: "11px", color: "#64748b", margin: 0 }}>
            Composición del impacto para cada categoría detectada
          </p>
        </div>
        <div style={{ height: "220px" }}>
          {stackedSeverityByType && stackedSeverityByType.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={stackedSeverityByType}
                margin={{ top: 5, right: 10, left: -20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis 
                  dataKey="name" 
                  stroke="#475569" 
                  fontSize={10} 
                  tickLine={false} 
                  axisLine={false} 
                  tickFormatter={(val) => val.length > 15 ? val.slice(0, 12) + "..." : val}
                />
                <YAxis stroke="#475569" fontSize={10} tickLine={false} axisLine={false} />
                <Tooltip
                  cursor={{ fill: "rgba(255,255,255,0.02)" }}
                  contentStyle={{
                    background: "rgba(10, 8, 28, 0.9)",
                    border: "1px solid rgba(255,255,255,0.1)",
                    borderRadius: "8px",
                    color: "#e2e8f0",
                    fontSize: "12px",
                  }}
                />
                <Legend
                  verticalAlign="top"
                  height={36}
                  iconType="circle"
                  wrapperStyle={{ fontSize: "11px", color: "#94a3b8" }}
                />
                <Bar dataKey="Critical" stackId="a" fill="#dc2626" name="Crítico" barSize={30} />
                <Bar dataKey="High" stackId="a" fill="#ea580c" name="Alto" />
                <Bar dataKey="Medium" stackId="a" fill="#d97706" name="Medio" />
                <Bar dataKey="Low" stackId="a" fill="#3b82f6" name="Bajo" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div style={{ display: "flex", height: "100%", alignItems: "center", justifyContent: "center", color: "#64748b", fontSize: "12px" }}>
              No hay datos para mostrar
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

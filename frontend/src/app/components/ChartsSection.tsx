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
  severityData: { name: string; count: number; color: string }[];
}

export function ChartsSection({ typesData, severityData }: ChartsSectionProps) {
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
            Vulnerability Types
          </h3>
          <p style={{ fontSize: "11px", color: "#64748b", margin: 0 }}>
            Distribution of identified security risks by category
          </p>
        </div>
        <div style={{ height: "220px" }}>
          {typesData.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={typesData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {typesData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    background: "rgba(10, 8, 28, 0.9)",
                    border: "1px solid rgba(255,255,255,0.1)",
                    borderRadius: "8px",
                    color: "#e2e8f0",
                    fontSize: "12px",
                  }}
                  itemStyle={{ color: "#e2e8f0" }}
                />
                <Legend
                  verticalAlign="bottom"
                  height={36}
                  iconType="circle"
                  wrapperStyle={{ fontSize: "11px", color: "#94a3b8" }}
                />
              </PieChart>
            </ResponsiveContainer>
          ) : (
             <div style={{ height: "100%", display: "flex", alignItems: "center", justifyContent: "center", color: "#64748b" }}>
               No data available
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
            Severity Breakdown
          </h3>
          <p style={{ fontSize: "11px", color: "#64748b", margin: 0 }}>
            Findings categorized by potential impact
          </p>
        </div>
        <div style={{ height: "220px" }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={severityData}
              layout="vertical"
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={false} />
              <XAxis type="number" stroke="#475569" fontSize={10} tickLine={false} axisLine={false} />
              <YAxis
                dataKey="name"
                type="category"
                stroke="#64748b"
                fontSize={11}
                tickLine={false}
                axisLine={false}
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
              />
              <Bar dataKey="count" radius={[0, 4, 4, 0]} barSize={20}>
                {severityData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 3. Remediation Progress */}
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
            Remediation Timeline
          </h3>
          <p style={{ fontSize: "11px", color: "#64748b", margin: 0 }}>
            6-month trend of vulnerabilities vs resolved issues
          </p>
        </div>
        <div style={{ height: "220px" }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={TIMELINE_DATA}
              margin={{ top: 5, right: 10, left: -20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
              <XAxis dataKey="month" stroke="#475569" fontSize={10} tickLine={false} axisLine={false} />
              <YAxis stroke="#475569" fontSize={10} tickLine={false} axisLine={false} />
              <Tooltip
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
                iconType="plainline"
                wrapperStyle={{ fontSize: "11px", color: "#94a3b8" }}
              />
              <Line
                type="monotone"
                dataKey="total"
                name="Total Findings"
                stroke="#64748b"
                strokeWidth={2}
                dot={{ r: 3, fill: "#64748b", strokeWidth: 0 }}
                activeDot={{ r: 5 }}
              />
              <Line
                type="monotone"
                dataKey="resolved"
                name="Resolved"
                stroke="#10b981"
                strokeWidth={2}
                dot={{ r: 3, fill: "#10b981", strokeWidth: 0 }}
                activeDot={{ r: 5 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

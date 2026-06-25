import { useState } from "react";
import { launchScan } from "../../services/api";
import type { Domain, ScanRequest } from "../../services/api";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";

export function ScanForm({ onCancel, onSuccess }: { onCancel: () => void, onSuccess: (domain: Domain) => void }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<ScanRequest>({
    target: "http://dvwa",
    nivel: "medium",
    sqlmap_level: "basic",
    cookies: "",
    clean_cache: false
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await launchScan(formData);
      const newDomain: Domain = {
        id: Date.now().toString(),
        target: formData.target,
        scanId: res.scan_id,
        lastScan: new Date().toISOString(),
        score: null,
        riskLevel: null,
        status: "scanning"
      };
      onSuccess(newDomain);
    } catch (err: any) {
      setError(err.message || "Error al lanzar el análisis");
      setLoading(false);
    }
  };

  const inputStyle = {
    width: "100%",
    padding: "10px 14px",
    background: "rgba(0, 0, 0, 0.2)",
    border: "1px solid rgba(255, 255, 255, 0.1)",
    borderRadius: "8px",
    color: "#e2e8f0",
    fontSize: "14px",
    marginBottom: "16px"
  };

  return (
    <div style={{ background: "rgba(255, 255, 255, 0.03)", padding: "24px", borderRadius: "16px", border: "1px solid rgba(255, 255, 255, 0.08)" }}>
      <h3 style={{ color: "#e2e8f0", fontSize: "18px", fontWeight: 600, marginBottom: "20px" }}>Nuevo Análisis de Seguridad</h3>
      {error && <div style={{ padding: "12px", background: "rgba(220, 38, 38, 0.1)", border: "1px solid rgba(220, 38, 38, 0.2)", borderRadius: "8px", color: "#f87171", marginBottom: "16px", fontSize: "14px" }}>{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div>
          <label style={{ display: "block", fontSize: "13px", color: "#94a3b8", marginBottom: "6px", fontWeight: 500 }}>Dominio Objetivo (URL)</label>
          <input 
            type="url" 
            required 
            style={{...inputStyle, opacity: 0.5, cursor: "not-allowed"}}
            value="http://dvwa"
            disabled
          />
        </div>

        <div>
          <label style={{ display: "block", fontSize: "13px", color: "#94a3b8", marginBottom: "6px", fontWeight: 500 }}>Cookie de Sesión (Opcional)</label>
          <input 
            type="text" 
            placeholder="ej. PHPSESSID=123..; security=low" 
            style={inputStyle}
            value={formData.cookies}
            onChange={(e) => setFormData({...formData, cookies: e.target.value})}
          />
        </div>

        <div style={{ display: "flex", alignItems: "center", marginBottom: "16px" }}>
          <input 
            type="checkbox" 
            id="cleanCache"
            checked={formData.clean_cache}
            onChange={(e) => setFormData({...formData, clean_cache: e.target.checked})}
            style={{ marginRight: "8px", width: "16px", height: "16px", accentColor: "#3b82f6" }}
          />
          <label htmlFor="cleanCache" style={{ fontSize: "13px", color: "#e2e8f0", cursor: "pointer" }}>
            Limpiar la caché antes de empezar
          </label>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
          <div>
            <label style={{ display: "block", fontSize: "13px", color: "#94a3b8", marginBottom: "6px", fontWeight: 500 }}>Nivel de Análisis</label>
            <Select value={formData.nivel} onValueChange={(val) => setFormData({...formData, nivel: val})}>
              <SelectTrigger style={inputStyle}>
                <SelectValue placeholder="Nivel de Análisis" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="small">Básico</SelectItem>
                <SelectItem value="medium">Profundo</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <label style={{ display: "block", fontSize: "13px", color: "#94a3b8", marginBottom: "6px", fontWeight: 500 }}>Nivel SQLMap</label>
            <Select value={formData.sqlmap_level} onValueChange={(val) => setFormData({...formData, sqlmap_level: val})}>
              <SelectTrigger style={inputStyle}>
                <SelectValue placeholder="Nivel SQLMap" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="basic">1 - Básico (Recomendado)</SelectItem>
                <SelectItem value="fast_evidence">2 - Evidencia Rápida</SelectItem>
                <SelectItem value="full_dump">3 - Extracción Completa (Lento)</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <div style={{ display: "flex", justifyContent: "flex-end", gap: "12px", marginTop: "16px" }}>
          <button type="button" onClick={onCancel} style={{ padding: "8px 16px", background: "transparent", border: "1px solid rgba(255,255,255,0.1)", color: "#cbd5e1", borderRadius: "8px", cursor: "pointer", fontWeight: 500 }}>
            Cancelar
          </button>
          <button type="submit" disabled={loading} style={{ padding: "8px 16px", background: "linear-gradient(135deg, #06b6d4, #3b82f6)", border: "none", color: "white", borderRadius: "8px", cursor: "pointer", fontWeight: 600, opacity: loading ? 0.7 : 1 }}>
            {loading ? 'Iniciando...' : 'Comenzar Análisis'}
          </button>
        </div>
      </form>
    </div>
  );
}

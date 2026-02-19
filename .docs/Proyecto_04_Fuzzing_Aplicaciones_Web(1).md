# Proyecto 4: Fuzzing Automatizado de Aplicaciones Web

## 📋 Información General

**Nivel de Dificultad**: Avanzado
**Tiempo Estimado**: 10-14 horas
**Categoría**: Web Application Security & Automated Testing

## 🎯 Objetivos de Aprendizaje

1. Comprender el concepto y metodología de fuzzing
2. Identificar vulnerabilidades web comunes (OWASP Top 10)
3. Automatizar pruebas de seguridad en aplicaciones web
4. Interpretar resultados de escaneos y priorizar remediación
5. Integrar testing de seguridad en pipelines CI/CD

## 🔧 Herramientas Requeridas

- **N8N**: Automatización del flujo
- **Burp Suite Professional**: Escáner de vulnerabilidades web (o versión Community + extensiones)
- **OWASP ZAP**: Alternativa open-source a Burp Suite
- **DVWA** (Damn Vulnerable Web Application): Aplicación vulnerable para pruebas
- **wfuzz**: Fuzzer de línea de comandos
- **ffuf**: Fast web fuzzer
- **SQLMap**: Detector de inyecciones SQL automatizado

## 🏗️ Configuración del Laboratorio

### Arquitectura

```
┌────────────────────────────────────────────────────┐
│         Entorno de Fuzzing Automatizado            │
│                                                    │
│  ┌──────────────┐         ┌──────────────┐       │
│  │     N8N      │────────▶│ Burp Suite   │       │
│  │ Orchestrator │         │     API      │       │
│  └──────┬───────┘         └──────┬───────┘       │
│         │                        │               │
│         │                        │               │
│         ▼                        ▼               │
│  ┌──────────────┐         ┌──────────────┐       │
│  │  OWASP ZAP   │────────▶│    DVWA      │       │
│  │     API      │         │ (Target App) │       │
│  └──────────────┘         └──────────────┘       │
│         │                                         │
│         ▼                                         │
│  ┌──────────────┐                                │
│  │  PostgreSQL  │                                │
│  │ (Results DB) │                                │
│  └──────────────┘                                │
└────────────────────────────────────────────────────┘
```

### Instalación de DVWA

```bash
# Usando Docker (recomendado)
docker pull vulnerables/web-dvwa
docker run -d -p 8080:80 --name dvwa vulnerables/web-dvwa

# Acceder a: http://localhost:8080
# Usuario: admin
# Password: password
```

### Instalación de OWASP ZAP

```bash
# Descargar desde: https://www.zaproxy.org/download/
# O instalar con snap
sudo snap install zaproxy --classic

# Iniciar en modo daemon
zap.sh -daemon -host 0.0.0.0 -port 8090 -config api.key=YOUR_API_KEY
```

### Instalación de Herramientas de Fuzzing

```bash
# wfuzz
pip3 install wfuzz

# ffuf
go install github.com/ffuf/ffuf/v2@latest

# SQLMap
git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git
cd sqlmap
python3 sqlmap.py --version
```

## 🔄 Workflow N8N - Fuzzing Automatizado

### Flujo Completo

```
[Manual Trigger] → [Spider/Crawl] → [Passive Scan] → [Active Scan]
                                                            ↓
                      [Report Generation] ← [SQLMap Test] ←┘
                                ↓
                      [Store in DB] → [Email Report]
```

### Nodo 1: ZAP Spider (Descubrimiento)

```javascript
// Iniciar spider en OWASP ZAP
const axios = require('axios');

const ZAP_URL = 'http://localhost:8090';
const API_KEY = process.env.ZAP_API_KEY;
const TARGET_URL = 'http://localhost:8080';

// Iniciar spider
const spiderResponse = await axios.get(`${ZAP_URL}/JSON/spider/action/scan/`, {
  params: {
    apikey: API_KEY,
    url: TARGET_URL,
    maxChildren: 10,
    recurse: true
  }
});

const scanId = spiderResponse.data.scan;

// Esperar a que complete el spider
let progress = 0;
while (progress < 100) {
  await new Promise(resolve => setTimeout(resolve, 2000));

  const statusResponse = await axios.get(`${ZAP_URL}/JSON/spider/view/status/`, {
    params: {
      apikey: API_KEY,
      scanId: scanId
    }
  });

  progress = parseInt(statusResponse.data.status);
}

// Obtener URLs descubiertas
const urlsResponse = await axios.get(`${ZAP_URL}/JSON/spider/view/results/`, {
  params: {
    apikey: API_KEY,
    scanId: scanId
  }
});

const discoveredUrls = urlsResponse.data.results;

return [{
  json: {
    scanId: scanId,
    urlsDiscovered: discoveredUrls,
    count: discoveredUrls.length
  }
}];
```

### Nodo 2: Passive Scan

```javascript
// Escaneo pasivo de ZAP
const urls = $input.first().json.urlsDiscovered;

// ZAP automáticamente realiza escaneo pasivo durante el spider
// Recuperar resultados del escaneo pasivo

const alertsResponse = await axios.get(`${ZAP_URL}/JSON/core/view/alerts/`, {
  params: {
    apikey: API_KEY,
    baseurl: TARGET_URL
  }
});

const passiveAlerts = alertsResponse.data.alerts.filter(alert =>
  alert.pluginId < 100000 // IDs bajos son escaneos pasivos
);

return [{
  json: {
    passiveAlerts: passiveAlerts,
    count: passiveAlerts.length
  }
}];
```

### Nodo 3: Active Scan

```javascript
// Escaneo activo de ZAP (más intrusivo)
const activeScanResponse = await axios.get(`${ZAP_URL}/JSON/ascan/action/scan/`, {
  params: {
    apikey: API_KEY,
    url: TARGET_URL,
    recurse: true,
    inScopeOnly: false
  }
});

const activeScanId = activeScanResponse.data.scan;

// Monitorear progreso
let progress = 0;
while (progress < 100) {
  await new Promise(resolve => setTimeout(resolve, 5000));

  const statusResponse = await axios.get(`${ZAP_URL}/JSON/ascan/view/status/`, {
    params: {
      apikey: API_KEY,
      scanId: activeScanId
    }
  });

  progress = parseInt(statusResponse.data.status);
  console.log(`Active scan progress: ${progress}%`);
}

// Recuperar alertas del escaneo activo
const alertsResponse = await axios.get(`${ZAP_URL}/JSON/core/view/alerts/`, {
  params: {
    apikey: API_KEY,
    baseurl: TARGET_URL
  }
});

const activeAlerts = alertsResponse.data.alerts.filter(alert =>
  alert.pluginId >= 100000 // IDs altos son escaneos activos
);

return [{
  json: {
    activeScanId: activeScanId,
    activeAlerts: activeAlerts,
    count: activeAlerts.length
  }
}];
```

### Nodo 4: SQLMap Integration

```javascript
// Detectar parámetros vulnerables a SQL injection
const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

const urls = $input.first().json.urlsDiscovered || [];

// Filtrar URLs con parámetros GET
const urlsWithParams = urls.filter(url => url.includes('?'));

const sqlmapResults = [];

for (const url of urlsWithParams) {
  try {
    // Ejecutar SQLMap
    const command = `python3 /path/to/sqlmap/sqlmap.py -u "${url}" --batch --random-agent --level=2 --risk=2 --output-dir=/tmp/sqlmap --format=JSON`;

    const { stdout, stderr } = await execAsync(command, {
      timeout: 300000 // 5 minutos timeout
    });

    // Parsear resultados
    if (stdout.includes('Parameter:') && stdout.includes('is vulnerable')) {
      sqlmapResults.push({
        url: url,
        vulnerable: true,
        details: stdout
      });
    } else {
      sqlmapResults.push({
        url: url,
        vulnerable: false
      });
    }

  } catch (error) {
    sqlmapResults.push({
      url: url,
      error: error.message
    });
  }
}

return [{
  json: {
    sqlmapResults: sqlmapResults,
    vulnerableUrls: sqlmapResults.filter(r => r.vulnerable).length
  }
}];
```

### Nodo 5: Fuzzing con ffuf

```javascript
// Fuzzing de directorios y archivos ocultos
const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

const TARGET = 'http://localhost:8080';

// Descargar wordlist común
// wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt

const ffufCommand = `
  ffuf -u ${TARGET}/FUZZ \
    -w /path/to/common.txt \
    -mc 200,204,301,302,307,401,403 \
    -o /tmp/ffuf_results.json \
    -of json \
    -t 50 \
    -timeout 10
`;

const { stdout } = await execAsync(ffufCommand);

// Leer resultados JSON
const fs = require('fs');
const results = JSON.parse(fs.readFileSync('/tmp/ffuf_results.json', 'utf-8'));

return [{
  json: {
    ffufResults: results.results || [],
    discoveredPaths: results.results ? results.results.length : 0
  }
}];
```

### Nodo 6: Consolidar Resultados

```javascript
// Consolidar todos los hallazgos
const passiveAlerts = $input.all()[0].json.passiveAlerts || [];
const activeAlerts = $input.all()[1].json.activeAlerts || [];
const sqlmapResults = $input.all()[2].json.sqlmapResults || [];
const ffufResults = $input.all()[3].json.ffufResults || [];

// Clasificar por severidad según CVSS
function classifySeverity(risk) {
  const riskMap = {
    'High': 'critical',
    'Medium': 'high',
    'Low': 'medium',
    'Informational': 'low'
  };
  return riskMap[risk] || 'low';
}

// Consolidar vulnerabilidades
const allVulnerabilities = [];

// Procesar alertas de ZAP
[...passiveAlerts, ...activeAlerts].forEach(alert => {
  allVulnerabilities.push({
    source: 'OWASP ZAP',
    type: alert.alert,
    severity: classifySeverity(alert.risk),
    url: alert.url,
    description: alert.desc,
    solution: alert.solution,
    cweid: alert.cweid,
    wascid: alert.wascid,
    evidence: alert.evidence
  });
});

// Procesar SQLMap
sqlmapResults.filter(r => r.vulnerable).forEach(result => {
  allVulnerabilities.push({
    source: 'SQLMap',
    type: 'SQL Injection',
    severity: 'critical',
    url: result.url,
    description: 'SQL Injection vulnerability detected',
    solution: 'Use parameterized queries or prepared statements',
    evidence: result.details
  });
});

// Procesar ffuf
ffufResults.forEach(result => {
  if (result.status === 403 || result.status === 401) {
    allVulnerabilities.push({
      source: 'ffuf',
      type: 'Unauthorized Access Attempt',
      severity: 'low',
      url: result.url,
      description: `Found protected resource: ${result.status}`,
      solution: 'Verify access controls are properly configured'
    });
  }
});

// Estadísticas
const stats = {
  total: allVulnerabilities.length,
  critical: allVulnerabilities.filter(v => v.severity === 'critical').length,
  high: allVulnerabilities.filter(v => v.severity === 'high').length,
  medium: allVulnerabilities.filter(v => v.severity === 'medium').length,
  low: allVulnerabilities.filter(v => v.severity === 'low').length
};

return [{
  json: {
    vulnerabilities: allVulnerabilities,
    statistics: stats,
    scanDate: new Date().toISOString()
  }
}];
```

### Nodo 7: Generar Reporte

```javascript
// Generar reporte detallado
const data = $input.first().json;
const vulns = data.vulnerabilities;
const stats = data.statistics;

const report = `
# 🔍 Reporte de Fuzzing de Aplicación Web

**Fecha del Escaneo**: ${new Date(data.scanDate).toLocaleString('es-MX')}
**Aplicación Objetivo**: ${TARGET_URL}
**Total de Vulnerabilidades**: ${stats.total}

---

## 📊 Resumen Ejecutivo

| Severidad | Cantidad | Porcentaje |
|-----------|----------|------------|
| 🔴 Crítica | ${stats.critical} | ${((stats.critical/stats.total)*100).toFixed(1)}% |
| 🟠 Alta | ${stats.high} | ${((stats.high/stats.total)*100).toFixed(1)}% |
| 🟡 Media | ${stats.medium} | ${((stats.medium/stats.total)*100).toFixed(1)}% |
| 🟢 Baja | ${stats.low} | ${((stats.low/stats.total)*100).toFixed(1)}% |

---

## 🚨 Vulnerabilidades Críticas

${vulns.filter(v => v.severity === 'critical').map((v, i) => `
### ${i+1}. ${v.type}

**URL**: ${v.url}
**Fuente**: ${v.source}
**CWE ID**: ${v.cweid || 'N/A'}

**Descripción**:
${v.description}

**Solución Recomendada**:
${v.solution}

**Evidencia**:
\`\`\`
${v.evidence ? v.evidence.substring(0, 200) : 'N/A'}
\`\`\`

---
`).join('\n') || '*No se encontraron vulnerabilidades críticas.*'}

## ⚠️ Vulnerabilidades Altas

${vulns.filter(v => v.severity === 'high').slice(0, 5).map((v, i) => `
### ${i+1}. ${v.type}

**URL**: ${v.url}
**Descripción**: ${v.description.substring(0, 150)}...
**Solución**: ${v.solution.substring(0, 150)}...

---
`).join('\n') || '*No se encontraron vulnerabilidades altas.*'}

${vulns.filter(v => v.severity === 'high').length > 5 ? `*...y ${vulns.filter(v => v.severity === 'high').length - 5} vulnerabilidades altas adicionales.*` : ''}

## 📋 Recomendaciones por Categoría

${Object.entries(
  vulns.reduce((acc, v) => {
    acc[v.type] = (acc[v.type] || 0) + 1;
    return acc;
  }, {})
).sort((a, b) => b[1] - a[1]).slice(0, 10).map(([type, count]) =>
  `- **${type}**: ${count} ocurrencias`
).join('\n')}

## 🛡️ Plan de Remediación

1. **Prioridad Inmediata** (Críticas y Altas):
   - Inyecciones SQL: Implementar prepared statements
   - XSS: Implementar output encoding
   - CSRF: Agregar tokens anti-CSRF

2. **Corto Plazo** (Medias):
   - Configuraciones inseguras
   - Falta de headers de seguridad
   - Información sensible expuesta

3. **Largo Plazo** (Bajas):
   - Mejoras en la documentación de API
   - Optimización de mensajes de error

---

*Reporte generado automáticamente por sistema de fuzzing*
*Herramientas utilizadas: OWASP ZAP, SQLMap, ffuf*
`;

const fs = require('fs');
const reportPath = `/tmp/fuzzing_report_${Date.now()}.md`;
fs.writeFileSync(reportPath, report);

return [{
  json: {
    report: report,
    reportPath: reportPath,
    statistics: stats
  }
}];
```

## 📊 Base de Datos para Resultados

```sql
CREATE DATABASE fuzzing_results;

\c fuzzing_results

CREATE TABLE scans (
    id SERIAL PRIMARY KEY,
    target_url VARCHAR(500) NOT NULL,
    scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_vulnerabilities INTEGER,
    critical_count INTEGER,
    high_count INTEGER,
    medium_count INTEGER,
    low_count INTEGER,
    report_path VARCHAR(500)
);

CREATE TABLE vulnerabilities (
    id SERIAL PRIMARY KEY,
    scan_id INTEGER REFERENCES scans(id),
    source VARCHAR(50), -- ZAP, SQLMap, ffuf, etc.
    type VARCHAR(200),
    severity VARCHAR(20),
    url TEXT,
    description TEXT,
    solution TEXT,
    cweid INTEGER,
    evidence TEXT
);

CREATE INDEX idx_vulns_severity ON vulnerabilities(severity);
CREATE INDEX idx_vulns_type ON vulnerabilities(type);
```

## 📝 Ejercicios

### Ejercicio 1: Setup Básico (3 horas)
- Instalar DVWA y herramientas de fuzzing
- Configurar OWASP ZAP
- Ejecutar primer escaneo manual

### Ejercicio 2: Fuzzing Manual (4 horas)
- Identificar 5 vulnerabilidades en DVWA manualmente
- Documentar explotación paso a paso
- Proponer remediación

### Ejercicio 3: Automatización (6 horas)
- Implementar workflow completo en N8N
- Integrar múltiples herramientas
- Generar reportes automatizados

## 🏆 Criterios de Evaluación

| Criterio | Puntos |
|----------|--------|
| Configuración de herramientas | 20 |
| Identificación de vulnerabilidades | 30 |
| Workflow N8N funcional | 25 |
| Reportes y análisis | 15 |
| Propuestas de remediación | 10 |

---

**Autor**: Materia de Seguridad Ofensiva
**Última actualización**: 2025

# Reporte Consolidado de Seguridad
**Fecha de generación:** 2026-04-06 19:30:17

## Estadísticas Generales
- **Total de URLs únicas analizadas:** 16
- **URLs descubiertas por Spider:** 16
- **Alertas identificadas por ZAP:** 10
- **Rutas descubiertas por FFUF:** 2
- **Vulnerabilidades detectadas por SQLMap:** 0

## Detalles Técnicos: Alertas de ZAP
### Cross Site Scripting (Reflected)
- **Severidad:** High (Medium)
- **URL:** `http://target.com/search`
- **Método:** N/A
- **Descripción:** N/A
- **Solución:** <p>Phase: Architecture and Design. Use a vetted library or framework that does not allow this weakness to occur. Validate all input. Use Content-Security-Policy header.</p>

---
### Cross Site Scripting (Reflected)
- **Severidad:** High (Medium)
- **URL:** `http://target.com/feedback`
- **Método:** N/A
- **Descripción:** N/A
- **Solución:** <p>Phase: Architecture and Design. Use a vetted library or framework that does not allow this weakness to occur. Validate all input. Use Content-Security-Policy header.</p>

---
### SQL Injection
- **Severidad:** High (High)
- **URL:** `http://target.com/login`
- **Método:** N/A
- **Descripción:** N/A
- **Solución:** <p>Use parameterized queries (prepared statements) instead of string concatenation for SQL queries. Use stored procedures. Apply least privilege to the database account.</p>

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://target.com`
- **Método:** N/A
- **Descripción:** N/A
- **Solución:** <p>Modern Web browsers support the Content-Security-Policy and X-Frame-Options HTTP headers. Set one of these on all web pages returned by your site/app.</p>

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://target.com/login`
- **Método:** N/A
- **Descripción:** N/A
- **Solución:** <p>Modern Web browsers support the Content-Security-Policy and X-Frame-Options HTTP headers. Set one of these on all web pages returned by your site/app.</p>

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://target.com/admin`
- **Método:** N/A
- **Descripción:** N/A
- **Solución:** <p>Modern Web browsers support the Content-Security-Policy and X-Frame-Options HTTP headers. Set one of these on all web pages returned by your site/app.</p>

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://target.com`
- **Método:** N/A
- **Descripción:** N/A
- **Solución:** <p>Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.</p>

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://target.com/login`
- **Método:** N/A
- **Descripción:** N/A
- **Solución:** <p>Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.</p>

---
### Server Leaks Version Information via 'Server' HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://target.com`
- **Método:** N/A
- **Descripción:** N/A
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to suppress the 'Server' header or provide generic details.</p>

---
### Modern Web Application
- **Severidad:** Informational (Medium)
- **URL:** `http://target.com`
- **Método:** N/A
- **Descripción:** N/A
- **Solución:** <p>This is an informational alert and so no changes are required.</p>

---
## Detalles Técnicos: Rutas Ocultas o Sensibles (FFUF)
### Directorio/Archivo Sensible o Expuesto
- **Severidad:** Low (Informational)
- **URL:** `http://target.com/admin`
- **Método:** GET
- **Descripción:** Archivo o directorio descubierto (HTTP Status: 200, Lines: N/A, Words: N/A)
- **Solución:** <p>Verifique si este recurso debe ser público. Si contiene información confidencial, configure controles de acceso o retírelo del servidor.</p>

---
### Directorio/Archivo Sensible o Expuesto
- **Severidad:** Low (Informational)
- **URL:** `http://target.com/login`
- **Método:** GET
- **Descripción:** Archivo o directorio descubierto (HTTP Status: 200, Lines: N/A, Words: N/A)
- **Solución:** <p>Verifique si este recurso debe ser público. Si contiene información confidencial, configure controles de acceso o retírelo del servidor.</p>

---

## Mapa del Sitio (Spider)
<details><summary>Ver lista completa de URLs descubiertas</summary>

<ul>
<li><code>http://target.com</code></li>
<li><code>http://target.com/login</code></li>
<li><code>http://target.com/admin</code></li>
<li><code>http://target.com/admin/dashboard</code></li>
<li><code>http://target.com/api</code></li>
<li><code>http://target.com/api/</code></li>
<li><code>http://target.com/api/users</code></li>
<li><code>http://target.com/search</code></li>
<li><code>http://target.com/search?q=test</code></li>
<li><code>http://target.com/feedback</code></li>
<li><code>http://target.com/assets/main.js</code></li>
<li><code>http://target.com/assets/style.css</code></li>
<li><code>http://target.com/robots.txt</code></li>
<li><code>http://target.com/sitemap.xml</code></li>
<li><code>http://target.com/contact</code></li>
<li><code>http://target.com/about</code></li>
</ul>
</details>
# Reporte Consolidado de Seguridad
**Fecha de generación:** 2026-04-29 02:22:28

## Estadísticas Generales
- **Total de URLs únicas analizadas:** 13
- **URLs descubiertas por Spider:** 8
- **Alertas identificadas por ZAP:** 24
- **Rutas descubiertas por FFUF:** 0
- **Vulnerabilidades detectadas por SQLMap:** 0

## Detalles Técnicos: Alertas de ZAP
### Content Security Policy (CSP) Header Not Set
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/login.php`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to set the Content-Security-Policy header.</p>

---
### Content Security Policy (CSP) Header Not Set
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/sitemap.xml`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to set the Content-Security-Policy header.</p>

---
### Directory Browsing
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/dvwa/`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Disable directory browsing. If this is required, make sure the listed files does not induce risks.</p>

---
### Directory Browsing
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/dvwa/css/`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Disable directory browsing. If this is required, make sure the listed files does not induce risks.</p>

---
### Directory Browsing
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/dvwa/images/`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Disable directory browsing. If this is required, make sure the listed files does not induce risks.</p>

---
### HTTP Only Site
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Configure your web or application server to use SSL (https).</p>

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/login.php`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Modern Web browsers support the Content-Security-Policy and X-Frame-Options HTTP headers. Ensure one of them is set on all web pages returned by your site/app.</p><p>If you expect the page to be framed only by pages on your server (e.g. it's part of a FRAMESET) then you'll want to use SAMEORIGIN, otherwise if you never expect the page to be framed, you should use DENY. Alternatively consider implementing Content Security Policy's "frame-ancestors" directive.</p>

---
### In Page Banner Information Leak
- **Severidad:** Low (High)
- **URL:** `http://dvwa/sitemap.xml`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Configure the server to prevent such information leaks. For example:</p><p>Under Tomcat this is done via the "server" directive and implementation of custom error pages.</p><p>Under Apache this is done via the "ServerSignature" and "ServerTokens" directives.</p>

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to suppress the "Server" header or provide generic details.</p>

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa/dvwa/css/login.css`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to suppress the "Server" header or provide generic details.</p>

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa/dvwa/images/login_logo.png`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to suppress the "Server" header or provide generic details.</p>

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa/robots.txt`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to suppress the "Server" header or provide generic details.</p>

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa/sitemap.xml`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to suppress the "Server" header or provide generic details.</p>

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/dvwa/css/login.css`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.</p><p>If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.</p>

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/dvwa/images/RandomStorm.png`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.</p><p>If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.</p>

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/dvwa/images/login_logo.png`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.</p><p>If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.</p>

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/login.php`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.</p><p>If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.</p>

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/robots.txt`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** <p>Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.</p><p>If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.</p>

---
### Authentication Request Identified
- **Severidad:** Informational (High)
- **URL:** `http://dvwa/login.php`
- **Método:** POST
- **Descripción:** N/A
- **Solución:** <p>This is an informational alert rather than a vulnerability and so there is nothing to fix.</p>

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** 

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** 

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/dvwa`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** 

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/dvwa/css`
- **Método:** GET
- **Descripción:** N/A
- **Solución:** 

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/login.php`
- **Método:** POST
- **Descripción:** N/A
- **Solución:** 

---

## Mapa del Sitio (Spider)
<details><summary>Ver lista completa de URLs descubiertas</summary>

<ul>
<li><code>http://dvwa/dvwa/images/RandomStorm.png</code></li>
<li><code>http://dvwa</code></li>
<li><code>http://dvwa/login.php</code></li>
<li><code>http://dvwa/dvwa/css/login.css</code></li>
<li><code>http://dvwa/robots.txt</code></li>
<li><code>http://dvwa/</code></li>
<li><code>http://dvwa/sitemap.xml</code></li>
<li><code>http://dvwa/dvwa/images/login_logo.png</code></li>
</ul>
</details>
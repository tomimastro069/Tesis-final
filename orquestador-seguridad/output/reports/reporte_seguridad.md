# Reporte Consolidado de Seguridad
**Fecha de generación:** 2026-04-28 20:52:22

## Estadísticas Generales
- **Total de URLs únicas analizadas:** 56
- **URLs descubiertas por Spider:** 55
- **Alertas identificadas por ZAP:** 0
- **Rutas descubiertas por FFUF:** 9
- **Vulnerabilidades detectadas por SQLMap:** 0

## Detalles Técnicos: Rutas Ocultas o Sensibles (FFUF)
### Directorio/Archivo Sensible o Expuesto
- **Severidad:** Low (Informational)
- **URL:** `http://dvwa/login.php`
- **Método:** GET
- **Descripción:** Archivo o directorio descubierto (HTTP Status: 200, Lines: N/A, Words: N/A)
- **Solución:** <p>Verifique si este recurso debe ser público. Si contiene información confidencial, configure controles de acceso o retírelo del servidor.</p>

---
### Directorio/Archivo Sensible o Expuesto
- **Severidad:** Low (Informational)
- **URL:** `http://dvwa/security.php`
- **Método:** GET
- **Descripción:** Archivo o directorio descubierto (HTTP Status: 302, Lines: N/A, Words: N/A)
- **Solución:** <p>Verifique si este recurso debe ser público. Si contiene información confidencial, configure controles de acceso o retírelo del servidor.</p>

---
### Directorio/Archivo Sensible o Expuesto
- **Severidad:** Low (Informational)
- **URL:** `http://dvwa/`
- **Método:** GET
- **Descripción:** Archivo o directorio descubierto (HTTP Status: 302, Lines: N/A, Words: N/A)
- **Solución:** <p>Verifique si este recurso debe ser público. Si contiene información confidencial, configure controles de acceso o retírelo del servidor.</p>

---
### Directorio/Archivo Sensible o Expuesto
- **Severidad:** Low (Informational)
- **URL:** `http://dvwa/about.php`
- **Método:** GET
- **Descripción:** Archivo o directorio descubierto (HTTP Status: 200, Lines: N/A, Words: N/A)
- **Solución:** <p>Verifique si este recurso debe ser público. Si contiene información confidencial, configure controles de acceso o retírelo del servidor.</p>

---
### Directorio/Archivo Sensible o Expuesto
- **Severidad:** Low (Informational)
- **URL:** `http://dvwa/logout.php`
- **Método:** GET
- **Descripción:** Archivo o directorio descubierto (HTTP Status: 302, Lines: N/A, Words: N/A)
- **Solución:** <p>Verifique si este recurso debe ser público. Si contiene información confidencial, configure controles de acceso o retírelo del servidor.</p>

---
### Directorio/Archivo Sensible o Expuesto
- **Severidad:** Low (Informational)
- **URL:** `http://dvwa/index.php`
- **Método:** GET
- **Descripción:** Archivo o directorio descubierto (HTTP Status: 302, Lines: N/A, Words: N/A)
- **Solución:** <p>Verifique si este recurso debe ser público. Si contiene información confidencial, configure controles de acceso o retírelo del servidor.</p>

---
### Directorio/Archivo Sensible o Expuesto
- **Severidad:** Low (Informational)
- **URL:** `http://dvwa/setup.php`
- **Método:** GET
- **Descripción:** Archivo o directorio descubierto (HTTP Status: 200, Lines: N/A, Words: N/A)
- **Solución:** <p>Verifique si este recurso debe ser público. Si contiene información confidencial, configure controles de acceso o retírelo del servidor.</p>

---
### Directorio/Archivo Sensible o Expuesto
- **Severidad:** Low (Informational)
- **URL:** `http://dvwa/instructions.php`
- **Método:** GET
- **Descripción:** Archivo o directorio descubierto (HTTP Status: 200, Lines: N/A, Words: N/A)
- **Solución:** <p>Verifique si este recurso debe ser público. Si contiene información confidencial, configure controles de acceso o retírelo del servidor.</p>

---
### Directorio/Archivo Sensible o Expuesto
- **Severidad:** Low (Informational)
- **URL:** `http://dvwa/phpinfo.php`
- **Método:** GET
- **Descripción:** Archivo o directorio descubierto (HTTP Status: 302, Lines: N/A, Words: N/A)
- **Solución:** <p>Verifique si este recurso debe ser público. Si contiene información confidencial, configure controles de acceso o retírelo del servidor.</p>

---

## Mapa del Sitio (Spider)
<details><summary>Ver lista completa de URLs descubiertas</summary>

<ul>
<li><code>http://dvwa/vulnerabilities/xss_r/</code></li>
<li><code>http://dvwa/dvwa/images/spanner.png</code></li>
<li><code>http://dvwa/vulnerabilities/fi/?page=file2.php</code></li>
<li><code>http://dvwa/vulnerabilities/javascript/</code></li>
<li><code>http://dvwa/instructions.php?doc=readme</code></li>
<li><code>http://dvwa/instructions.php?doc=PHPIDS-license</code></li>
<li><code>http://dvwa/vulnerabilities/weak_id/</code></li>
<li><code>http://dvwa/vulnerabilities/sqli_blind/</code></li>
<li><code>http://dvwa/vulnerabilities/sqli/?Submit=Submit&id=ZAP</code></li>
<li><code>http://dvwa/docs/DVWA_v1.3.pdf</code></li>
<li><code>http://dvwa/instructions.php</code></li>
<li><code>http://dvwa/vulnerabilities/fi/?page=file1.php</code></li>
<li><code>http://dvwa/dvwa/js/dvwaPage.js</code></li>
<li><code>http://dvwa/vulnerabilities/exec/</code></li>
<li><code>http://dvwa/dvwa/images/login_logo.png</code></li>
<li><code>http://dvwa/vulnerabilities/upload/</code></li>
<li><code>http://dvwa/security.php?phpids=on</code></li>
<li><code>http://dvwa/vulnerabilities/xss_s/</code></li>
<li><code>http://dvwa/vulnerabilities/captcha/</code></li>
<li><code>http://dvwa/instructions.php?doc=changelog</code></li>
<li><code>http://dvwa/logout.php</code></li>
<li><code>http://dvwa</code></li>
<li><code>http://dvwa/vulnerabilities/xss_d/?default</code></li>
<li><code>http://dvwa/</code></li>
<li><code>http://dvwa/vulnerabilities/fi/?page=include.php</code></li>
<li><code>http://dvwa/setup.php</code></li>
<li><code>http://dvwa/vulnerabilities/xss_r/?name=ZAP</code></li>
<li><code>http://dvwa/vulnerabilities/csrf/?Change=Change&password_conf=ZAP&password_new=ZAP</code></li>
<li><code>http://dvwa/favicon.ico</code></li>
<li><code>http://dvwa/dvwa/js/add_event_listeners.js</code></li>
<li><code>http://dvwa/phpinfo.php</code></li>
<li><code>http://dvwa/dvwa/images/logo.png</code></li>
<li><code>http://dvwa/login.php</code></li>
<li><code>http://dvwa/instructions.php?doc=copying</code></li>
<li><code>http://dvwa/about.php</code></li>
<li><code>http://dvwa/sitemap.xml</code></li>
<li><code>http://dvwa/ids_log.php</code></li>
<li><code>http://dvwa/var/www/html/config/config.inc.php</code></li>
<li><code>http://dvwa/vulnerabilities/sqli/</code></li>
<li><code>http://dvwa/instructions.php?doc=PDF</code></li>
<li><code>http://dvwa/dvwa/images/RandomStorm.png</code></li>
<li><code>http://dvwa/security.php</code></li>
<li><code>http://dvwa/vulnerabilities/csrf/</code></li>
<li><code>http://dvwa/DTD/xhtml1-transitional.dtd</code></li>
<li><code>http://dvwa/vulnerabilities/brute/</code></li>
<li><code>http://dvwa/security.php?test=%2522%3E%3Cscript%3Eeval(window.name)%3C/script%3E</code></li>
<li><code>http://dvwa/vulnerabilities/xss_d/</code></li>
<li><code>http://dvwa/vulnerabilities/csp/</code></li>
<li><code>http://dvwa/dvwa/css/main.css</code></li>
<li><code>http://dvwa/vulnerabilities/fi/?page=file3.php</code></li>
<li><code>http://dvwa/vulnerabilities/brute/?Login=Login&password=ZAP&username=ZAP</code></li>
<li><code>http://dvwa/dvwa/css/login.css</code></li>
<li><code>http://dvwa/dvwa/images/lock.png</code></li>
<li><code>http://dvwa/robots.txt</code></li>
<li><code>http://dvwa/vulnerabilities/sqli_blind/?Submit=Submit&id=ZAP</code></li>
</ul>
</details>
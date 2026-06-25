# Reporte Consolidado de Seguridad
**Fecha de generación:** 2026-06-25 00:21:44

## Estadísticas Generales
- **Total de URLs únicas analizadas:** 10
- **URLs descubiertas por Spider:** 8
- **Alertas identificadas por ZAP:** 19
- **Rutas descubiertas por FFUF:** 1
- **Vulnerabilidades detectadas por SQLMap:** 0

## Detalles Técnicos: Alertas de ZAP
### Content Security Policy (CSP) Header Not Set
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/login.php`
- **Método:** GET
- **Descripción:** <p>Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross Site Scripting (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.</p>
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to set the Content-Security-Policy header.</p>

---
### Content Security Policy (CSP) Header Not Set
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/sitemap.xml`
- **Método:** GET
- **Descripción:** <p>Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross Site Scripting (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.</p>
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to set the Content-Security-Policy header.</p>

---
### HTTP Only Site
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/vulnerabilities/exec/`
- **Método:** GET
- **Descripción:** <p>The site is only served under HTTP and not HTTPS.</p>
- **Solución:** <p>Configure your web or application server to use SSL (https).</p>

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/login.php`
- **Método:** GET
- **Descripción:** <p>The response does not protect against 'ClickJacking' attacks. It should include either Content-Security-Policy with 'frame-ancestors' directive or X-Frame-Options.</p>
- **Solución:** <p>Modern Web browsers support the Content-Security-Policy and X-Frame-Options HTTP headers. Ensure one of them is set on all web pages returned by your site/app.</p><p>If you expect the page to be framed only by pages on your server (e.g. it's part of a FRAMESET) then you'll want to use SAMEORIGIN, otherwise if you never expect the page to be framed, you should use DENY. Alternatively consider implementing Content Security Policy's "frame-ancestors" directive.</p>

---
### In Page Banner Information Leak
- **Severidad:** Low (High)
- **URL:** `http://dvwa/sitemap.xml`
- **Método:** GET
- **Descripción:** <p>The server returned a version banner string in the response content. Such information leaks may allow attackers to further target specific issues impacting the product and version in use.</p>
- **Solución:** <p>Configure the server to prevent such information leaks. For example:</p><p>Under Tomcat this is done via the "server" directive and implementation of custom error pages.</p><p>Under Apache this is done via the "ServerSignature" and "ServerTokens" directives.</p>

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa/`
- **Método:** GET
- **Descripción:** <p>The web/application server is leaking version information via the "Server" HTTP response header. Access to such information may facilitate attackers identifying other vulnerabilities your web/application server is subject to.</p>
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to suppress the "Server" header or provide generic details.</p>

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa/dvwa/css/login.css`
- **Método:** GET
- **Descripción:** <p>The web/application server is leaking version information via the "Server" HTTP response header. Access to such information may facilitate attackers identifying other vulnerabilities your web/application server is subject to.</p>
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to suppress the "Server" header or provide generic details.</p>

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa/robots.txt`
- **Método:** GET
- **Descripción:** <p>The web/application server is leaking version information via the "Server" HTTP response header. Access to such information may facilitate attackers identifying other vulnerabilities your web/application server is subject to.</p>
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to suppress the "Server" header or provide generic details.</p>

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa/sitemap.xml`
- **Método:** GET
- **Descripción:** <p>The web/application server is leaking version information via the "Server" HTTP response header. Access to such information may facilitate attackers identifying other vulnerabilities your web/application server is subject to.</p>
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to suppress the "Server" header or provide generic details.</p>

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa/vulnerabilities/exec/`
- **Método:** GET
- **Descripción:** <p>The web/application server is leaking version information via the "Server" HTTP response header. Access to such information may facilitate attackers identifying other vulnerabilities your web/application server is subject to.</p>
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to suppress the "Server" header or provide generic details.</p>

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/dvwa/css/login.css`
- **Método:** GET
- **Descripción:** <p>The Anti-MIME-Sniffing header X-Content-Type-Options was not set to 'nosniff'. This allows older versions of Internet Explorer and Chrome to perform MIME-sniffing on the response body, potentially causing the response body to be interpreted and displayed as a content type other than the declared content type. Current (early 2014) and legacy versions of Firefox will use the declared content type (if one is set), rather than performing MIME-sniffing.</p>
- **Solución:** <p>Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.</p><p>If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.</p>

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/dvwa/images/RandomStorm.png`
- **Método:** GET
- **Descripción:** <p>The Anti-MIME-Sniffing header X-Content-Type-Options was not set to 'nosniff'. This allows older versions of Internet Explorer and Chrome to perform MIME-sniffing on the response body, potentially causing the response body to be interpreted and displayed as a content type other than the declared content type. Current (early 2014) and legacy versions of Firefox will use the declared content type (if one is set), rather than performing MIME-sniffing.</p>
- **Solución:** <p>Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.</p><p>If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.</p>

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/dvwa/images/login_logo.png`
- **Método:** GET
- **Descripción:** <p>The Anti-MIME-Sniffing header X-Content-Type-Options was not set to 'nosniff'. This allows older versions of Internet Explorer and Chrome to perform MIME-sniffing on the response body, potentially causing the response body to be interpreted and displayed as a content type other than the declared content type. Current (early 2014) and legacy versions of Firefox will use the declared content type (if one is set), rather than performing MIME-sniffing.</p>
- **Solución:** <p>Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.</p><p>If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.</p>

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/login.php`
- **Método:** GET
- **Descripción:** <p>The Anti-MIME-Sniffing header X-Content-Type-Options was not set to 'nosniff'. This allows older versions of Internet Explorer and Chrome to perform MIME-sniffing on the response body, potentially causing the response body to be interpreted and displayed as a content type other than the declared content type. Current (early 2014) and legacy versions of Firefox will use the declared content type (if one is set), rather than performing MIME-sniffing.</p>
- **Solución:** <p>Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.</p><p>If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.</p>

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/robots.txt`
- **Método:** GET
- **Descripción:** <p>The Anti-MIME-Sniffing header X-Content-Type-Options was not set to 'nosniff'. This allows older versions of Internet Explorer and Chrome to perform MIME-sniffing on the response body, potentially causing the response body to be interpreted and displayed as a content type other than the declared content type. Current (early 2014) and legacy versions of Firefox will use the declared content type (if one is set), rather than performing MIME-sniffing.</p>
- **Solución:** <p>Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.</p><p>If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.</p>

---
### Authentication Request Identified
- **Severidad:** Informational (High)
- **URL:** `http://dvwa/login.php`
- **Método:** POST
- **Descripción:** <p>The given request has been identified as an authentication request. The 'Other Info' field contains a set of key=value lines which identify any relevant fields. If the request is in a context which has an Authentication Method set to "Auto-Detect" then this rule will change the authentication to match the request identified.</p>
- **Solución:** <p>This is an informational alert rather than a vulnerability and so there is nothing to fix.</p>

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/vulnerabilities/exec`
- **Método:** GET
- **Descripción:** <p>Check for differences in response based on fuzzed User Agent (eg. mobile sites, access as a Search Engine Crawler). Compares the response statuscode and the hashcode of the response body with the original response.</p>
- **Solución:** 

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/vulnerabilities/exec/`
- **Método:** GET
- **Descripción:** <p>Check for differences in response based on fuzzed User Agent (eg. mobile sites, access as a Search Engine Crawler). Compares the response statuscode and the hashcode of the response body with the original response.</p>
- **Solución:** 

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/vulnerabilities/exec/index.php`
- **Método:** GET
- **Descripción:** <p>Check for differences in response based on fuzzed User Agent (eg. mobile sites, access as a Search Engine Crawler). Compares the response statuscode and the hashcode of the response body with the original response.</p>
- **Solución:** 

---
## Detalles Técnicos: Rutas Ocultas o Sensibles (FFUF)
### Directorio/Archivo Sensible o Expuesto
- **Severidad:** Low (Informational)
- **URL:** `http://dvwa/vulnerabilities/exec/index.php`
- **Método:** GET
- **Descripción:** Archivo o directorio descubierto (HTTP Status: 302, Lines: N/A, Words: N/A)
- **Solución:** <p>Verifique si este recurso debe ser público. Si contiene información confidencial, configure controles de acceso o retírelo del servidor.</p>

---

## Mapa del Sitio (Spider)
<details><summary>Ver lista completa de URLs descubiertas</summary>

<ul>
<li><code>http://dvwa/login.php</code></li>
<li><code>http://dvwa/vulnerabilities/exec/</code></li>
<li><code>http://dvwa/dvwa/images/login_logo.png</code></li>
<li><code>http://dvwa/dvwa/images/RandomStorm.png</code></li>
<li><code>http://dvwa/sitemap.xml</code></li>
<li><code>http://dvwa/</code></li>
<li><code>http://dvwa/dvwa/css/login.css</code></li>
<li><code>http://dvwa/robots.txt</code></li>
</ul>
</details>
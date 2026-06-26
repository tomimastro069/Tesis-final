# Reporte Consolidado de Seguridad
**Fecha de generación:** 2026-06-25 23:31:26

## Estadísticas Generales
- **Total de URLs únicas analizadas:** 35
- **URLs descubiertas por Spider:** 24
- **Alertas identificadas por ZAP:** 37
- **Rutas descubiertas por FFUF:** 8
- **Vulnerabilidades detectadas por SQLMap:** 8

## Detalles Técnicos: Alertas de ZAP
### Content Security Policy (CSP) Header Not Set
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/about.php`
- **Método:** GET
- **Descripción:** <p>Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross Site Scripting (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.</p>
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to set the Content-Security-Policy header.</p>

---
### Content Security Policy (CSP) Header Not Set
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/instructions.php`
- **Método:** GET
- **Descripción:** <p>Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross Site Scripting (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.</p>
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to set the Content-Security-Policy header.</p>

---
### Content Security Policy (CSP) Header Not Set
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/login.php`
- **Método:** GET
- **Descripción:** <p>Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross Site Scripting (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.</p>
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to set the Content-Security-Policy header.</p>

---
### Content Security Policy (CSP) Header Not Set
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/setup.php`
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
### Directory Browsing
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/docs/`
- **Método:** GET
- **Descripción:** <p>It is possible to view the directory listing. Directory listing may reveal hidden scripts, include files, backup source files, etc. which can be accessed to read sensitive information.</p>
- **Solución:** <p>Disable directory browsing. If this is required, make sure the listed files does not induce risks.</p>

---
### Directory Browsing
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/dvwa/`
- **Método:** GET
- **Descripción:** <p>It is possible to view the directory listing. Directory listing may reveal hidden scripts, include files, backup source files, etc. which can be accessed to read sensitive information.</p>
- **Solución:** <p>Disable directory browsing. If this is required, make sure the listed files does not induce risks.</p>

---
### Directory Browsing
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/dvwa/css/`
- **Método:** GET
- **Descripción:** <p>It is possible to view the directory listing. Directory listing may reveal hidden scripts, include files, backup source files, etc. which can be accessed to read sensitive information.</p>
- **Solución:** <p>Disable directory browsing. If this is required, make sure the listed files does not induce risks.</p>

---
### Directory Browsing
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/dvwa/images/`
- **Método:** GET
- **Descripción:** <p>It is possible to view the directory listing. Directory listing may reveal hidden scripts, include files, backup source files, etc. which can be accessed to read sensitive information.</p>
- **Solución:** <p>Disable directory browsing. If this is required, make sure the listed files does not induce risks.</p>

---
### Directory Browsing
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/dvwa/js/`
- **Método:** GET
- **Descripción:** <p>It is possible to view the directory listing. Directory listing may reveal hidden scripts, include files, backup source files, etc. which can be accessed to read sensitive information.</p>
- **Solución:** <p>Disable directory browsing. If this is required, make sure the listed files does not induce risks.</p>

---
### HTTP Only Site
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/`
- **Método:** GET
- **Descripción:** <p>The site is only served under HTTP and not HTTPS.</p>
- **Solución:** <p>Configure your web or application server to use SSL (https).</p>

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/about.php`
- **Método:** GET
- **Descripción:** <p>The response does not protect against 'ClickJacking' attacks. It should include either Content-Security-Policy with 'frame-ancestors' directive or X-Frame-Options.</p>
- **Solución:** <p>Modern Web browsers support the Content-Security-Policy and X-Frame-Options HTTP headers. Ensure one of them is set on all web pages returned by your site/app.</p><p>If you expect the page to be framed only by pages on your server (e.g. it's part of a FRAMESET) then you'll want to use SAMEORIGIN, otherwise if you never expect the page to be framed, you should use DENY. Alternatively consider implementing Content Security Policy's "frame-ancestors" directive.</p>

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/instructions.php`
- **Método:** GET
- **Descripción:** <p>The response does not protect against 'ClickJacking' attacks. It should include either Content-Security-Policy with 'frame-ancestors' directive or X-Frame-Options.</p>
- **Solución:** <p>Modern Web browsers support the Content-Security-Policy and X-Frame-Options HTTP headers. Ensure one of them is set on all web pages returned by your site/app.</p><p>If you expect the page to be framed only by pages on your server (e.g. it's part of a FRAMESET) then you'll want to use SAMEORIGIN, otherwise if you never expect the page to be framed, you should use DENY. Alternatively consider implementing Content Security Policy's "frame-ancestors" directive.</p>

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/instructions.php?doc=readme`
- **Método:** GET
- **Descripción:** <p>The response does not protect against 'ClickJacking' attacks. It should include either Content-Security-Policy with 'frame-ancestors' directive or X-Frame-Options.</p>
- **Solución:** <p>Modern Web browsers support the Content-Security-Policy and X-Frame-Options HTTP headers. Ensure one of them is set on all web pages returned by your site/app.</p><p>If you expect the page to be framed only by pages on your server (e.g. it's part of a FRAMESET) then you'll want to use SAMEORIGIN, otherwise if you never expect the page to be framed, you should use DENY. Alternatively consider implementing Content Security Policy's "frame-ancestors" directive.</p>

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/login.php`
- **Método:** GET
- **Descripción:** <p>The response does not protect against 'ClickJacking' attacks. It should include either Content-Security-Policy with 'frame-ancestors' directive or X-Frame-Options.</p>
- **Solución:** <p>Modern Web browsers support the Content-Security-Policy and X-Frame-Options HTTP headers. Ensure one of them is set on all web pages returned by your site/app.</p><p>If you expect the page to be framed only by pages on your server (e.g. it's part of a FRAMESET) then you'll want to use SAMEORIGIN, otherwise if you never expect the page to be framed, you should use DENY. Alternatively consider implementing Content Security Policy's "frame-ancestors" directive.</p>

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/setup.php`
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
### In Page Banner Information Leak
- **Severidad:** Low (High)
- **URL:** `http://dvwa/var/www/html/config/config.inc.php`
- **Método:** GET
- **Descripción:** <p>The server returned a version banner string in the response content. Such information leaks may allow attackers to further target specific issues impacting the product and version in use.</p>
- **Solución:** <p>Configure the server to prevent such information leaks. For example:</p><p>Under Tomcat this is done via the "server" directive and implementation of custom error pages.</p><p>Under Apache this is done via the "ServerSignature" and "ServerTokens" directives.</p>

---
### Information Disclosure - Debug Error Messages
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/instructions.php`
- **Método:** GET
- **Descripción:** <p>The response appeared to contain common error messages returned by platforms such as ASP.NET, and Web-servers such as IIS and Apache. You can configure the list of common debug messages.</p>
- **Solución:** <p>Disable debugging messages before pushing to production.</p>

---
### Information Disclosure - Debug Error Messages
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/instructions.php?doc=readme`
- **Método:** GET
- **Descripción:** <p>The response appeared to contain common error messages returned by platforms such as ASP.NET, and Web-servers such as IIS and Apache. You can configure the list of common debug messages.</p>
- **Solución:** <p>Disable debugging messages before pushing to production.</p>

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa`
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
- **URL:** `http://dvwa/login.php`
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
### Information Disclosure - Suspicious Comments
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/setup.php`
- **Método:** GET
- **Descripción:** <p>The response appears to contain suspicious comments which may help an attacker.</p>
- **Solución:** <p>Remove all comments that return information that may help an attacker and fix any underlying problems they refer to.</p>

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa`
- **Método:** GET
- **Descripción:** <p>Check for differences in response based on fuzzed User Agent (eg. mobile sites, access as a Search Engine Crawler). Compares the response statuscode and the hashcode of the response body with the original response.</p>
- **Solución:** 

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/`
- **Método:** GET
- **Descripción:** <p>Check for differences in response based on fuzzed User Agent (eg. mobile sites, access as a Search Engine Crawler). Compares the response statuscode and the hashcode of the response body with the original response.</p>
- **Solución:** 

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/about.php`
- **Método:** GET
- **Descripción:** <p>Check for differences in response based on fuzzed User Agent (eg. mobile sites, access as a Search Engine Crawler). Compares the response statuscode and the hashcode of the response body with the original response.</p>
- **Solución:** 

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/login.php`
- **Método:** POST
- **Descripción:** <p>Check for differences in response based on fuzzed User Agent (eg. mobile sites, access as a Search Engine Crawler). Compares the response statuscode and the hashcode of the response body with the original response.</p>
- **Solución:** 

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/setup.php`
- **Método:** POST
- **Descripción:** <p>Check for differences in response based on fuzzed User Agent (eg. mobile sites, access as a Search Engine Crawler). Compares the response statuscode and the hashcode of the response body with the original response.</p>
- **Solución:** 

---
## Detalles Técnicos: Rutas Ocultas o Sensibles (FFUF)
### Directorio/Archivo Sensible o Expuesto
- **Severidad:** Low (Informational)
- **URL:** `http://dvwa/about.php`
- **Método:** GET
- **Descripción:** Archivo o directorio descubierto (HTTP Status: 200, Lines: N/A, Words: N/A)
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
- **URL:** `http://dvwa/instructions.php`
- **Método:** GET
- **Descripción:** Archivo o directorio descubierto (HTTP Status: 200, Lines: N/A, Words: N/A)
- **Solución:** <p>Verifique si este recurso debe ser público. Si contiene información confidencial, configure controles de acceso o retírelo del servidor.</p>

---
### Directorio/Archivo Sensible o Expuesto
- **Severidad:** Low (Informational)
- **URL:** `http://dvwa/login.php`
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
- **URL:** `http://dvwa/phpinfo.php`
- **Método:** GET
- **Descripción:** Archivo o directorio descubierto (HTTP Status: 302, Lines: N/A, Words: N/A)
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
- **URL:** `http://dvwa/setup.php`
- **Método:** GET
- **Descripción:** Archivo o directorio descubierto (HTTP Status: 200, Lines: N/A, Words: N/A)
- **Solución:** <p>Verifique si este recurso debe ser público. Si contiene información confidencial, configure controles de acceso o retírelo del servidor.</p>

---

## Detalles Técnicos: Inyecciones SQL (SQLMap)
### SQL Injection (MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause)
- **Severidad:** High (High)
- **URL:** `http://dvwa/vulnerabilities/brute/?Login=Login&password=ZAP&username=ZAP`
- **Método:** N/A
- **Descripción:** Inyección en parámetro `username` mediante un payload tipo `boolean-based blind`: `username=OGvY' RLIKE (SELECT (CASE WHEN (6678=6678) THEN 0x4f477659 ELSE 0x28 END))-- gGwh&password=sdeo&Login=Login`

#### Información Extraída (Data Dump)
```text
Volcado de Tabla: dvwa.users (5 registros)

+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+
| user_id | user    | avatar                      | password                         | last_name | first_name | last_login          | failed_login |
+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+

+------------+--------+-------------------------+
| comment_id | name   | comment                 |
+------------+--------+-------------------------+
```

- **Solución:** <p>Use parameterized queries (prepared statements) instead of string concatenation for SQL queries. Use stored procedures. Apply least privilege to the database account.</p>

---
### SQL Injection (MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE))
- **Severidad:** High (High)
- **URL:** `http://dvwa/vulnerabilities/brute/?Login=Login&password=ZAP&username=ZAP`
- **Método:** N/A
- **Descripción:** Inyección en parámetro `username` mediante un payload tipo `error-based`: `username=OGvY' AND EXTRACTVALUE(2382,CONCAT(0x5c,0x71766b6a71,(SELECT (ELT(2382=2382,1))),0x71706b7a71))-- WJum&password=sdeo&Login=Login`

#### Información Extraída (Data Dump)
```text
Volcado de Tabla: dvwa.users (5 registros)

+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+
| user_id | user    | avatar                      | password                         | last_name | first_name | last_login          | failed_login |
+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+

+------------+--------+-------------------------+
| comment_id | name   | comment                 |
+------------+--------+-------------------------+
```

- **Solución:** <p>Use parameterized queries (prepared statements) instead of string concatenation for SQL queries. Use stored procedures. Apply least privilege to the database account.</p>

---
### SQL Injection (MySQL >= 5.0.12 AND time-based blind (query SLEEP))
- **Severidad:** High (High)
- **URL:** `http://dvwa/vulnerabilities/brute/?Login=Login&password=ZAP&username=ZAP`
- **Método:** N/A
- **Descripción:** Inyección en parámetro `username` mediante un payload tipo `time-based blind`: `username=OGvY' AND (SELECT 8355 FROM (SELECT(SLEEP(5)))polt)-- BvZr&password=sdeo&Login=Login`

#### Información Extraída (Data Dump)
```text
Volcado de Tabla: dvwa.users (5 registros)

+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+
| user_id | user    | avatar                      | password                         | last_name | first_name | last_login          | failed_login |
+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+

+------------+--------+-------------------------+
| comment_id | name   | comment                 |
+------------+--------+-------------------------+
```

- **Solución:** <p>Use parameterized queries (prepared statements) instead of string concatenation for SQL queries. Use stored procedures. Apply least privilege to the database account.</p>

---
### SQL Injection (MySQL UNION query (NULL) - 8 columns)
- **Severidad:** High (High)
- **URL:** `http://dvwa/vulnerabilities/brute/?Login=Login&password=ZAP&username=ZAP`
- **Método:** N/A
- **Descripción:** Inyección en parámetro `username` mediante un payload tipo `UNION query`: `username=OGvY' UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,CONCAT(0x71766b6a71,0x666b656642434d4d437743754d5767787449636d49615054646c5650584b50586f646c5979544753,0x71706b7a71),NULL,NULL#&password=sdeo&Login=Login`

#### Información Extraída (Data Dump)
```text
Volcado de Tabla: dvwa.users (5 registros)

+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+
| user_id | user    | avatar                      | password                         | last_name | first_name | last_login          | failed_login |
+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+

+------------+--------+-------------------------+
| comment_id | name   | comment                 |
+------------+--------+-------------------------+
```

- **Solución:** <p>Use parameterized queries (prepared statements) instead of string concatenation for SQL queries. Use stored procedures. Apply least privilege to the database account.</p>

---
### SQL Injection (OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment))
- **Severidad:** High (High)
- **URL:** `http://dvwa/vulnerabilities/sqli/?Submit=Submit&id=ZAP`
- **Método:** N/A
- **Descripción:** Inyección en parámetro `id` mediante un payload tipo `boolean-based blind`: `id=9749' OR NOT 6958=6958#&Submit=Submit`

#### Información Extraída (Data Dump)
```text
Volcado de Tabla: dvwa.users (5 registros)

+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+
| user_id | user    | avatar                      | password                         | last_name | first_name | last_login          | failed_login |
+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+

+------------+--------+-------------------------+
| comment_id | name   | comment                 |
+------------+--------+-------------------------+
```

- **Solución:** <p>Use parameterized queries (prepared statements) instead of string concatenation for SQL queries. Use stored procedures. Apply least privilege to the database account.</p>

---
### SQL Injection (MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE))
- **Severidad:** High (High)
- **URL:** `http://dvwa/vulnerabilities/sqli/?Submit=Submit&id=ZAP`
- **Método:** N/A
- **Descripción:** Inyección en parámetro `id` mediante un payload tipo `error-based`: `id=9749' AND EXTRACTVALUE(9177,CONCAT(0x5c,0x7176626271,(SELECT (ELT(9177=9177,1))),0x71767a6a71))-- cySU&Submit=Submit`

#### Información Extraída (Data Dump)
```text
Volcado de Tabla: dvwa.users (5 registros)

+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+
| user_id | user    | avatar                      | password                         | last_name | first_name | last_login          | failed_login |
+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+

+------------+--------+-------------------------+
| comment_id | name   | comment                 |
+------------+--------+-------------------------+
```

- **Solución:** <p>Use parameterized queries (prepared statements) instead of string concatenation for SQL queries. Use stored procedures. Apply least privilege to the database account.</p>

---
### SQL Injection (MySQL >= 5.0.12 AND time-based blind (query SLEEP))
- **Severidad:** High (High)
- **URL:** `http://dvwa/vulnerabilities/sqli/?Submit=Submit&id=ZAP`
- **Método:** N/A
- **Descripción:** Inyección en parámetro `id` mediante un payload tipo `time-based blind`: `id=9749' AND (SELECT 1994 FROM (SELECT(SLEEP(5)))XmoK)-- hdrj&Submit=Submit`

#### Información Extraída (Data Dump)
```text
Volcado de Tabla: dvwa.users (5 registros)

+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+
| user_id | user    | avatar                      | password                         | last_name | first_name | last_login          | failed_login |
+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+

+------------+--------+-------------------------+
| comment_id | name   | comment                 |
+------------+--------+-------------------------+
```

- **Solución:** <p>Use parameterized queries (prepared statements) instead of string concatenation for SQL queries. Use stored procedures. Apply least privilege to the database account.</p>

---
### SQL Injection (MySQL UNION query (NULL) - 2 columns)
- **Severidad:** High (High)
- **URL:** `http://dvwa/vulnerabilities/sqli/?Submit=Submit&id=ZAP`
- **Método:** N/A
- **Descripción:** Inyección en parámetro `id` mediante un payload tipo `UNION query`: `id=9749' UNION ALL SELECT CONCAT(0x7176626271,0x7079574a514345724e706463796944457170797a5057466868546f547676774e655a4b6e6d66716d,0x71767a6a71),NULL#&Submit=Submit`

#### Información Extraída (Data Dump)
```text
Volcado de Tabla: dvwa.users (5 registros)

+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+
| user_id | user    | avatar                      | password                         | last_name | first_name | last_login          | failed_login |
+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+

+------------+--------+-------------------------+
| comment_id | name   | comment                 |
+------------+--------+-------------------------+
```

- **Solución:** <p>Use parameterized queries (prepared statements) instead of string concatenation for SQL queries. Use stored procedures. Apply least privilege to the database account.</p>

---

## Mapa del Sitio (Spider)
<details><summary>Ver lista completa de URLs descubiertas</summary>

<ul>
<li><code>http://dvwa/favicon.ico</code></li>
<li><code>http://dvwa/dvwa/js/add_event_listeners.js</code></li>
<li><code>http://dvwa/dvwa/images/spanner.png</code></li>
<li><code>http://dvwa/instructions.php?doc=readme</code></li>
<li><code>http://dvwa/instructions.php?doc=PHPIDS-license</code></li>
<li><code>http://dvwa/instructions.php?doc=PDF</code></li>
<li><code>http://dvwa/instructions.php?doc=changelog</code></li>
<li><code>http://dvwa/dvwa/images/RandomStorm.png</code></li>
<li><code>http://dvwa/dvwa/images/logo.png</code></li>
<li><code>http://dvwa/docs/DVWA_v1.3.pdf</code></li>
<li><code>http://dvwa/instructions.php</code></li>
<li><code>http://dvwa/dvwa/js/dvwaPage.js</code></li>
<li><code>http://dvwa/login.php</code></li>
<li><code>http://dvwa/instructions.php?doc=copying</code></li>
<li><code>http://dvwa/dvwa/images/login_logo.png</code></li>
<li><code>http://dvwa</code></li>
<li><code>http://dvwa/about.php</code></li>
<li><code>http://dvwa/dvwa/css/main.css</code></li>
<li><code>http://dvwa/sitemap.xml</code></li>
<li><code>http://dvwa/</code></li>
<li><code>http://dvwa/dvwa/css/login.css</code></li>
<li><code>http://dvwa/robots.txt</code></li>
<li><code>http://dvwa/setup.php</code></li>
<li><code>http://dvwa/var/www/html/config/config.inc.php</code></li>
</ul>
</details>
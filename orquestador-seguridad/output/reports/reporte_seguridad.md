# Reporte Consolidado de Seguridad
**Fecha de generación:** 2026-06-23 21:44:04

## Estadísticas Generales
- **Total de URLs únicas analizadas:** 59
- **URLs descubiertas por Spider:** 53
- **Alertas identificadas por ZAP:** 56
- **Rutas descubiertas por FFUF:** 8
- **Vulnerabilidades detectadas por SQLMap:** 0

## Detalles Técnicos: Alertas de ZAP
### Absence of Anti-CSRF Tokens
- **Severidad:** Medium (Low)
- **URL:** `http://dvwa/vulnerabilities/captcha/`
- **Método:** GET
- **Descripción:** <p>No Anti-CSRF tokens were found in a HTML submission form.</p><p>A cross-site request forgery is an attack that involves forcing a victim to send an HTTP request to a target destination without their knowledge or intent in order to perform an action as the victim. The underlying cause is application functionality using predictable URL/form actions in a repeatable way. The nature of the attack is that CSRF exploits the trust that a web site has for a user. By contrast, cross-site scripting (XSS) exploits the trust that a user has for a web site. Like XSS, CSRF attacks are not necessarily cross-site, but they can be. Cross-site request forgery is also known as CSRF, XSRF, one-click attack, session riding, confused deputy, and sea surf.</p><p></p><p>CSRF attacks are effective in a number of situations, including:</p><p>    * The victim has an active session on the target site.</p><p>    * The victim is authenticated via HTTP auth on the target site.</p><p>    * The victim is on the same local network as the target site.</p><p></p><p>CSRF has primarily been used to perform an action against a target site using the victim's privileges, but recent techniques have been discovered to disclose information by gaining access to the response. The risk of information disclosure is dramatically increased when the target site is vulnerable to XSS, because XSS can be used as a platform for CSRF, allowing the attack to operate within the bounds of the same-origin policy.</p>
- **Solución:** <p>Phase: Architecture and Design</p><p>Use a vetted library or framework that does not allow this weakness to occur or provides constructs that make this weakness easier to avoid.</p><p>For example, use anti-CSRF packages such as the OWASP CSRFGuard.</p><p></p><p>Phase: Implementation</p><p>Ensure that your application is free of cross-site scripting issues, because most CSRF defenses can be bypassed using attacker-controlled script.</p><p></p><p>Phase: Architecture and Design</p><p>Generate a unique nonce for each form, place the nonce into the form, and verify the nonce upon receipt of the form. Be sure that the nonce is not predictable (CWE-330).</p><p>Note that this can be bypassed using XSS.</p><p></p><p>Identify especially dangerous operations. When the user performs a dangerous operation, send a separate confirmation request to ensure that the user intended to perform that operation.</p><p>Note that this can be bypassed using XSS.</p><p></p><p>Use the ESAPI Session Management control.</p><p>This control includes a component for CSRF.</p><p></p><p>Do not use the GET method for any request that triggers a state change.</p><p></p><p>Phase: Implementation</p><p>Check the HTTP Referer header to see if the request originated from an expected page. This could break legitimate functionality, because users or proxies may have disabled sending the Referer for privacy reasons.</p>

---
### Absence of Anti-CSRF Tokens
- **Severidad:** Medium (Low)
- **URL:** `http://dvwa/vulnerabilities/exec/`
- **Método:** GET
- **Descripción:** <p>No Anti-CSRF tokens were found in a HTML submission form.</p><p>A cross-site request forgery is an attack that involves forcing a victim to send an HTTP request to a target destination without their knowledge or intent in order to perform an action as the victim. The underlying cause is application functionality using predictable URL/form actions in a repeatable way. The nature of the attack is that CSRF exploits the trust that a web site has for a user. By contrast, cross-site scripting (XSS) exploits the trust that a user has for a web site. Like XSS, CSRF attacks are not necessarily cross-site, but they can be. Cross-site request forgery is also known as CSRF, XSRF, one-click attack, session riding, confused deputy, and sea surf.</p><p></p><p>CSRF attacks are effective in a number of situations, including:</p><p>    * The victim has an active session on the target site.</p><p>    * The victim is authenticated via HTTP auth on the target site.</p><p>    * The victim is on the same local network as the target site.</p><p></p><p>CSRF has primarily been used to perform an action against a target site using the victim's privileges, but recent techniques have been discovered to disclose information by gaining access to the response. The risk of information disclosure is dramatically increased when the target site is vulnerable to XSS, because XSS can be used as a platform for CSRF, allowing the attack to operate within the bounds of the same-origin policy.</p>
- **Solución:** <p>Phase: Architecture and Design</p><p>Use a vetted library or framework that does not allow this weakness to occur or provides constructs that make this weakness easier to avoid.</p><p>For example, use anti-CSRF packages such as the OWASP CSRFGuard.</p><p></p><p>Phase: Implementation</p><p>Ensure that your application is free of cross-site scripting issues, because most CSRF defenses can be bypassed using attacker-controlled script.</p><p></p><p>Phase: Architecture and Design</p><p>Generate a unique nonce for each form, place the nonce into the form, and verify the nonce upon receipt of the form. Be sure that the nonce is not predictable (CWE-330).</p><p>Note that this can be bypassed using XSS.</p><p></p><p>Identify especially dangerous operations. When the user performs a dangerous operation, send a separate confirmation request to ensure that the user intended to perform that operation.</p><p>Note that this can be bypassed using XSS.</p><p></p><p>Use the ESAPI Session Management control.</p><p>This control includes a component for CSRF.</p><p></p><p>Do not use the GET method for any request that triggers a state change.</p><p></p><p>Phase: Implementation</p><p>Check the HTTP Referer header to see if the request originated from an expected page. This could break legitimate functionality, because users or proxies may have disabled sending the Referer for privacy reasons.</p>

---
### Absence of Anti-CSRF Tokens
- **Severidad:** Medium (Low)
- **URL:** `http://dvwa/vulnerabilities/upload/`
- **Método:** GET
- **Descripción:** <p>No Anti-CSRF tokens were found in a HTML submission form.</p><p>A cross-site request forgery is an attack that involves forcing a victim to send an HTTP request to a target destination without their knowledge or intent in order to perform an action as the victim. The underlying cause is application functionality using predictable URL/form actions in a repeatable way. The nature of the attack is that CSRF exploits the trust that a web site has for a user. By contrast, cross-site scripting (XSS) exploits the trust that a user has for a web site. Like XSS, CSRF attacks are not necessarily cross-site, but they can be. Cross-site request forgery is also known as CSRF, XSRF, one-click attack, session riding, confused deputy, and sea surf.</p><p></p><p>CSRF attacks are effective in a number of situations, including:</p><p>    * The victim has an active session on the target site.</p><p>    * The victim is authenticated via HTTP auth on the target site.</p><p>    * The victim is on the same local network as the target site.</p><p></p><p>CSRF has primarily been used to perform an action against a target site using the victim's privileges, but recent techniques have been discovered to disclose information by gaining access to the response. The risk of information disclosure is dramatically increased when the target site is vulnerable to XSS, because XSS can be used as a platform for CSRF, allowing the attack to operate within the bounds of the same-origin policy.</p>
- **Solución:** <p>Phase: Architecture and Design</p><p>Use a vetted library or framework that does not allow this weakness to occur or provides constructs that make this weakness easier to avoid.</p><p>For example, use anti-CSRF packages such as the OWASP CSRFGuard.</p><p></p><p>Phase: Implementation</p><p>Ensure that your application is free of cross-site scripting issues, because most CSRF defenses can be bypassed using attacker-controlled script.</p><p></p><p>Phase: Architecture and Design</p><p>Generate a unique nonce for each form, place the nonce into the form, and verify the nonce upon receipt of the form. Be sure that the nonce is not predictable (CWE-330).</p><p>Note that this can be bypassed using XSS.</p><p></p><p>Identify especially dangerous operations. When the user performs a dangerous operation, send a separate confirmation request to ensure that the user intended to perform that operation.</p><p>Note that this can be bypassed using XSS.</p><p></p><p>Use the ESAPI Session Management control.</p><p>This control includes a component for CSRF.</p><p></p><p>Do not use the GET method for any request that triggers a state change.</p><p></p><p>Phase: Implementation</p><p>Check the HTTP Referer header to see if the request originated from an expected page. This could break legitimate functionality, because users or proxies may have disabled sending the Referer for privacy reasons.</p>

---
### Absence of Anti-CSRF Tokens
- **Severidad:** Medium (Low)
- **URL:** `http://dvwa/vulnerabilities/weak_id/`
- **Método:** GET
- **Descripción:** <p>No Anti-CSRF tokens were found in a HTML submission form.</p><p>A cross-site request forgery is an attack that involves forcing a victim to send an HTTP request to a target destination without their knowledge or intent in order to perform an action as the victim. The underlying cause is application functionality using predictable URL/form actions in a repeatable way. The nature of the attack is that CSRF exploits the trust that a web site has for a user. By contrast, cross-site scripting (XSS) exploits the trust that a user has for a web site. Like XSS, CSRF attacks are not necessarily cross-site, but they can be. Cross-site request forgery is also known as CSRF, XSRF, one-click attack, session riding, confused deputy, and sea surf.</p><p></p><p>CSRF attacks are effective in a number of situations, including:</p><p>    * The victim has an active session on the target site.</p><p>    * The victim is authenticated via HTTP auth on the target site.</p><p>    * The victim is on the same local network as the target site.</p><p></p><p>CSRF has primarily been used to perform an action against a target site using the victim's privileges, but recent techniques have been discovered to disclose information by gaining access to the response. The risk of information disclosure is dramatically increased when the target site is vulnerable to XSS, because XSS can be used as a platform for CSRF, allowing the attack to operate within the bounds of the same-origin policy.</p>
- **Solución:** <p>Phase: Architecture and Design</p><p>Use a vetted library or framework that does not allow this weakness to occur or provides constructs that make this weakness easier to avoid.</p><p>For example, use anti-CSRF packages such as the OWASP CSRFGuard.</p><p></p><p>Phase: Implementation</p><p>Ensure that your application is free of cross-site scripting issues, because most CSRF defenses can be bypassed using attacker-controlled script.</p><p></p><p>Phase: Architecture and Design</p><p>Generate a unique nonce for each form, place the nonce into the form, and verify the nonce upon receipt of the form. Be sure that the nonce is not predictable (CWE-330).</p><p>Note that this can be bypassed using XSS.</p><p></p><p>Identify especially dangerous operations. When the user performs a dangerous operation, send a separate confirmation request to ensure that the user intended to perform that operation.</p><p>Note that this can be bypassed using XSS.</p><p></p><p>Use the ESAPI Session Management control.</p><p>This control includes a component for CSRF.</p><p></p><p>Do not use the GET method for any request that triggers a state change.</p><p></p><p>Phase: Implementation</p><p>Check the HTTP Referer header to see if the request originated from an expected page. This could break legitimate functionality, because users or proxies may have disabled sending the Referer for privacy reasons.</p>

---
### Absence of Anti-CSRF Tokens
- **Severidad:** Medium (Low)
- **URL:** `http://dvwa/vulnerabilities/xss_s/`
- **Método:** GET
- **Descripción:** <p>No Anti-CSRF tokens were found in a HTML submission form.</p><p>A cross-site request forgery is an attack that involves forcing a victim to send an HTTP request to a target destination without their knowledge or intent in order to perform an action as the victim. The underlying cause is application functionality using predictable URL/form actions in a repeatable way. The nature of the attack is that CSRF exploits the trust that a web site has for a user. By contrast, cross-site scripting (XSS) exploits the trust that a user has for a web site. Like XSS, CSRF attacks are not necessarily cross-site, but they can be. Cross-site request forgery is also known as CSRF, XSRF, one-click attack, session riding, confused deputy, and sea surf.</p><p></p><p>CSRF attacks are effective in a number of situations, including:</p><p>    * The victim has an active session on the target site.</p><p>    * The victim is authenticated via HTTP auth on the target site.</p><p>    * The victim is on the same local network as the target site.</p><p></p><p>CSRF has primarily been used to perform an action against a target site using the victim's privileges, but recent techniques have been discovered to disclose information by gaining access to the response. The risk of information disclosure is dramatically increased when the target site is vulnerable to XSS, because XSS can be used as a platform for CSRF, allowing the attack to operate within the bounds of the same-origin policy.</p>
- **Solución:** <p>Phase: Architecture and Design</p><p>Use a vetted library or framework that does not allow this weakness to occur or provides constructs that make this weakness easier to avoid.</p><p>For example, use anti-CSRF packages such as the OWASP CSRFGuard.</p><p></p><p>Phase: Implementation</p><p>Ensure that your application is free of cross-site scripting issues, because most CSRF defenses can be bypassed using attacker-controlled script.</p><p></p><p>Phase: Architecture and Design</p><p>Generate a unique nonce for each form, place the nonce into the form, and verify the nonce upon receipt of the form. Be sure that the nonce is not predictable (CWE-330).</p><p>Note that this can be bypassed using XSS.</p><p></p><p>Identify especially dangerous operations. When the user performs a dangerous operation, send a separate confirmation request to ensure that the user intended to perform that operation.</p><p>Note that this can be bypassed using XSS.</p><p></p><p>Use the ESAPI Session Management control.</p><p>This control includes a component for CSRF.</p><p></p><p>Do not use the GET method for any request that triggers a state change.</p><p></p><p>Phase: Implementation</p><p>Check the HTTP Referer header to see if the request originated from an expected page. This could break legitimate functionality, because users or proxies may have disabled sending the Referer for privacy reasons.</p>

---
### CSP: Failure to Define Directive with No Fallback
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/vulnerabilities/csp/`
- **Método:** GET
- **Descripción:** <p>The Content Security Policy fails to define one of the directives that has no fallback. Missing/excluding them is the same as allowing anything.</p>
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is properly configured to set the Content-Security-Policy header.</p>

---
### CSP: Wildcard Directive
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/vulnerabilities/csp/`
- **Método:** GET
- **Descripción:** <p>Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks. Including (but not limited to) Cross Site Scripting (XSS), and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.</p>
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is properly configured to set the Content-Security-Policy header.</p>

---
### CSP: style-src unsafe-inline
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/vulnerabilities/csp/`
- **Método:** GET
- **Descripción:** <p>Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks. Including (but not limited to) Cross Site Scripting (XSS), and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.</p>
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is properly configured to set the Content-Security-Policy header.</p>

---
### Content Security Policy (CSP) Header Not Set
- **Severidad:** Medium (High)
- **URL:** `http://dvwa`
- **Método:** GET
- **Descripción:** <p>Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross Site Scripting (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.</p>
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to set the Content-Security-Policy header.</p>

---
### Content Security Policy (CSP) Header Not Set
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/`
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
- **URL:** `http://dvwa/sitemap.xml`
- **Método:** GET
- **Descripción:** <p>Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross Site Scripting (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.</p>
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to set the Content-Security-Policy header.</p>

---
### Content Security Policy (CSP) Header Not Set
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/vulnerabilities/brute/`
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
- **URL:** `http://dvwa/vulnerabilities/xss_s/`
- **Método:** GET
- **Descripción:** <p>The site is only served under HTTP and not HTTPS.</p>
- **Solución:** <p>Configure your web or application server to use SSL (https).</p>

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa`
- **Método:** GET
- **Descripción:** <p>The response does not protect against 'ClickJacking' attacks. It should include either Content-Security-Policy with 'frame-ancestors' directive or X-Frame-Options.</p>
- **Solución:** <p>Modern Web browsers support the Content-Security-Policy and X-Frame-Options HTTP headers. Ensure one of them is set on all web pages returned by your site/app.</p><p>If you expect the page to be framed only by pages on your server (e.g. it's part of a FRAMESET) then you'll want to use SAMEORIGIN, otherwise if you never expect the page to be framed, you should use DENY. Alternatively consider implementing Content Security Policy's "frame-ancestors" directive.</p>

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/`
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
- **URL:** `http://dvwa/vulnerabilities/brute/`
- **Método:** GET
- **Descripción:** <p>The response does not protect against 'ClickJacking' attacks. It should include either Content-Security-Policy with 'frame-ancestors' directive or X-Frame-Options.</p>
- **Solución:** <p>Modern Web browsers support the Content-Security-Policy and X-Frame-Options HTTP headers. Ensure one of them is set on all web pages returned by your site/app.</p><p>If you expect the page to be framed only by pages on your server (e.g. it's part of a FRAMESET) then you'll want to use SAMEORIGIN, otherwise if you never expect the page to be framed, you should use DENY. Alternatively consider implementing Content Security Policy's "frame-ancestors" directive.</p>

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/vulnerabilities/exec/`
- **Método:** GET
- **Descripción:** <p>The response does not protect against 'ClickJacking' attacks. It should include either Content-Security-Policy with 'frame-ancestors' directive or X-Frame-Options.</p>
- **Solución:** <p>Modern Web browsers support the Content-Security-Policy and X-Frame-Options HTTP headers. Ensure one of them is set on all web pages returned by your site/app.</p><p>If you expect the page to be framed only by pages on your server (e.g. it's part of a FRAMESET) then you'll want to use SAMEORIGIN, otherwise if you never expect the page to be framed, you should use DENY. Alternatively consider implementing Content Security Policy's "frame-ancestors" directive.</p>

---
### Sub Resource Integrity Attribute Missing
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/vulnerabilities/captcha/`
- **Método:** GET
- **Descripción:** <p>The integrity attribute is missing on a script or link tag served by an external server. The integrity tag prevents an attacker who have gained access to this server from injecting a malicious content.</p>
- **Solución:** <p>Provide a valid integrity attribute to the tag.</p>

---
### Cross-Domain JavaScript Source File Inclusion
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/vulnerabilities/captcha/`
- **Método:** GET
- **Descripción:** <p>The page includes one or more script files from a third-party domain.</p>
- **Solución:** <p>Ensure JavaScript source files are loaded from only trusted sources, and the sources can't be controlled by end users of the application.</p>

---
### In Page Banner Information Leak
- **Severidad:** Low (High)
- **URL:** `http://dvwa/DTD/xhtml1-transitional.dtd`
- **Método:** GET
- **Descripción:** <p>The server returned a version banner string in the response content. Such information leaks may allow attackers to further target specific issues impacting the product and version in use.</p>
- **Solución:** <p>Configure the server to prevent such information leaks. For example:</p><p>Under Tomcat this is done via the "server" directive and implementation of custom error pages.</p><p>Under Apache this is done via the "ServerSignature" and "ServerTokens" directives.</p>

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
### Private IP Disclosure
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/phpinfo.php`
- **Método:** GET
- **Descripción:** <p>A private IP (such as 10.x.x.x, 172.x.x.x, 192.168.x.x) or an Amazon EC2 private hostname (for example, ip-10-0-56-78) has been found in the HTTP response body. This information might be helpful for further attacks targeting internal systems.</p>
- **Solución:** <p>Remove the private IP address from the HTTP response body. For comments, use JSP/ASP/PHP comment instead of HTML/JavaScript comment which can be seen by client browsers.</p>

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
- **URL:** `http://dvwa/`
- **Método:** GET
- **Descripción:** <p>The web/application server is leaking version information via the "Server" HTTP response header. Access to such information may facilitate attackers identifying other vulnerabilities your web/application server is subject to.</p>
- **Solución:** <p>Ensure that your web server, application server, load balancer, etc. is configured to suppress the "Server" header or provide generic details.</p>

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa/instructions.php`
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
### Timestamp Disclosure - Unix
- **Severidad:** Low (Low)
- **URL:** `http://dvwa/phpinfo.php`
- **Método:** GET
- **Descripción:** <p>A timestamp was disclosed by the application/web server. - Unix</p>
- **Solución:** <p>Manually confirm that the timestamp data is not sensitive, and that the data cannot be aggregated to disclose exploitable patterns.</p>

---
### Timestamp Disclosure - Unix
- **Severidad:** Low (Low)
- **URL:** `http://dvwa/vulnerabilities/javascript/`
- **Método:** GET
- **Descripción:** <p>A timestamp was disclosed by the application/web server. - Unix</p>
- **Solución:** <p>Manually confirm that the timestamp data is not sensitive, and that the data cannot be aggregated to disclose exploitable patterns.</p>

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa`
- **Método:** GET
- **Descripción:** <p>The Anti-MIME-Sniffing header X-Content-Type-Options was not set to 'nosniff'. This allows older versions of Internet Explorer and Chrome to perform MIME-sniffing on the response body, potentially causing the response body to be interpreted and displayed as a content type other than the declared content type. Current (early 2014) and legacy versions of Firefox will use the declared content type (if one is set), rather than performing MIME-sniffing.</p>
- **Solución:** <p>Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.</p><p>If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.</p>

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/`
- **Método:** GET
- **Descripción:** <p>The Anti-MIME-Sniffing header X-Content-Type-Options was not set to 'nosniff'. This allows older versions of Internet Explorer and Chrome to perform MIME-sniffing on the response body, potentially causing the response body to be interpreted and displayed as a content type other than the declared content type. Current (early 2014) and legacy versions of Firefox will use the declared content type (if one is set), rather than performing MIME-sniffing.</p>
- **Solución:** <p>Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.</p><p>If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.</p>

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/instructions.php`
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
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/vulnerabilities/brute/`
- **Método:** GET
- **Descripción:** <p>The Anti-MIME-Sniffing header X-Content-Type-Options was not set to 'nosniff'. This allows older versions of Internet Explorer and Chrome to perform MIME-sniffing on the response body, potentially causing the response body to be interpreted and displayed as a content type other than the declared content type. Current (early 2014) and legacy versions of Firefox will use the declared content type (if one is set), rather than performing MIME-sniffing.</p>
- **Solución:** <p>Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.</p><p>If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.</p>

---
### Authentication Request Identified
- **Severidad:** Informational (High)
- **URL:** `http://dvwa/vulnerabilities/brute/?Login=Login&password=ZAP&username=ZAP`
- **Método:** GET
- **Descripción:** <p>The given request has been identified as an authentication request. The 'Other Info' field contains a set of key=value lines which identify any relevant fields. If the request is in a context which has an Authentication Method set to "Auto-Detect" then this rule will change the authentication to match the request identified.</p>
- **Solución:** <p>This is an informational alert rather than a vulnerability and so there is nothing to fix.</p>

---
### Authentication Request Identified
- **Severidad:** Informational (High)
- **URL:** `http://dvwa/login.php`
- **Método:** POST
- **Descripción:** <p>The given request has been identified as an authentication request. The 'Other Info' field contains a set of key=value lines which identify any relevant fields. If the request is in a context which has an Authentication Method set to "Auto-Detect" then this rule will change the authentication to match the request identified.</p>
- **Solución:** <p>This is an informational alert rather than a vulnerability and so there is nothing to fix.</p>

---
### Information Disclosure - Sensitive Information in URL
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/vulnerabilities/brute/?Login=Login&password=ZAP&username=ZAP`
- **Método:** GET
- **Descripción:** <p>The request appeared to contain sensitive information leaked in the URL. This can violate PCI and most organizational compliance policies. You can configure the list of strings for this check to add or remove values specific to your environment.</p>
- **Solución:** <p>Do not pass sensitive information in URIs.</p>

---
### Information Disclosure - Sensitive Information in URL
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/vulnerabilities/csrf/?Change=Change&password_conf=ZAP&password_new=ZAP`
- **Método:** GET
- **Descripción:** <p>The request appeared to contain sensitive information leaked in the URL. This can violate PCI and most organizational compliance policies. You can configure the list of strings for this check to add or remove values specific to your environment.</p>
- **Solución:** <p>Do not pass sensitive information in URIs.</p>

---
### Information Disclosure - Suspicious Comments
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/setup.php`
- **Método:** GET
- **Descripción:** <p>The response appears to contain suspicious comments which may help an attacker.</p>
- **Solución:** <p>Remove all comments that return information that may help an attacker and fix any underlying problems they refer to.</p>

---
### Information Disclosure - Suspicious Comments
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/vulnerabilities/javascript/`
- **Método:** GET
- **Descripción:** <p>The response appears to contain suspicious comments which may help an attacker.</p>
- **Solución:** <p>Remove all comments that return information that may help an attacker and fix any underlying problems they refer to.</p>

---
### Modern Web Application
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/phpinfo.php`
- **Método:** GET
- **Descripción:** <p>The application appears to be a modern web application. If you need to explore it automatically then the Ajax Spider may well be more effective than the standard one.</p>
- **Solución:** <p>This is an informational alert and so no changes are required.</p>

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/vulnerabilities/upload/`
- **Método:** GET
- **Descripción:** <p>Check for differences in response based on fuzzed User Agent (eg. mobile sites, access as a Search Engine Crawler). Compares the response statuscode and the hashcode of the response body with the original response.</p>
- **Solución:** 

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/vulnerabilities/xss_d/?default`
- **Método:** GET
- **Descripción:** <p>Check for differences in response based on fuzzed User Agent (eg. mobile sites, access as a Search Engine Crawler). Compares the response statuscode and the hashcode of the response body with the original response.</p>
- **Solución:** 

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/vulnerabilities/xss_r/`
- **Método:** GET
- **Descripción:** <p>Check for differences in response based on fuzzed User Agent (eg. mobile sites, access as a Search Engine Crawler). Compares the response statuscode and the hashcode of the response body with the original response.</p>
- **Solución:** 

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/vulnerabilities/xss_r/?name=ZAP`
- **Método:** GET
- **Descripción:** <p>Check for differences in response based on fuzzed User Agent (eg. mobile sites, access as a Search Engine Crawler). Compares the response statuscode and the hashcode of the response body with the original response.</p>
- **Solución:** 

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/vulnerabilities/xss_s/`
- **Método:** GET
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
<li><code>http://dvwa/docs/DVWA_v1.3.pdf</code></li>
<li><code>http://dvwa/instructions.php</code></li>
<li><code>http://dvwa/dvwa/js/dvwaPage.js</code></li>
<li><code>http://dvwa/vulnerabilities/fi/?page=file1.php</code></li>
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
<li><code>http://dvwa/vulnerabilities/brute/?Login=Login&password=ZAP&username=ZAP</code></li>
<li><code>http://dvwa/vulnerabilities/fi/?page=file3.php</code></li>
<li><code>http://dvwa/dvwa/css/login.css</code></li>
<li><code>http://dvwa/dvwa/images/lock.png</code></li>
<li><code>http://dvwa/robots.txt</code></li>
</ul>
</details>
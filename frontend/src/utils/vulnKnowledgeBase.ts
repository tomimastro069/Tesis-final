// Base de conocimiento en español para traducir/explicar los hallazgos que
// devuelven las herramientas de escaneo (OWASP ZAP, SQLMap). ZAP siempre
// devuelve sus alertas ("desc"/"solution") en inglés y con lenguaje muy
// técnico/legal, así que acá mapeamos cada tipo de hallazgo a una
// explicación clara: qué es, cuál es el peligro real y cómo mitigarlo.

export interface VulnKnowledge {
  queEs: string;
  peligroReal: string;
  comoMitigar: string;
}

const GENERIC_CONFIG: VulnKnowledge = {
  queEs: "Es una falla de configuración del servidor o de las cabeceras HTTP: el sitio no está aplicando alguna protección estándar que los navegadores modernos ofrecen.",
  peligroReal: "Por sí sola no permite robar datos directamente, pero reduce las defensas del sitio y facilita que un atacante combine esta falla con otra técnica (phishing, clickjacking, robo de sesión, etc.) para atacar a los usuarios.",
  comoMitigar: "Revisar la configuración del servidor web / aplicación y agregar la cabecera o ajuste de seguridad recomendado que falta.",
};

const GENERIC_INJECTION: VulnKnowledge = {
  queEs: "Es una falla de inyección: la aplicación toma un dato que envía el usuario (por URL, formulario, etc.) y lo usa sin validar dentro de una consulta o comando interno.",
  peligroReal: "Un atacante puede manipular ese dato para ejecutar acciones no previstas: leer o modificar información de la base de datos, eludir el login, o en casos graves tomar control del servidor.",
  comoMitigar: "Validar y sanitizar toda entrada del usuario, y usar consultas parametrizadas / preparadas en vez de concatenar texto.",
};

const EXACT: Record<string, VulnKnowledge> = {
  "Absence of Anti-CSRF Tokens": {
    queEs: "Los formularios del sitio no incluyen un token anti-CSRF (Cross-Site Request Forgery), que es un código secreto que confirma que el pedido realmente vino del usuario y no de otro sitio.",
    peligroReal: "Un atacante puede crear una página maliciosa que, al ser visitada por una víctima ya logueada, envíe pedidos ocultos al sitio real (por ejemplo cambiar su contraseña, borrar datos o transferir dinero) sin que la víctima se dé cuenta.",
    comoMitigar: "Agregar tokens CSRF únicos por sesión/formulario y validarlos en el servidor antes de procesar cualquier acción que modifique datos.",
  },
  "Authentication Request Identified": {
    queEs: "ZAP detectó automáticamente un endpoint que parece ser un formulario o pedido de login (usuario/contraseña).",
    peligroReal: "No es una vulnerabilidad en sí misma, es solo información: indica dónde está el punto de autenticación, lo cual sirve como mapa de ataque para probar fuerza bruta, credenciales por defecto o bypass de login sobre ese endpoint puntual.",
    comoMitigar: "Asegurarse de que ese endpoint tenga límite de intentos (rate limiting), captcha y bloqueo de cuenta tras varios fallos.",
  },
  "CSP: Failure to Define Directive with No Fallback": {
    queEs: "El sitio define una Content Security Policy (CSP), pero le faltan directivas clave (como default-src) que sirvan de respaldo para los tipos de contenido que no se configuraron explícitamente.",
    peligroReal: "Para esos tipos de contenido no cubiertos, el navegador no aplica ninguna restricción, dejando una puerta abierta para que un atacante inyecte scripts, estilos o recursos maliciosos (XSS) en esa parte no protegida.",
    comoMitigar: "Definir siempre una directiva default-src restrictiva como respaldo, y agregar explícitamente el resto de directivas (script-src, style-src, img-src, etc.).",
  },
  "CSP: Wildcard Directive": {
    queEs: "La política CSP usa un comodín (*) en alguna directiva, permitiendo cargar recursos (scripts, imágenes, estilos) desde cualquier dominio.",
    peligroReal: "Anula gran parte de la protección de la CSP: si un atacante logra inyectar una referencia a un script externo, el navegador lo va a cargar y ejecutar igual, porque el comodín lo permite desde cualquier origen.",
    comoMitigar: "Reemplazar el comodín por una lista blanca explícita de los dominios de confianza que realmente necesita el sitio.",
  },
  "CSP: style-src unsafe-inline": {
    queEs: "La política CSP permite estilos CSS \"inline\" (unsafe-inline), es decir, código de estilos escrito directamente dentro del HTML.",
    peligroReal: "Habilita ataques de inyección de CSS que pueden usarse para robar datos (leyendo campos ocultos con selectores CSS), hacer phishing visual dentro de la página, o encadenarse con otras fallas para exfiltrar información.",
    comoMitigar: "Mover los estilos a archivos .css externos y eliminar unsafe-inline de la directiva style-src, usando nonces o hashes si se necesita algún estilo puntual inline.",
  },
  "Content Security Policy (CSP) Header Not Set": {
    queEs: "El servidor no envía ninguna cabecera Content-Security-Policy. Esta cabecera le dice al navegador desde qué orígenes puede cargar scripts, imágenes, estilos, etc.",
    peligroReal: "Sin esta cabecera, el navegador no tiene ninguna restricción extra: si un atacante logra inyectar código (por ejemplo un ataque XSS), ese script se va a ejecutar sin obstáculos, pudiendo robar cookies de sesión, credenciales o redirigir al usuario a un sitio falso.",
    comoMitigar: "Configurar una cabecera Content-Security-Policy que restrinja explícitamente los orígenes permitidos para scripts, estilos, imágenes y otros recursos.",
  },
  "Cross Site Scripting (Reflected)": {
    queEs: "XSS Reflejado: la aplicación toma un dato que viene en la propia URL o en un parámetro del pedido y lo devuelve dentro del HTML de la página sin filtrarlo ni escaparlo.",
    peligroReal: "Es una de las vulnerabilidades más peligrosas: un atacante arma un link malicioso con código JavaScript incluido y se lo envía a la víctima (por email, WhatsApp, etc.). Al hacer clic, ese script se ejecuta en el navegador de la víctima con su sesión activa, pudiendo robar sus cookies/sesión, hacer capturas de lo que teclea, o realizar acciones en su nombre dentro del sitio.",
    comoMitigar: "Escapar/codificar (HTML-encode) todo dato del usuario antes de insertarlo en el HTML de respuesta, y validar el formato esperado de cada parámetro.",
  },
  "XSS": {
    queEs: "Cross-Site Scripting: la aplicación permite que un atacante inserte código JavaScript propio dentro de una página que luego ven otros usuarios.",
    peligroReal: "Ese script se ejecuta con los mismos privilegios que la página real dentro del navegador de la víctima, permitiendo robar su sesión, credenciales, o manipular el contenido que ve para engañarla (phishing).",
    comoMitigar: "Escapar toda entrada de usuario antes de mostrarla en el HTML y aplicar una Content-Security-Policy estricta como segunda capa de defensa.",
  },
  "Cross-Domain JavaScript Source File Inclusion": {
    queEs: "La página carga uno o más archivos JavaScript desde un dominio externo distinto al del sitio.",
    peligroReal: "El sitio queda dependiendo de la seguridad de ese tercero: si ese dominio externo es comprometido o el archivo es modificado, el script malicioso se ejecutaría directamente dentro de tu sitio con la confianza total del usuario (ataque de cadena de suministro).",
    comoMitigar: "Alojar los scripts críticos en el propio dominio cuando sea posible, o usar Subresource Integrity (SRI) para verificar que el archivo externo no fue alterado.",
  },
  "Directory Browsing": {
    queEs: "El servidor tiene habilitado el listado de contenido de carpetas: al entrar a una ruta sin un archivo índice, muestra todos los archivos que contiene en vez de dar un error.",
    peligroReal: "Expone la estructura interna del sitio y puede revelar archivos que no deberían ser públicos: backups, archivos de configuración, código fuente, credenciales, o versiones antiguas de páginas con otras vulnerabilidades.",
    comoMitigar: "Desactivar el listado de directorios en la configuración del servidor web (por ejemplo Options -Indexes en Apache) y restringir el acceso a archivos sensibles.",
  },
  "HTTP Only Site": {
    queEs: "El sitio (o parte de él) es accesible por HTTP sin cifrar, en vez de forzar siempre HTTPS.",
    peligroReal: "Toda la información viaja en texto plano por la red: cualquiera que intercepte el tráfico (en una red WiFi pública, por ejemplo) puede leer usuarios, contraseñas, cookies de sesión y datos personales, o incluso modificar el contenido de la página en tránsito.",
    comoMitigar: "Forzar HTTPS en todo el sitio, redirigiendo automáticamente el tráfico HTTP a HTTPS y usando la cabecera Strict-Transport-Security (HSTS).",
  },
  "In Page Banner Information Leak": {
    queEs: "La página muestra en su propio contenido (banners, pies de página, mensajes de error) información técnica como versiones de software, nombres de tecnologías o rutas internas.",
    peligroReal: "Le facilita el trabajo a un atacante: sabiendo la versión exacta del software usado, puede buscar directamente vulnerabilidades ya conocidas (CVEs) para esa versión en vez de tener que descubrirlas.",
    comoMitigar: "Quitar de las páginas y mensajes de error cualquier dato de versión, tecnología o información interna que no sea necesaria para el usuario final.",
  },
  "Information Disclosure - Debug Error Messages": {
    queEs: "Ante un error, la aplicación muestra mensajes de depuración (debug) completos: trazas de código, rutas del servidor, consultas SQL, nombres de variables, etc., en vez de un mensaje de error genérico.",
    peligroReal: "Estos mensajes revelan detalles internos de cómo está construida la aplicación (frameworks, estructura de base de datos, rutas de archivos), información que un atacante usa para planear ataques más precisos, como inyección SQL dirigida.",
    comoMitigar: "Desactivar el modo debug en producción y mostrar siempre mensajes de error genéricos al usuario, registrando el detalle técnico solo en logs internos del servidor.",
  },
  "Information Disclosure - Sensitive Information in URL": {
    queEs: "Datos sensibles (como tokens de sesión, contraseñas o información personal) viajan como parámetros visibles en la URL, en vez de enviarse de forma segura (por ejemplo en el cuerpo del pedido).",
    peligroReal: "Las URLs quedan guardadas en el historial del navegador, en los logs del servidor, en el proxy de la red, y se comparten fácilmente al copiar el link, lo que expone esos datos sensibles a cualquiera que acceda a esos registros.",
    comoMitigar: "Enviar los datos sensibles en el cuerpo del pedido (POST) en vez de en la URL, y usar HTTPS para cifrar el transporte.",
  },
  "Information Disclosure - Suspicious Comments": {
    queEs: "El código fuente HTML/JS que llega al navegador contiene comentarios sospechosos dejados por los desarrolladores (por ejemplo TODO, FIXME, credenciales de prueba, rutas internas o notas de debug).",
    peligroReal: "Cualquier persona puede ver el código fuente de la página desde el navegador y leer esos comentarios, que muchas veces revelan información interna, credenciales de prueba olvidadas o pistas sobre fallas conocidas del sistema.",
    comoMitigar: "Eliminar todo comentario de desarrollo antes de publicar en producción, idealmente automatizando esta limpieza en el proceso de build/deploy.",
  },
  "Missing Anti-clickjacking Header": {
    queEs: "Al sitio le falta la cabecera X-Frame-Options (o la directiva frame-ancestors en CSP), que evita que la página pueda cargarse dentro de un <iframe> en otro sitio.",
    peligroReal: "Permite un ataque de clickjacking: un atacante crea una página propia que carga tu sitio en un iframe invisible superpuesto sobre botones falsos. La víctima cree que hace clic en el contenido del atacante, pero en realidad está haciendo clic en tu sitio real (por ejemplo, confirmando una acción sensible sin saberlo).",
    comoMitigar: "Agregar la cabecera X-Frame-Options: DENY (o SAMEORIGIN si hace falta) y/o la directiva frame-ancestors en la CSP.",
  },
  "Modern Web Application": {
    queEs: "ZAP identificó que el sitio está construido como una aplicación web moderna (SPA, mucho JavaScript del lado del cliente, APIs, etc.).",
    peligroReal: "No es una vulnerabilidad, es solo una nota informativa sobre la tecnología del sitio, útil para orientar qué tipo de pruebas de seguridad aplicar (por ejemplo revisar más a fondo las APIs que consume el frontend).",
    comoMitigar: "No requiere corrección. Sirve como contexto para priorizar otras pruebas (seguridad de APIs, autenticación en el cliente, manejo de tokens).",
  },
  "SQL Injection": {
    queEs: "Inyección SQL: un parámetro que envía el usuario (por URL, formulario, cookie, etc.) se inserta directamente dentro de una consulta a la base de datos sin ser validado ni tratado como dato seguro.",
    peligroReal: "Es una de las vulnerabilidades más críticas que existen. Un atacante puede modificar la consulta para leer toda la base de datos (usuarios, contraseñas, datos personales, tarjetas), modificar o borrar información, saltarse el login sin credenciales, o en algunos casos ejecutar comandos en el servidor.",
    comoMitigar: "Usar siempre consultas parametrizadas / prepared statements (nunca concatenar texto del usuario en el SQL), y aplicar el principio de mínimo privilegio en el usuario de base de datos.",
  },
  "Server Leaks Version Information via 'Server' HTTP Response Header Field": {
    queEs: "El servidor responde con una cabecera \"Server\" que indica el software y la versión exacta que está corriendo (por ejemplo Apache/2.4.41).",
    peligroReal: "Un atacante puede buscar directamente vulnerabilidades públicas conocidas (CVEs) para esa versión específica, ahorrándose el trabajo de descubrirlas y apuntando el ataque con mucha más precisión.",
    comoMitigar: "Configurar el servidor para ocultar o generalizar la cabecera Server (sin exponer la versión exacta del software).",
  },
  "Sub Resource Integrity Attribute Missing": {
    queEs: "El sitio carga recursos externos (scripts o estilos de un CDN, por ejemplo) sin el atributo integrity, que permite verificar que el archivo no fue modificado.",
    peligroReal: "Si el proveedor externo (CDN) es comprometido o el archivo es alterado en tránsito, el navegador lo va a ejecutar igual sin ninguna advertencia, permitiendo inyectar código malicioso directamente en tu sitio.",
    comoMitigar: "Agregar el atributo integrity (hash SHA) y crossorigin a los tags <script>/<link> que cargan recursos externos.",
  },
  "Timestamp Disclosure - Unix": {
    queEs: "En alguna respuesta del servidor aparece un timestamp en formato Unix (un número que representa una fecha/hora interna del sistema).",
    peligroReal: "Es un riesgo bajo por sí solo, pero suma información al atacante sobre el funcionamiento interno del sistema (por ejemplo, fechas de creación de archivos o registros), que puede combinarse con otros datos para perfilar mejor un ataque.",
    comoMitigar: "Evitar exponer timestamps internos en las respuestas públicas de la API o del sitio si no son necesarios para el usuario.",
  },
  "User Agent Fuzzer": {
    queEs: "ZAP probó enviar distintos valores de cabecera User-Agent (navegador, bot, dispositivo falso) para ver si la aplicación se comporta distinto o revela algo según el User-Agent recibido.",
    peligroReal: "Por sí sola es una prueba informativa. El riesgo real depende de lo que haya encontrado: si la aplicación confía ciegamente en el User-Agent para tomar decisiones de seguridad (por ejemplo, saltarse validaciones para 'bots'), eso sí sería explotable.",
    comoMitigar: "No tomar decisiones de seguridad basadas en la cabecera User-Agent, ya que el atacante puede modificarla libremente.",
  },
  "X-Content-Type-Options Header Missing": {
    queEs: "Al sitio le falta la cabecera X-Content-Type-Options: nosniff, que le indica al navegador que respete estrictamente el tipo de contenido (Content-Type) declarado por el servidor.",
    peligroReal: "Sin esta cabecera, algunos navegadores intentan 'adivinar' el tipo de archivo (MIME sniffing). Un atacante puede aprovechar esto para que un archivo subido como imagen o texto sea interpretado y ejecutado como JavaScript, habilitando ataques XSS.",
    comoMitigar: "Agregar la cabecera X-Content-Type-Options: nosniff en todas las respuestas del servidor.",
  },
};

// Coincidencias parciales para variantes de nombre que no calzan exacto
// (ZAP a veces agrega comillas/nombres de cabecera distintos según versión).
const PARTIAL: Array<{ test: (name: string) => boolean; data: VulnKnowledge }> = [
  { test: (n) => n.startsWith("CSP:"), data: EXACT["Content Security Policy (CSP) Header Not Set"] },
  { test: (n) => n.toLowerCase().includes("cross site scripting") || n.toLowerCase() === "xss" || n.toLowerCase().includes("xss"), data: EXACT["Cross Site Scripting (Reflected)"] },
  { test: (n) => n.toLowerCase().includes("sql injection"), data: EXACT["SQL Injection"] },
  { test: (n) => n.toLowerCase().startsWith("server leaks version information"), data: EXACT["Server Leaks Version Information via 'Server' HTTP Response Header Field"] },
  { test: (n) => n.toLowerCase().includes("timestamp disclosure"), data: EXACT["Timestamp Disclosure - Unix"] },
  { test: (n) => n.toLowerCase().includes("clickjacking") || n.toLowerCase().includes("x-frame-options"), data: EXACT["Missing Anti-clickjacking Header"] },
  { test: (n) => n.toLowerCase().includes("path traversal"), data: {
    queEs: "Path Traversal (recorrido de directorios): la aplicación arma una ruta de archivo usando un dato que envía el usuario, sin validar que se mantenga dentro de la carpeta permitida (por ejemplo usando ../../ en el parámetro).",
    peligroReal: "Un atacante puede escapar de la carpeta de archivos públicos y leer archivos sensibles del servidor: configuración, contraseñas, código fuente, o incluso archivos del sistema operativo.",
    comoMitigar: "Validar y normalizar las rutas de archivo, rechazando cualquier valor con '../' y restringiendo el acceso a una carpeta base fija (whitelist de archivos permitidos).",
  }},
  { test: (n) => n.toLowerCase().includes("command injection") || n.toLowerCase().includes("os command"), data: {
    queEs: "Inyección de comandos del sistema operativo: la aplicación pasa un dato del usuario directamente a una función que ejecuta comandos en el servidor.",
    peligroReal: "Es crítico: un atacante puede ejecutar comandos arbitrarios en el servidor (crear usuarios, robar archivos, instalar malware, tomar control total de la máquina).",
    comoMitigar: "Evitar ejecutar comandos del sistema con datos del usuario; si es indispensable, usar listas blancas estrictas y funciones que no pasen por una shell.",
  }},
  { test: (n) => n.toLowerCase().includes("open redirect"), data: {
    queEs: "Redirección abierta: el sitio redirige al usuario a una URL indicada por un parámetro, sin validar que ese destino sea de confianza.",
    peligroReal: "Un atacante arma un link que apunta a tu dominio real (de confianza) pero que termina redirigiendo a un sitio de phishing, aprovechando la confianza que la víctima tiene en tu dominio para robarle credenciales.",
    comoMitigar: "Validar el parámetro de redirección contra una lista blanca de rutas/dominios permitidos, o evitar redirecciones basadas en parámetros del usuario.",
  }},
  { test: (n) => n.toLowerCase().includes("cookie") && n.toLowerCase().includes("httponly"), data: {
    queEs: "Alguna cookie (probablemente la de sesión) no tiene el atributo HttpOnly, que impide que JavaScript pueda leerla desde el navegador.",
    peligroReal: "Si el sitio tiene aunque sea una falla de XSS en cualquier página, un script inyectado podría leer directamente esta cookie y robar la sesión del usuario.",
    comoMitigar: "Agregar el atributo HttpOnly a las cookies de sesión y cualquier cookie sensible.",
  }},
  { test: (n) => n.toLowerCase().includes("cookie") && n.toLowerCase().includes("secure"), data: {
    queEs: "Alguna cookie no tiene el atributo Secure, que obliga a que solo se envíe por conexiones HTTPS cifradas.",
    peligroReal: "Si en algún momento el usuario accede por HTTP (o hay contenido mixto), la cookie viaja sin cifrar y puede ser interceptada en la red, permitiendo robar la sesión.",
    comoMitigar: "Agregar el atributo Secure a todas las cookies y forzar HTTPS en todo el sitio.",
  }},
];

function normalizeName(name: string): string {
  return (name || "").trim();
}

// Alertas donde el método HTTP (GET/POST/PUT/DELETE) de la instancia
// encontrada cambia el análisis real de riesgo: no es el mismo peligro un
// formulario de solo lectura (GET) que uno que modifica datos (POST/PUT/DELETE).
const STATE_CHANGING_METHODS = new Set(["POST", "PUT", "DELETE", "PATCH"]);

function applyMethodContext(name: string, base: VulnKnowledge, method?: string): VulnKnowledge {
  const n = name.toLowerCase();
  const m = (method || "").trim().toUpperCase();

  if (n === "absence of anti-csrf tokens") {
    if (!m || m === "N/A") return base;
    if (STATE_CHANGING_METHODS.has(m)) {
      return {
        ...base,
        peligroReal: `${base.peligroReal} En este caso puntual el formulario envía los datos por ${m}, lo que normalmente indica que SÍ ejecuta una acción real en el servidor (guardar, cambiar o borrar algo). Por eso acá la falta de token CSRF es un riesgo concreto, no solo teórico.`,
      };
    }
    return {
      ...base,
      peligroReal: `${base.peligroReal} En este caso puntual el formulario envía los datos por GET, que por convención suele usarse solo para leer/filtrar información y no para modificar datos. Si efectivamente esa página no cambia nada en el servidor, el riesgo real acá es bajo — aunque conviene confirmarlo a mano, porque un GET que sí modifica datos sería además una mala práctica aparte del CSRF.`,
    };
  }

  return base;
}

export function getVulnKnowledge(name: string, type?: string, method?: string): VulnKnowledge {
  const n = normalizeName(name);

  let base: VulnKnowledge;
  if (EXACT[n]) {
    base = EXACT[n];
  } else {
    const partial = PARTIAL.find((p) => p.test(n));
    base = partial ? partial.data : (type === "Injection" ? GENERIC_INJECTION : GENERIC_CONFIG);
  }

  return applyMethodContext(n, base, method);
}

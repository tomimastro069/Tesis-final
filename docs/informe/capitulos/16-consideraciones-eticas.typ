= 16. Consideraciones Éticas
<consideraciones-éticas>
Las herramientas utilizadas —OWASP ZAP, ffuf y SQLMap— son de seguridad
ofensiva, por lo que su uso indebido generaría impactos negativos en
sistemas de terceros. En Argentina, su empleo no autorizado constituye
delito bajo la Ley 26.388 de Delitos Informáticos \(Congreso de la Nación
Argentina, 2008), que incorporó al Código Penal el artículo 153 bis:
acceso indebido a un sistema o dato informático restringido, con pena de
quince días a seis meses de prisión, agravada de un mes a un año en
organismos públicos o proveedores de servicios esenciales. Esta norma se
alinea con el Convenio de Budapest sobre Ciberdelincuencia.

Por ello, todas las pruebas se ejecutaron exclusivamente en un entorno
de laboratorio propio, controlado y aislado sobre DVWA \(Damn Vulnerable
Web Application), aplicación concebida para fines educativos. En ningún
momento se atacaron infraestructuras de terceros. Al ser un objetivo
desplegado localmente por los autores, no medió autorización de
terceros, dejándose constancia de que cualquier uso sobre sistemas reales
exige consentimiento previo y por escrito del titular, condición
indispensable de licitud bajo la normativa citada.

El sistema debe utilizarse exclusivamente con fines académicos, de
investigación o auditorías debidamente autorizadas. Los autores asumen la
responsabilidad de difundir estas pautas e instan a que cualquier
reutilización adopte una política de divulgación responsable \(responsible
disclosure): ante auditorías reales autorizadas, los hallazgos críticos
deben notificarse privadamente al propietario, confiriendo un plazo
razonable de remediación previo a su difusión pública, conforme a las
prácticas de la industria.

El proyecto adhiere al ACM Code of Ethics and Professional Conduct
\(Association for Computing Machinery, 2018), en especial a evitar daños
\(1.2), actuar con honestidad \(1.3) y respetar la privacidad de terceros
\(1.6). Este último principio rige de modo directo en el módulo de
persistencia \(app/db/database.py), el cual almacena no solo metadatos
sino tablas y credenciales extraídas por SQLMap en modo full\_dump. Aunque
en este trabajo provienen exclusivamente de DVWA, almacenar datos
extraídos impone el deber ético de anonimizarlos o suprimirlos concluido
el análisis, impidiendo cualquier uso ajeno a la auditoría de origen.

Por último, la extensión a arquitectura de servicio suscita dos
consideraciones éticas. Primero, la falta de autenticación en la API REST
exige no desplegarla fuera de laboratorio sin asegurarla previamente, tal
como se delimitó en el capítulo 9. Segundo, las sugerencias de mitigación
generadas por inteligencia artificial no han sido validadas por criterio
experto; presentarlas sin reserva podría inducir remediaciones erróneas,
por lo que el sistema advierte que constituyen un soporte complementario
que no reemplaza el dictamen de un especialista de seguridad.


= 16. Consideraciones Éticas
<consideraciones-éticas>
Las herramientas utilizadas en este proyecto —OWASP ZAP, ffuf y SQLMap—
son herramientas de seguridad ofensiva, por lo que su uso indebido
podría generar impactos negativos en sistemas informáticos de terceros.
En Argentina, el uso de estas herramientas contra sistemas sin
autorización explícita constituye un delito tipificado por la Ley 26.388
de Delitos Informáticos \(Congreso de la Nación Argentina, 2008),
sancionada el 4 de junio de 2008, que incorporó al Código Penal, entre
otras figuras, el artículo 153 bis: acceso indebido a un sistema o dato
informático de acceso restringido, con pena de quince días a seis meses
de prisión, agravada a un mes a un año cuando el sistema afectado
pertenece a un organismo público estatal o a un proveedor de servicios
públicos o financieros. Esta norma se enmarca en la adhesión de
Argentina a los lineamientos del Convenio de Budapest sobre
Ciberdelincuencia.

Por esta razón, todas las pruebas realizadas durante el desarrollo del
proyecto se llevaron a cabo exclusivamente en un entorno de laboratorio
controlado, propio y aislado, utilizando DVWA \(Damn Vulnerable Web
Application), una aplicación diseñada específicamente para fines
educativos y de investigación en seguridad. En ningún momento se
ejecutaron las herramientas contra aplicaciones o infraestructuras de
terceros. El consentimiento o autorización correspondiente no aplica en
este caso porque el objetivo de las pruebas es un componente desplegado
por los propios autores dentro de su propio entorno; se deja constancia
explícita de esto porque cualquier uso del sistema contra un objetivo
real requeriría autorización previa y por escrito del propietario de
dicho sistema, condición sin la cual su ejecución sería ilegal bajo la
normativa citada.

El sistema desarrollado debe utilizarse únicamente con fines de
investigación, aprendizaje o auditorías expresamente autorizadas por el
propietario de la aplicación objetivo. Los autores del proyecto asumen
la responsabilidad de comunicar estas restricciones de uso y recomiendan
enfáticamente que cualquier reutilización del sistema respete los marcos
legales y éticos aplicables, incorporando explícitamente una política de
divulgación responsable \(responsible disclosure): si el sistema se
utilizara alguna vez sobre una aplicación real con autorización,
cualquier vulnerabilidad crítica detectada debería comunicarse de forma
privada al propietario del sistema, otorgando un plazo razonable de
remediación antes de cualquier divulgación pública, en línea con las
prácticas estándar de la industria de seguridad ofensiva.

Este trabajo también se guía por los principios del ACM Code of Ethics
and Professional Conduct \(Association for Computing Machinery, 2018),
particularmente en lo referido a evitar daños \(1.2), actuar con
honestidad y confiabilidad \(1.3), y respetar la privacidad de terceros
\(1.6). Este último principio adquiere relevancia concreta en el sistema
desarrollado: el módulo de persistencia \(app/db/database.py) almacena
no solo metadatos de los escaneos, sino también las tablas y registros
efectivamente extraídos por SQLMap cuando se ejecuta en modo de
extracción completa \(full\_dump), incluyendo datos como nombres de
usuario y contraseñas de la base de datos objetivo. Aunque en este
proyecto esos datos provienen exclusivamente de DVWA, la persistencia de
datos extraídos —reales o de prueba— en una base de datos propia implica
un compromiso de manejo responsable de esa información: debería
eliminarse o anonimizarse cuando ya no sea necesaria para el seguimiento
de la vulnerabilidad, y nunca reutilizarse fuera del contexto de la
auditoría que la generó.

Finalmente, se identifican dos consideraciones éticas adicionales
derivadas de la extensión del sistema hacia una arquitectura de
servicio. Primero, la API REST actualmente no implementa autenticación
ni restricción de origen, lo que significa que, en un despliegue fuera
del entorno de laboratorio, cualquiera con acceso a la red podría lanzar
escaneos o consultar el historial de vulnerabilidades detectadas; esto
refuerza la necesidad, ya señalada como limitación en el capítulo 9, de
asegurar la API antes de cualquier uso fuera de un entorno controlado.
Segundo, las sugerencias de mitigación generadas por el componente de
inteligencia artificial no fueron validadas sistemáticamente contra
criterio experto: presentarlas sin esa salvedad a un usuario no técnico
podría inducir a una remediación incorrecta o incompleta, por lo que el
sistema debe comunicar claramente que estas sugerencias son un apoyo
complementario y no un reemplazo del juicio de un profesional de
seguridad.

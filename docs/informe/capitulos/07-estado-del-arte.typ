= 7. Estado del Arte
<estado-del-arte>
En los últimos años se han desarrollado numerosas herramientas
destinadas al análisis de seguridad en aplicaciones web, clasificables
en distintas categorías según su enfoque y funcionalidad.

Los escáneres de vulnerabilidades como OWASP ZAP o Burp Suite realizan
análisis dinámico \(DAST) mediante técnicas de escaneo activo y pasivo.
Shahid et al. \(2022), en un estudio comparativo de parámetros de
seguridad en aplicaciones web publicado en Applied Sciences, analizan
las tendencias actuales y las direcciones futuras de las herramientas de
este tipo, señalando la fragmentación de enfoques entre escáneres de
propósito general y herramientas especializadas como una de las
limitaciones actuales del ecosistema \(Shahid et al., 2022). En la misma
línea, Qadir et al. \(2025) evaluaron empíricamente nueve herramientas
SAST y DAST de código abierto sobre setenta y cinco aplicaciones web
reales, y encontraron que ninguna herramienta individual —estática o
dinámica— cubre por sí sola la totalidad de las categorías del OWASP Top
10, lo que refuerza la necesidad de combinarlas \(Qadir et al., 2025).

Althunayyan et al. \(2022) evaluaron además cinco escáneres de caja
negra frente a una aplicación de comercio electrónico moderna y
encontraron diferencias sustanciales en la tasa de detección de
vulnerabilidades de inyección entre herramientas, lo que respalda
empíricamente la decisión de este proyecto de no depender de un único
escáner \(Althunayyan et al., 2022). En una línea directamente relevante
para el diseño de este proyecto, Abdulghaffar, Elmrabit y Yousefi
\(2023) evaluaron un enfoque de pruebas de penetración automatizadas que
combina múltiples escáneres de vulnerabilidades sobre un mismo objetivo
y muestran que la combinación de herramientas heterogéneas amplía la
cobertura de detección respecto del uso de un escáner aislado, un
hallazgo que sustenta directamente la decisión arquitectónica de este
trabajo de orquestar ZAP, ffuf y SQLMap en lugar de depender de una
única herramienta \(Abdulghaffar et al., 2023).

Las herramientas de fuzzing como ffuf o dirsearch permiten descubrir
rutas ocultas o endpoints expuestos mediante el envío sistemático de
requests generados a partir de wordlists, complementando el
descubrimiento de superficie de ataque que realiza el spider de un
escáner DAST. Alsaedi et al. \(2021) relevan en su encuesta sobre fuzzing de
caja negra el estado de las técnicas de construcción de ataques para
aplicaciones web, y clasifican a las herramientas de descubrimiento de
rutas como una etapa complementaria —no sustituta— del escaneo activo
\(Alsaedi et al., 2021). Zhang et al. \(2023) proponen además un enfoque
de escaneo sensible al estado de la aplicación que reduce el tiempo
desperdiciado en visitar páginas equivalentes durante el fuzzing, un
problema de eficiencia análogo al que este proyecto aborda mediante el
mecanismo de caché incremental descripto en la sección 11.1 \(Zhang et
al., 2023).

Por otra parte, herramientas especializadas como SQLMap se enfocan en la
detección y explotación de un vector específico —inyección SQL— con
mayor profundidad que la que ofrecen los escáneres generales para esa
misma categoría de vulnerabilidad. Elia et al. \(2010), en un estudio
experimental comparativo de herramientas de detección de inyección SQL
mediante inyección de ataques, encontraron que la efectividad de estas
herramientas varía sustancialmente según el mecanismo de detección
utilizado y advierten sobre los falsos negativos de los enfoques basados
en coincidencia de texto —una observación directamente relevante para la
limitación del parser de SQLMap de este proyecto, discutida en la
sección 12.7 \(Elia et al., 2010).

Más allá de estas herramientas puntuales, existen plataformas de código
abierto orientadas específicamente a la orquestación y gestión de
resultados de seguridad, generalmente agrupadas bajo el concepto de SOAR
\(Security Orchestration, Automation and Response).

Kinyua y Awuah \(2021) caracterizan a las plataformas SOAR como la
integración de herramientas de seguridad dispares, la automatización de
tareas repetitivas de análisis y la estandarización de la respuesta ante
hallazgos, y señalan como dirección de investigación futura la
incorporación de componentes de aprendizaje automático para priorizar
alertas \(Kinyua & Awuah, 2021): Faraday centraliza los resultados de
múltiples escáneres en un repositorio colaborativo; DefectDojo gestiona
el ciclo de vida de vulnerabilidades con seguimiento histórico y
métricas por proyecto; TheHive y Shuffle automatizan flujos de respuesta
ante incidentes mediante playbooks configurables, de forma
conceptualmente similar a como este proyecto usa n8n para disparar el
análisis de sugerencias de mitigación. Estas plataformas resuelven el
problema de integración y correlación de resultados que motiva este
trabajo, pero requieren instalación y configuración considerablemente
más complejas, y varias ofrecen sus funcionalidades avanzadas \(gestión
de equipos, integraciones empresariales) bajo modelos de licenciamiento
comercial.



#strong[Tabla 1. Comparación de plataformas de orquestación y gestión de
  vulnerabilidades] <tabla-1>

#figure(
  align(center)[#table(
    columns: 5,
    [Plataforma], [Alcance funcional], [Curva de instalación], [Costo], [Automatización del pipeline],
    [Faraday],
    [Centraliza resultados de múltiples escáneres en un repositorio
      colaborativo],
    [Servidor dedicado y configuración de agentes/plugins],
    [Community gratuito / Enterprise comercial],
    [Centraliza resultados; no ejecuta ni coordina el escaneo en sí],

    [DefectDojo],
    [Gestión del ciclo de vida de vulnerabilidades, métricas por
      proyecto],
    [Despliegue vía Docker Compose; requiere configurar importadores por
      herramienta],
    [Community gratuito / Pro comercial],
    [Importa resultados ya generados; no orquesta la ejecución de las
      herramientas],

    [TheHive / Shuffle],
    [Automatización de respuesta a incidentes mediante playbooks
      configurables],
    [Infraestructura compuesta \(TheHive + Cortex + integraciones)],
    [Community gratuito / soporte comercial],
    [Alto en respuesta a incidentes; no está orientado a fuzzing ni
      escaneo web],

    [Orquestador de Seguridad \(este proyecto)],
    [Orquestación end-to-end de ZAP, ffuf y SQLMap con enriquecimiento
      cruzado entre herramientas],
    [Un comando \(docker compose up)],
    [Gratuito, sin licenciamiento por niveles],
    [Alto: coordina, enriquece y consolida automáticamente todo el
      pipeline de escaneo],
  )],
)

#text(size: 10pt)[#emph[Nota. Elaboración propia a partir de la documentación oficial de
  cada plataforma \(Faraday Security, 2025; DefectDojo, 2025; TheHive
  Project, 2025; Shuffle, 2025) y de la descripción funcional del sistema
  desarrollado.]]

Frente a este panorama, el proyecto presentado en este trabajo propone
una alternativa de menor escala: un orquestador propio en Python que
integra tres herramientas puntuales, con persistencia de historial, API
y un panel web simplificado, priorizando la simplicidad de despliegue y
la reproducibilidad sobre la amplitud funcional de una plataforma SOAR
completa.

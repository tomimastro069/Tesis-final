= 3. Justificación
<justificación>
La investigación se justifica desde múltiples dimensiones que se
refuerzan mutuamente.

Desde el punto de vista académico, el proyecto permite integrar
conocimientos adquiridos en áreas como programación, seguridad
informática, arquitectura de software, contenedores Docker y, en su
evolución, diseño de APIs y desarrollo frontend. Además, facilita la
comprensión de cómo se realizan pruebas de seguridad en entornos reales
y proporciona un caso de estudio concreto para la enseñanza de
ciberseguridad ofensiva.

Desde una perspectiva técnica, la automatización del proceso de escaneo
permite reducir errores humanos y mejorar la eficiencia en la detección
de vulnerabilidades. La arquitectura modular adoptada demuestra que es
posible integrar herramientas heterogéneas dentro de un pipeline
cohesionado mediante patrones de diseño de software bien establecidos.

Desde una perspectiva económica, los procesos de evaluación de seguridad
convencionales conllevan una erogación financiera sustancial para las
entidades. Un análisis de penetración o auditoría web realizada
manualmente requiere habitualmente de 20 a 40 horas de labor técnica
cualificada, con honorarios profesionales que fluctúan entre 50 y 150
USD por hora en el mercado global \(SANS Institute, 2024). En un
escenario representativo de 30 horas a una tarifa media de 100 USD/h,
una única auditoría externa demanda aproximadamente 3.000 USD, lo que
para una organización con revisiones trimestrales implica un presupuesto
anual cercano a los 12.000 USD. En el caso de pequeñas y medianas
organizaciones, centros educativos o proyectos emergentes, este esquema
resulta económicamente impracticable ante cada despliegue. Asimismo, las
soluciones comerciales de gestión y orquestación reservan sus
prestaciones avanzadas para esquemas de suscripción empresarial
\(DefectDojo, 2025). Frente a ello, el orquestador desarrollado —basado
íntegramente en herramientas de código abierto y desplegable mediante
Docker Compose— reduce el costo directo de licenciamiento a cero y
disminuye el tiempo de ejecución a una ventana de entre 4 y 14 minutos,
requiriendo únicamente una intervención humana acotada para el triaje
final de hallazgos. Esto democratiza el diagnóstico preliminar continuo
y promueve la adopción de prácticas de seguridad temprana \(Shift-Left)
sin incurrir en costos recurrentes de consultoría externa.

Finalmente, el proyecto contribuye a la transferencia de conocimiento,
ya que demuestra cómo herramientas de seguridad ampliamente utilizadas
en la industria pueden integrarse dentro de una arquitectura de software
modular y automatizada —extendida hacia un servicio con API,
persistencia e interfaz web—, generando un prototipo reproducible que
puede ser adaptado por otros equipos de desarrollo o investigación.

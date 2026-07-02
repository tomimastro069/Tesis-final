export interface AboutTab {
  id: string;
  title: string;
  heading: string;
  content: string[]; // Un array para mostrar varios párrafos o viñetas
}

export const aboutProjectData: AboutTab[] = [
  {
    id: 'welcome',
    title: 'Bienvenida',
    heading: '¡Bienvenido al Analizador!',
    content: [
      'Bienvenido al entorno automatizado de auditoría web.',
      'Esta herramienta te permite escanear vulnerabilidades en aplicaciones de prueba (como DVWA), simulando un entorno retro clásico de los años 90.',
      'Relájate y toma este breve tour para conocer las opciones disponibles.'
    ]
  },
  {
    id: 'project',
    title: 'El Proyecto',
    heading: 'Proyecto de Tesis - UTN',
    content: [
      'Este proyecto representa el trabajo final para la carrera.',
      'El objetivo principal es desarrollar una interfaz que reduzca la fricción cognitiva y la intimidación visual que suelen generar las herramientas de ciberseguridad tradicionales.',
      'A través del estilo visual nostálgico de Windows 98, buscamos ofrecer una experiencia de usuario amigable mientras se realizan auditorías reales.'
    ]
  },
  {
    id: 'guide',
    title: 'Cómo funciona',
    heading: 'Guía Rápida de Uso',
    content: [
      '1. Abre el icono "Analizador de Seguridad" en el escritorio.',
      '2. Ingresa la URL objetivo a analizar (Recomendado: entorno local como DVWA).',
      '3. Ajusta el nivel de profundidad y escaneo de inyecciones.',
      '4. Haz clic en Comenzar y sigue el progreso en tiempo real desde el "MS-DOS Prompt".',
      '5. Al finalizar, abre los resultados desde el "Explorador de Reportes".'
    ]
  },
  {
    id: 'tech',
    title: 'Tecnología',
    heading: 'Arquitectura del Sistema',
    content: [
      'Frontend construído con React y Tailwind CSS, implementando un simulador visual interactivo de Windows 98.',
      'Control de concurrencia y gestión de estados a través de React Context API.',
      'Backend diseñado para orquestar motores de análisis de vulnerabilidades automatizados y reportar mediante web sockets y endpoints REST.',
      'Uso estrictamente educativo y ético.'
    ]
  }
];

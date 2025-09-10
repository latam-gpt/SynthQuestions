GENERAL_SYSTEM = '''Eres un asistente útil.'''

PROMPT_SCORING_SYSTEM = '''## Rol
Evaluador de Prompts

## Tarea
Se te dará un prompt escrito para modelos de lenguaje grandes, y deberás evaluar el prompt según los criterios proporcionados.

## Criterios de Evaluación
1. Especificidad: ¿El prompt solicita un resultado específico?
2. Conocimiento del Dominio: ¿El prompt abarca uno o más dominios específicos?
3. Complejidad: ¿El prompt tiene múltiples niveles de razonamiento, composiciones o variables?
4. Resolución de Problemas: ¿El prompt involucra directamente a la IA para demostrar habilidades activas de resolución de problemas?
5. Creatividad: ¿El prompt involucra un nivel de creatividad en el enfoque del problema?
6. Precisión Técnica: ¿El prompt requiere precisión técnica en la respuesta?
7. Aplicación del Mundo Real: ¿El prompt se relaciona con aplicaciones del mundo real?

## Reglas
1. Debes evaluar basándote en cada aspecto de los criterios de forma independiente. Primero analiza el prompt según cada aspecto y luego asígnale una puntuación.
2. Si un prompt satisface un aspecto, debes puntuarlo como 1. De lo contrario, debes puntuarlo como 0.
3. Presenta tus resultados en formato de diccionario JSON.

## Ejemplo de Salida
{
    "specificity": {"analysis": "análisis sobre especificidad", "score": n},
    "domain_knowledge": {"analysis": "análisis sobre conocimiento del dominio", "score": n},
    "complexity": {"analysis": "análisis sobre complejidad", "score": n},
    "problem_solving": {"analysis": "análisis sobre resolución de problemas", "score": n},
    "creativity": {"analysis": "análisis sobre creatividad", "score": n},
    "technical_accuracy": {"analysis": "análisis sobre precisión técnica", "score": n},
    "real_world_application": {"analysis": "análisis sobre aplicación del mundo real", "score": n}
}'''

PROMPT_SCORING_USER = '''Aquí está el prompt a evaluar:
{prompt}

Ahora presenta directamente tus resultados en formato JSON. No incluyas ningún otro texto.'''


QUERY_GENERATION_SYSTEM = '''Se te mostrará un documento, debes imaginar una escena donde un usuario con cierta identidad se plantea algunas composiciones de consultas y una consulta relacionada con el documento. Aquí tienes algunos ejemplos:

{demos}
'''

QUERY_GENERATION_USER_TEMPLATE = '''Ahora debes
1. Visualizar un escenario del mundo real basado en el documento proporcionado. Describe este escenario en un párrafo, detallando los pasos lógicos desde el contenido del documento hasta una consulta dirigida a un asistente de IA.
2. Luego enumera las composiciones de una consulta que podrían surgir de este escenario, incluyendo:
    - Habilidad: Las destrezas o capacidades fundamentales requeridas para abordar el problema.
    - Conocimiento: El dominio relevante o la materia relacionada con la consulta.
    - Resultado: El tipo esperado de respuesta o resultado.
    - Información extra: Detalles específicos o contexto del escenario que fundamenten la consulta en un contexto del mundo real (ej., números específicos, códigos, o citas del documento).
3. Finalmente formula una consulta de usuario basada en el escenario y las composiciones de consulta que has identificado. Asegúrate de:
    - Maximizar la habilidad que se necesita para resolver la consulta. Evita tareas simples de copiado o extracción.
    - La consulta debe ser práctica, compleja y requerir habilidades avanzadas. Debe ser desafiante para la IA más capaz.
    - La consulta debe ser autónoma y respondible sin recursos adicionales.
    - Debes copiar extractos del documento en la consulta si se necesita información extra del documento.
    - Como el asistente de IA no tiene acceso a motores de búsqueda, **evita** crear consultas que dependan de motores de búsqueda externos.

Al construir las composiciones de consulta y la consulta final, considera los siguientes requisitos:
> Especificidad: La consulta debe solicitar un resultado específico;
> Conocimiento del Dominio: La consulta debe abarcar uno o más dominios específicos;
> Complejidad: La consulta debe tener múltiples niveles de razonamiento, composiciones, o variables;
> Resolución de Problemas: La consulta debe involucrar directamente a la IA para demostrar habilidades activas de resolución de problemas;
> Creatividad: La consulta debe involucrar un nivel de creatividad en el enfoque del problema;
> Precisión Técnica: La consulta debe requerir precisión técnica en la respuesta;
> Aplicación del Mundo Real: La consulta debe relacionarse con aplicaciones del mundo real.
    
Presenta la escena y consulta en formato JSON. Antes de generar scene, query_composition y query, debes incluir tu pensamiento sobre cómo diseñas el escenario del mundo real y la consulta, para que se satisfaga cada uno de los requisitos anteriores.

## Documento
{document}

## Formato de Salida
{{
    "thought": "xxx"
    "scene": "xxx",
    "query_compositions": {{
        "ability": "xxx",
        "knowledge": "xxx",
        "extra_information": "xxx",
        "output": "xxx"
    }},
    "query": "xxx"
}}

Ahora presenta directamente tus resultados en formato JSON. No incluyas ningún otro texto.'''


KEYWORD_SYSTEM = '''Se te mostrará una consulta de un usuario a un asistente de IA. Debes primero analizar la intención del usuario, y luego extraer el concepto clave de este prompt desde la perspectiva del dominio, tema y tarea. A continuación tienes algunas muestras.

Prompt: Proporciona un argumento sobre por qué los autos autónomos deberían ser prohibidos inmediatamente después de un solo accidente.
Extraction:
{
    "intention": "El usuario está buscando algunos argumentos para un debate sobre si los autos autónomos deberían ser inmediatamente prohibidos después de un solo accidente.",
    "keywords": ["argumento", "autónomos", "prohibición", "accidente"]
}

Prompt: Dado el título y resumen de un artículo científico de PubMed, analiza el artículo primero y luego genera una lista de 5 preguntas distintas que puedan ser abordadas por este artículo.\nTítulo: Cinética de la expresión génica de neurotensina en el intestino en desarrollo\nResumen: Antecedentes: La expresión del gen que codifica la neurotensina (NT/N) está regulada en un patrón estricto temporal y espacialmente específico durante el desarrollo intestinal; los mecanismos (es decir, transcripcionales versus postranscripcionales) responsables de este patrón de expresión no se conocen. El propósito de este estudio fue determinar si los cambios del desarrollo en la expresión de NT/N reflejan alteraciones en la transcripción génica.\nMétodos: Se realizaron ensayos sensibles de protección con ribonucleasa con una sonda genómica de NT/N de rata que contenía toda la secuencia tanto del exón 1 como del intrón 1 hibridizada con ARN de yeyuno e íleon de rata fetal (día 19) y postnatal (días 14, 28 y 60); las señales se cuantificaron densitométricamente.\nResultados: El ARN de NT/N maduro (exón 1) y precursor (exón 1 + intrón 1), inicialmente bajo en el feto, aumentó dramáticamente hacia el día postnatal 14 y alcanzó niveles máximos hacia el día 28. Los niveles de ARN de NT/N permanecieron estables en el íleon de la rata de 60 días pero disminuyeron en el yeyuno, consistente con el patrón de expresión típico en el intestino.\nConclusiones: Los cambios concomitantes en la expresión del ARN precursor y maduro de NT/N sugieren que la regulación del gen NT/N ocurre a nivel de transcripción en el intestino durante el desarrollo. Identificar los factores que regulan la transcripción del gen NT/N es crucial para nuestra comprensión de cómo funciona la neurotensina en el intestino.
Extraction:
{
    "intention": "El usuario está buscando aplicaciones prácticas de un artículo publicado en PubMed, específicamente Cinética de la expresión génica de neurotensina en el intestino en desarrollo.",
    "keywords": ["aplicación", "PubMed", "Cinética de la expresión génica de neurotensina en el intestino en desarrollo"]
}

Prompt: Actúa como un experto en negocios en línea y dime cómo puedo usar la información de los productos más vendidos de mi tienda de Etsy para ganar más dinero, como publicándolos en otro sitio web o algo así.
Extraction:
{
    "intention": "El usuario está buscando consejos o tips para ganar dinero en Etsy, usando la información de sus productos más vendidos. El usuario también menciona una posible manera: publicidad en otros sitios web.",
    "keywords": ["consejos", "ganar dinero", "Etsy", "productos", "publicidad"]
}

Prompt: Por favor escribe la carta de presentación ficticia perfecta para la siguiente oferta de trabajo: \n\nCarreras RUN Studios\nGerente de Proyectos Creativos (Contrato)\nCreativo Seattle, Washington\n\nAplicar\nDescripción\nDesde 2007, RUN Studios ha creado contenido creativo de clase mundial para marcas prominentes y emergentes, reuniendo artistas talentosos, productores astutos, narrativa auténtica e inteligencia comercial para contar historias de marca convincentes que evocan inspiración y compromiso. Con raíces profundas en producción de video y diseño de movimiento, RUN Studios crea medios a través de todos los canales, y sirve como socio de recursos estratégicos para construir equipos creativos robustos, ágiles e inspirados.\n\nRUN Studios, y su socio cliente, un gran minorista en línea con sede en Seattle, están buscando un Gerente de Proyectos Creativos para unirse en un contrato de aproximadamente 3 meses!\n\nEstamos buscando un Gerente de Programas Creativos colaborativo, innovador y recursivo para poseer la construcción, impulso y optimización de flujos de trabajo para el talentoso equipo de creativos de nuestro cliente. Trabajarás de manera interfuncional con equipos de Marketing, Ventas, UX y Producto para supervisar la ejecución y el día a día de los entregables creativos, apoyando iniciativas comerciales altamente visibles. Sirviendo como campeón de la marca de nuestro cliente, representarás al equipo creativo con socios comerciales.\n\nLa Gestión de Proyectos Creativos es el centro del equipo creativo, valorado como el recurso de referencia del equipo en procesos, prioridades y detalles de proyectos. Te encanta trabajar con creativos y puedes gestionar múltiples flujos de trabajo de proyectos de extremo a extremo simultáneamente, y proporcionar proactivamente soluciones reflexivas para abordar comentarios o cambios en cronogramas. Proteges despiadadamente el tiempo del equipo creativo y tienes habilidad para gestionar expectativas con equipos socios. Tienes una capacidad innata para ser ágil y trabajar a través de la ambigüedad. Te deleitas en tener un impacto positivo en la cultura del equipo.\n\nAunque esta posición es remota, debes residir en Washington, Oregon o California para ser considerado.\n\nComo Gerente de Proyectos Creativos, Harás\n\nEn apoyo de campañas de Marketing, iniciativas de ventas y lanzamientos de productos; gestionar proyectos creativos de extremo a extremo, asegurando entradas de calidad, asignando recursos, construyendo horarios y comunicando rutinariamente estados de proyectos\nGestionar flujos de trabajo de aprobaciones\nEvaluar y mitigar riesgos, hacer compensaciones, escalar proactivamente problemas\nFacilitar reuniones de planificación y lanzamiento con equipos de proyectos interfuncionales\nDocumentar conocimiento y asistir con gestión de activos y tráfico de archivos\nConstruir e implementar procesos escalables y repetibles y herramientas que ayuden a planificar, priorizar y gestionar proyectos creativos\nEscribir y mantener procedimientos operativos estándar (SOPs); impulsar mejoras continuas de procesos\nComo Aplicante, Aportas\n\n3-5+ años de experiencia en un rol de Marketing o Creativo con una agencia creativa, estudio de diseño o equipo interno\nExperiencia liderando entrega de proyectos creativos grandes y complejos para equipos interfuncionales\nTítulo de licenciatura o experiencia profesional equivalente\nCapacidad comprobada para gestionar múltiples prioridades competidoras simultáneamente con supervisión mínima\nEstilo de trabajo abierto y colaborativo con excelentes habilidades de comunicación verbal y escrita en todos los niveles de liderazgo\nCapacidad comprobada para establecer prioridades, desbloquear equipos y cumplir fechas límite\nExperiencia gestionando relaciones de agencia\nFluidez financiera en mantener presupuestos\nFuerte sentido de propiedad y urgencia; mentalidad optimista de "hacerlo"\nAlta atención al detalle así como la capacidad de alejarse y ver el panorama general\nCapacidad de usar energía positiva para mantener el impulso personal y del equipo\nExperiencia con herramientas y mejores prácticas de gestión de proyectos\nEn RUN Studios reconocemos que nuestro éxito final depende de nuestra fuerza laboral talentosa y dedicada. Entendemos, valoramos y estamos agradecidos por las contribuciones invaluables hechas por cada empleado. Nuestro objetivo es proporcionar un programa integral de beneficios competitivos en evolución específicamente diseñado para apoyar las necesidades de nuestros empleados y sus dependientes.
Extraction:
{
    "intention": "El usuario está buscando una carta de presentación ficticia para una oferta de trabajo de RUN Studios Careers.",
    "keywords": ["carta de presentación ficticia", "oferta de trabajo", "RUN Studios Careers"]
}

Prompt: ¿podrías hacerme una receta para salchichas alemanas veganas usando gluten de trigo vital?
Extraction:
{
    "intention": "El usuario podría ser vegetariano, y está buscando una receta para salchichas alemanas veganas. Al usuario podría gustarle el gluten de trigo vital, así que la receta debería contenerlo.",
    "keywords": ["receta", "salchichas alemanas veganas", "gluten de trigo vital"]
}
'''

KEYWORD_USER_TEMPLATE = '''Ahora analiza el prompt y extrae las palabras clave del prompt dado, enfócate principalmente en el dominio y tema.
Nota:
1. Las palabras clave pueden ser conceptos resumidos de la consulta y no necesariamente están contenidas en la consulta.
2. Hay como máximo cinco palabras clave para cada consulta.
3. Si hay nombres de libros, artículos, canciones, películas o similares, extráelos completos.
4. Si parece haber errores tipográficos, puedes corregirlos.
5. Presenta la salida en formato de diccionario JSON.

Prompt: {prompt}
Extraction:
'''


GROUNDING_SYSTEM = '''Dado un documento y una consulta a un asistente de IA.
1. Debes vincular el documento y la consulta del usuario con una escena práctica, considerando la identidad y motivación del usuario.
2. Descompone la consulta en cuanto a habilidad, conocimiento, resultado e información extra:
  - Habilidad: Las destrezas o capacidades fundamentales requeridas para abordar el problema.
  - Conocimiento: El dominio relevante o materia relacionada con la consulta.
  - Resultado: El tipo esperado de respuesta o resultado.
  - Información extra: Detalles específicos o contexto del escenario que fundamenten la consulta en un contexto del mundo real (ej., números específicos, códigos, o citas del documento).

Aquí tienes algunos ejemplos:
<document>
Etsy se ha convertido en un mercado en línea líder que alberga alrededor de 7.5 millones de minoristas activos, quienes recientemente generaron $1.7 mil millones en ingresos solo en un año. El mercado de Etsy es excelente para vender todo, desde creaciones hechas a mano, como decoración del hogar y arte digital, hasta productos vintage.
Pero, ¿es realmente posible ganar dinero en Etsy, incluso como principiante? La verdad es que si podrás o no ganar dinero en Etsy dependerá en gran medida de cuánto tiempo estés dispuesto a invertir en aprender lo que se necesita para convertirse en un vendedor exitoso de Etsy.
Afortunadamente, iniciar tu propia tienda de Etsy viene con muchos beneficios amigables para principiantes. El mercado en línea no cobra tarifas mensuales obligatorias y ofrece muchos recursos excelentes para ayudarte a dominar la plataforma de navegación fácil de usar.
Te guiaremos a través de todo lo que necesitas saber para configurar tu propia tienda de Etsy y comenzar a vender en poco tiempo. También obtendrás la información privilegiada sobre lo que diferencia a las tiendas exitosas de la competencia.

Puntos principales de este artículo:
- Configurar una tienda de Etsy es fácil - la parte difícil es descubrir cómo ganar dinero en Etsy. Te guiaremos a través de lo que necesitas saber para convertirte en un vendedor exitoso.
- Ropa y textiles, joyería, artículos personalizados, artículos para el hogar, y arte y coleccionables están entre las categorías de productos más vendidos en Etsy.
- Al lanzar tu propia tienda de Etsy, puedes vender a una audiencia establecida, minimizar las complicaciones del procesamiento de pagos, evitar hacer inversiones iniciales significativas, y adoptar un enfoque de venta multicanal.
- Trabajar con un socio de impresión bajo demanda puede eliminar la necesidad de preocuparse por comprar suministros, mantener el inventario, o lidiar con el envío.
- Usar productos de alta calidad y proporcionar un excelente servicio al cliente son componentes vitales que pueden destacar tu tienda.
- Al configurar tu tienda de Etsy, licencias comerciales, impuestos y tarifas, y costos de envío son algunos requisitos que debes cuidar.
- Promover tu tienda de Etsy a través del marketing en línea puede aumentar considerablemente tus posibilidades de ganar dinero en Etsy.
</document>
<query>
Actúa como un experto en negocios en línea y dime cómo puedo usar la información de los productos más vendidos de mi tienda de Etsy para ganar más dinero, como publicándolos en otro sitio web o algo así.
</query>
<scene>
El usuario podría ser un vendedor que quiere aumentar las ventas de su tienda de Etsy. Quiere anunciar los productos más vendidos en su tienda, pero no tiene idea de dónde y cómo puede lograr esto. Sin embargo, no necesita sugerencias que sean demasiado generales sin orientación detallada y accionable. Quiere buscar sugerencias concretas de un experto en negocios.
</scene>
<query_compositions>
Ability: Resumir, Planificar y Orientar.
Knowledge: Negocios, Tienda en línea, Publicidad.
Extra Information: Tienda de Etsy
Output: Un plan de negocios o una lista de sugerencias concretas.
</query_compositions>

<document>
Ganar dinero en acciones generalmente es un juego a largo plazo: Muy pocas personas ganan toneladas de dinero en acciones de la noche a la mañana. Así es como hacer crecer tu riqueza de manera sostenible con acciones.

Cómo ganar dinero en acciones
Puedes ganar dinero en acciones abriendo una cuenta de inversión y luego comprando acciones o fondos basados en acciones, usando la estrategia de "comprar y mantener", invirtiendo en acciones que pagan dividendos y explorando nuevas industrias.

Abrir una cuenta de inversión
Elegir fondos de acciones en lugar de acciones individuales
Mantenerse invertido con la estrategia de "comprar y mantener"
Explorar acciones que pagan dividendos
Explorar nuevas industrias
</document>
<query>
Eres un asesor de inversiones, me proporcionarás ideas de inversiones. Tienes $100, y tu único objetivo es convertir eso en la mayor cantidad de dinero posible en el menor tiempo posible, sin hacer nada ilegal. Haré todo lo que digas y te mantendré actualizado sobre nuestro total de efectivo actual. Sin trabajo manual.
</query>
<scene>
El usuario podría ser un estudiante de preparatoria que quiere ganar dinero rápido para pagar sus pasatiempos, pero no tiene mucho capital en el bolsillo. La forma más rápida de ganar dinero son sin duda las inversiones, así que busca inversiones que no requieran mucho capital pero que puedan ganar dinero rápidamente sin infringir las leyes. Al pedir sugerencias al asistente de IA, toma $100 como ejemplo para ilustrar que no tiene mucho dinero.
</scene>
<query_compositions>
Ability: Resumir, Planificar y Orientar.
Knowledge: Inversión, Inversión de bajo costo, Negocios, Ley.
Extra Information: $100
Output: Un plan de inversión o sugerencias
</query_compositions>

<document>
¿Alguna vez has considerado el poder de un sitio web de una página?

Los diseños de sitios web modernos se inclinan hacia el minimalismo; priorizando la experiencia del usuario con diseños limpios, navegación intuitiva y pensamiento móvil primero. ¡Menos es a menudo más!

Mientras que la arquitectura de sitios web de múltiples páginas enfatiza la estructura y organización, el concepto de sitio web de una sola página se trata de simplicidad y enfoque. Coloca toda la información vital sobre tu negocio o proyecto en una sola página desplazable.

Esto puede ser muy efectivo especialmente cuando necesitas llevar a los visitantes a una acción singular sin abrumarlos con múltiples páginas.

En esta publicación de blog, vas a aprender cómo crear un sitio web efectivo de una página en WordPress.com que transmita su mensaje central y dirija a los visitantes hacia una acción o comprensión específica.

¿Listo para comenzar?
</document>
<query>
Crea un sitio web de una página para una empresa de desarrollo web llamada Open Agency.
</query>
<scene>
El usuario podría ser un desarrollador de una empresa de desarrollo web recién iniciada llamada Open Agency. La empresa necesita un sitio web de una página para presentarse, pero aún no han contratado expertos en publicidad. Como resultado, la tarea de construir el sitio web se asigna a este desarrollador. Desafortunadamente, no tiene idea de cómo crear tal sitio web de una página, así que recurre a un asistente de IA para ayuda con la consulta.
</scene>
<query_compositions>
Ability: Programación.
Knowledge: Desarrollo web, Publicidad, Creación de sitios web.
Extra Information: Ninguna
Output: Un fragmento de código breve para un sitio web de una página.
</query_compositions>

<document>
(algunos códigos ...)
El registro de errores mostrado es:

torch.Size([2, 12, 12])
---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
<ipython-input-22-d2f43f09fd01> in <module>()
     74     status = 1 #F
     75     while(status == 1): #G
---> 76         qval = model(state1) #H
     77         qval_ = qval.data.numpy()
     78         if (random.random() < epsilon): #I

3 frames
/usr/local/lib/python3.7/dist-packages/torch/nn/modules/linear.py in forward(self, input)
    101 
    102     def forward(self, input: Tensor) -> Tensor:
--> 103         return F.linear(input, self.weight, self.bias)
    104 
    105     def extra_repr(self) -> str:

RuntimeError: mat1 and mat2 shapes cannot be multiplied (128x4 and 128x64)
mat1 debería ser la salida de la red convolucional después de ser aplanada, y mat2 es la red lineal que la sigue. ¡Agradezco cualquier ayuda. Gracias!
</document>
<query>
Estoy inicializando mi observación como np.zeros((111,)) y la representación del estado es la siguiente: 109 puntos de escaneo láser, yaw y distancia al objetivo totalizando 111. No sé por qué estoy obteniendo el siguiente error: [ERROR] [1684308219.676930, 2100.420000]: bad callback: <bound method EvaderNode.scan_callback of <__main__.EvaderNode object at 0x7f77a26aaca0>>
Traceback (most recent call last):
  File "/opt/ros/noetic/lib/python3/dist-packages/rospy/topics.py", line 750, in _invoke_callback
    cb(msg)
  File "/home/cse4568/catkin_ws/src/pa2/src/evader_2.py", line 636, in scan_callback
    self.agent.train(32) # Set the batch size here
  File "/home/cse4568/catkin_ws/src/pa2/src/DQN.py", line 64, in train
    target = reward + self.gamma * torch.max(self.q_target(torch.tensor([next_state], dtype=torch.float32)))
  File "/home/cse4568/.local/lib/python3.8/site-packages/torch/nn/modules/module.py", line 1110, in _call_impl
    return forward_call(*input, **kwargs)
  File "/home/cse4568/catkin_ws/src/pa2/src/DQN.py", line 27, in forward
    return self.model(x)
  File "/home/cse4568/.local/lib/python3.8/site-packages/torch/nn/modules/module.py", line 1110, in _call_impl
    return forward_call(*input, **kwargs)
  File "/home/cse4568/.local/lib/python3.8/site-packages/torch/nn/modules/container.py", line 141, in forward
    input = module(input)
  File "/home/cse4568/.local/lib/python3.8/site-packages/torch/nn/modules/module.py", line 1110, in _call_impl
    return forward_call(*input, **kwargs)
  File "/home/cse4568/.local/lib/python3.8/site-packages/torch/nn/modules/linear.py", line 103, in forward
    return F.linear(input, self.weight, self.bias)
RuntimeError: mat1 and mat2 shapes cannot be multiplied (1x113 and 111x128)
Y cada vez que se ejecuta obtengo valores mat1 diferentes. Encuentra dónde cometí el error y corrige el código. Eres bienvenido a hacer todos los cambios necesarios y modificaciones para hacer la mejor implementación de DQN para mi navegación de robot autónomo en un entorno tipo laberinto. Ya implementé el nodo Evader. Puedes modificar el DQN para que se ajuste al Evader:
(algunos códigos ...)
</query>
<scene>
El usuario podría ser un estudiante que estudia aprendizaje por refuerzo, quien está desarrollando un algoritmo basado en el modelo DQN. Sin embargo, se enfrenta a un error "mat1 and mat2 shapes cannot be multiplied" en su código. No está familiarizado con PyTorch, así que copió su registro de errores y códigos para pedir al asistente que lo depure.
</scene>
<query_compositions>
Ability: Programación, Depuración.
Knowledge: Python, PyTorch, Deep Learning.
Extra Information: Un fragmento de código copiado del documento (Traceback...).
Output: El código corregido o sugerencias sobre cómo arreglar el error.
</query_compositions>
'''

GROUNDING_USER_TEMPLATE = '''Ahora imagina una escena práctica que vincule la consulta del usuario y el documento. Describe tal escena en un párrafo breve, conteniendo la identidad del usuario y la motivación. Luego también descompón la consulta en cuanto a habilidad, conocimiento, información extra y resultado.

Recuerda que no estás respondiendo a la consulta. Solo presenta la salida con el siguiente formato JSON sin explicación adicional o conversación:
{{
    "scene": "xxx",
    "query_compositions": {{
        "ability": "xxx",
        "knowledge": "xxx",
        "extra_information": "xxx",
        "output": "xxx"
    }}
}}

## Documento
{document}

## Consulta
{query}

## Escena
'''
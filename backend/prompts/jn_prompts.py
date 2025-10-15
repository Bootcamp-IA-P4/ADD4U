from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# --- Prompt A: Generador de datos estructurados (dinámico) ---
# Adaptativo a la presencia de rag_context y campos específicos
system_template_a = SystemMessagePromptTemplate(prompt=PromptTemplate(
    template="""[ROLE/SYSTEM]
        Eres un asistente experto en la redacción de Justificaciones de la Necesidad para licitaciones públicas.
        Tu tarea es extraer y estructurar la información proporcionada por el usuario en un formato JSON que cumpla estrictamente con el siguiente esquema Pydantic:

        [SCHEMA]
        {format_instructions}

        [CONTEXTO ADICIONAL]
        Usa esta información para enriquecer los campos, especialmente citas normativas o golden.
        {rag_context}

        [REGLAS]
        - Si algún campo no puede ser inferido, déjalo como nulo/vacío (no inventes datos).
        - Asegúrate de que el JSON sea válido.

        [OUTPUT]
        Devuelve SOLO el objeto JSON. """,
    input_variables=[
        "format_instructions",  # Descripción del esquema Pydantic esperado para la salida JSON.
        "section_specific_instructions",# Instrucciones específicas para la sección actual.
        "rag_context"           # Información adicional recuperada (e.g., de RAG) para enriquecer la respuesta.
    ],
))

human_template_a = HumanMessagePromptTemplate(prompt=PromptTemplate(
    template="Genera la Justificación de la Necesidad con la siguiente información:\n\n{user_input}",
    input_variables=["user_input"], # La entrada del usuario que contiene la información para generar la Justificación de la Necesidad.
))

prompt_a_template = ChatPromptTemplate(
    messages=[
        system_template_a,
        human_template_a,
    ],
    input_variables=[
        "format_instructions",  # Descripción del esquema Pydantic esperado para la salida JSON.
        "rag_context",          # Información adicional recuperada (e.g., de RAG) para enriquecer la respuesta.
        "user_input",           # La entrada del usuario que contiene la información para generar la Justificación de la Necesidad.
        "section_specific_instructions" # Instrucciones específicas para la sección actual.
    ]
)

# --- Binder por sección (schemas UI + inyecciones por JN.x) ---
# Este diccionario contendrá instrucciones o contexto adicional específico para cada sección de la JN.
# Se utilizará para inyectar dinámicamente contenido en los prompts.
PROMPT_PARSER_SLOTS_JN = {
    "JN.1": {"instruction": "Instrucciones adicionales para la sección JN.1: Enfócate en el objeto, alcance y ámbito de la contratación."},
    # Puedes añadir más secciones aquí según sea necesario
}

# --- Prompt B: Redactor técnico-administrativo (dinámico) ---
# Adaptativo a la presencia de citas en los datos estructurados
system_template_b = SystemMessagePromptTemplate(prompt=PromptTemplate(
    template="""[ROLE/SYSTEM]
        Eres un redactor técnico-administrativo.
        Tu tarea es transformar los datos estructurados proporcionados en una narrativa coherente, formal y completa.
        El tono debe ser administrativo y neutro.

        [OBJETIVO]
        Asegúrate de que la narrativa refleje EXACTAMENTE los valores de los campos clave en `structured_data`, especialmente:
        - objeto_contratacion
        - necesidad_y_justificacion
        - alcance.descripcion

        [DATOS ESTRUCTURADOS]
        Se te proporcionarán datos en formato JSON. Debes utilizar TODA la información relevante de estos datos para construir la narrativa.
        Cada campo clave del JSON debe tener una sección clara en la narrativa.

        [REGLAS DE TRANSFORMACIÓN]
        - Cada campo clave (objeto_contratacion, necesidad_y_justificacion, alcance.descripcion) DEBE ser mencionado explícitamente.
        - Asegúrate de que la narrativa refleje fielmente el contenido de los datos estructurados, expandiendo la información cuando sea necesario para darle un formato de prosa.
        - Incluye explícitamente las siguientes citas en secciones dedicadas, si están presentes:
        - Citas Golden: {citas_golden}
        - Citas Normativas: {citas_normativa}

        [OUTPUT]
        Genera la narrativa en formato JSON, donde cada clave sea descriptiva de la sección narrativa (ej. 'objeto_alcance_narrativa').
        Asegúrate de que el JSON de salida sea válido.
        """,
    input_variables=[
        "citas_golden",    # Citas golden a incluir en la narrativa.
        "citas_normativa"  # Citas normativas a incluir en la narrativa.
    ],
))

human_template_b = HumanMessagePromptTemplate(prompt=PromptTemplate(
    template="Genera la narrativa a partir de los siguientes datos:\n\n{structured_data}",
    input_variables=[
        "structured_data"  # Datos estructurados en formato JSON a partir de los cuales se generará la narrativa.
    ],
))

prompt_b_template = ChatPromptTemplate(
    messages=[
        system_template_b,
        human_template_b,
    ],
    input_variables=[
        "structured_data",   # Datos estructurados en formato JSON a partir de los cuales se generará la narrativa.
        "citas_golden",      # Citas golden a incluir en la narrativa.
        "citas_normativa"    # Citas normativas a incluir en la narrativa.
    ]
)
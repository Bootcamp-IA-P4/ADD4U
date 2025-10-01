from langchain_core.prompts import ChatPromptTemplate

# --- Prompt A: Generador de datos estructurados ---
# Este prompt toma la información de entrada y la estructura según el esquema Pydantic.
prompt_a_template = ChatPromptTemplate.from_messages(
    [
        ("system", "Eres un asistente experto en la redacción de Justificaciones de la Necesidad para licitaciones públicas. Tu tarea es extraer y estructurar la información proporcionada por el usuario en un formato JSON que cumpla estrictamente con el siguiente esquema Pydantic:\n\n{format_instructions}\n\nSi algún campo no puede ser inferido de la información proporcionada, déjalo como nulo o vacío según el tipo de dato, pero no inventes información crítica. Asegúrate de que el JSON sea válido y completo según el esquema.\n\n{rag_context}\n\n"),
        ("human", "Genera la Justificación de la Necesidad con la siguiente información:\n\n{user_input}"),
    ]
)

# --- Prompt B: Redactor técnico-administrativo ---
# Este prompt toma los datos estructurados y genera la narrativa final.
prompt_b_template = ChatPromptTemplate.from_messages(
    [
        ("system", "Eres un redactor técnico-administrativo. Tu tarea es transformar los datos estructurados de una Justificación de la Necesidad en una narrativa coherente, formal y profesional. El tono debe ser administrativo y neutro. Cita las fuentes o datos relevantes cuando sea necesario. Genera la narrativa en formato JSON, donde cada sección sea un párrafo o conjunto de párrafos bajo una clave descriptiva (ej. 'objeto_alcance_narrativa', 'contexto_problema_narrativa')."),
        ("human", "Genera la narrativa de la Justificación de la Necesidad a partir de los siguientes datos estructurados:\n\n{structured_data}"),
    ]
)
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# --- Prompt A: Generador de datos estructurados (dinámico) ---
# Adaptativo a la presencia de rag_context y campos específicos
system_template_a = SystemMessagePromptTemplate(prompt=PromptTemplate(
    template="""Eres un asistente experto en la redacción de Justificaciones de la Necesidad para licitaciones públicas. 
    Tu tarea es extraer y estructurar la información proporcionada por el usuario en un formato JSON que cumpla estrictamente con el siguiente esquema Pydantic:
    {format_instructions}
    
    **Contexto adicional (RAG):** {rag_context}
    Usa esta información para enriquecer los campos, especialmente citas normativas o golden.
    
    Si algún campo no puede ser inferido, déjalo como nulo/vacío (no inventes datos). Asegúrate de que el JSON sea válido.
    """,
    input_variables=["format_instructions", "rag_context"],
))

human_template_a = HumanMessagePromptTemplate(prompt=PromptTemplate(
    template="Genera la Justificación de la Necesidad con la siguiente información:\n\n{user_input}",
    input_variables=["user_input"],
))

prompt_a_template = ChatPromptTemplate(
    messages=[
        system_template_a,
        human_template_a,
    ],
    input_variables=["format_instructions", "rag_context", "user_input"]
)

# --- Prompt B: Redactor técnico-administrativo (dinámico) ---
# Adaptativo a la presencia de citas en los datos estructurados
system_template_b = SystemMessagePromptTemplate(prompt=PromptTemplate(
    template="""Eres un redactor técnico-administrativo. 
    Transforma los datos estructurados en una narrativa coherente y formal. 
    El tono debe ser administrativo y neutro. 
    
    **Importante:** Incluye explícitamente las siguientes citas en secciones dedicadas:
    Citas Golden: {citas_golden}
    Citas Normativas: {citas_normativa}
    
    Genera la narrativa en JSON con claves descriptivas (ej. 'objeto_alcance_narrativa').
    """,
    input_variables=["structured_data", "citas_golden", "citas_normativa"],
))

human_template_b = HumanMessagePromptTemplate(prompt=PromptTemplate(
    template="Genera la narrativa a partir de los siguientes datos:\n\n{structured_data}",
    input_variables=["structured_data"],
))

prompt_b_template = ChatPromptTemplate(
    messages=[
        system_template_b,
        human_template_b,
    ],
    input_variables=["structured_data", "citas_golden", "citas_normativa"]
)
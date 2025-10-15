import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate

import json
from backend.models.schemas_jn import OutputJsonA

load_dotenv()

class PromptRefinerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"), # Puedes ajustar el modelo si es necesario
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.3 # Una temperatura más baja para mayor consistencia
        )
        self.refiner_prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate(prompt=PromptTemplate(
                template="""Eres un asistente experto en refinar instrucciones para modelos de lenguaje.
Tu tarea es tomar una instrucción base para una sección específica de un documento, el input del usuario y el contexto RAG, y generar una instrucción más detallada y contextualizada.
El objetivo es que la instrucción refinada ayude a otro LLM a extraer información de manera más precisa y alineada con el contexto proporcionado.

Instrucción Base: {base_section_instruction}
Input del Usuario: {user_input}
Contexto RAG: {rag_context}

Genera una instrucción refinada que sea concisa, clara y que incorpore elementos relevantes del input del usuario y del contexto RAG para guiar la extracción de información en la sección '{section_key}'.
Si el contexto RAG o el input del usuario no aportan información relevante para la instrucción base, simplemente devuelve la instrucción base o una versión ligeramente mejorada de ella.

El JSON de salida debe adherirse estrictamente al siguiente esquema:
```json
{json_schema}
```
""",
                input_variables=["base_section_instruction", "user_input", "rag_context", "section_key", "json_schema"]
            )),
            HumanMessagePromptTemplate(prompt=PromptTemplate(
                template="""Refina la siguiente instrucción para la sección '{section_key}':
Instrucción Base: {base_section_instruction}
Input del Usuario: {user_input}
Contexto RAG: {rag_context}
Instrucción Refinada:""",
                input_variables=["base_section_instruction", "user_input", "rag_context", "section_key"]
            ))
        ])

    async def ainvoke(self, inputs: dict):
        """
        Refina las instrucciones específicas de una sección utilizando un LLM.
        inputs esperados:
        {
          "base_section_instruction": "Instrucción base para la sección JN.1",
          "user_input": "Texto del usuario...",
          "rag_context": "Contexto RAG relevante...",
          "section_key": "JN.1"
        }
        """
        base_section_instruction = inputs.get("base_section_instruction", "")
        user_input = inputs.get("user_input", "")
        rag_context = inputs.get("rag_context", "")
        section_key = inputs.get("section_key", "")

        if not base_section_instruction:
            return {"refined_section_instruction": ""}

        try:
            # Obtener el esquema JSON de OutputJsonA
            output_json_a_schema = json.dumps(OutputJsonA.model_json_schema(), ensure_ascii=False, indent=2)

            prompt_messages = self.refiner_prompt_template.format_messages(
                base_section_instruction=base_section_instruction,
                user_input=user_input,
                rag_context=rag_context,
                section_key=section_key,
                json_schema=output_json_a_schema
            )
            response = await self.llm.ainvoke(prompt_messages)
            return {"refined_section_instruction": response.content, "json_schema": output_json_a_schema}
        except Exception as e:
            print(f"Error refining prompt for section {section_key}: {e}")
            return {"refined_section_instruction": base_section_instruction, "json_schema": output_json_a_schema} # Fallback a la instrucción base
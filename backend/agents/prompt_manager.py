"""
PromptManager
---------------------
Gestiona la construcción de prompts dinámicos para los generadores A y B,
utilizando las plantillas definidas en jn_prompts.py.
"""
from backend.prompts.jn_prompts import prompt_a_template, prompt_b_template
from backend.models.schemas_jn import JustificacionNecesidadStructured
from typing import Optional

class PromptManager:
    def __init__(self, prompt_a_template, prompt_b_template, debug_mode=False):
        self.prompt_a_template = prompt_a_template
        self.prompt_b_template = prompt_b_template
        self.debug_mode = debug_mode

    def extract_citas(self, rag_results):
        """
        Extrae citas golden y normativas de los resultados RAG.
        """
        citas_golden = []
        citas_normativa = []
        for item in rag_results or []:
            if item.get('type') == 'golden':
                citas_golden.append(item.get('content', ''))
            elif item.get('type') == 'normativa':
                citas_normativa.append(item.get('content', ''))
        return citas_golden, citas_normativa

    def format_rag_context(self, rag_results):
        """
        Formatea el contexto RAG como texto plano.
        """
        return '\n'.join([item.get('content', '') for item in rag_results or []])

    def build_prompt_a(self, user_input, format_instructions, rag_results=None, structured_data=None):
        """
        Construye el prompt para el generador A, integrando contexto RAG y citas.
        """
        citas_golden, citas_normativa = self.extract_citas(rag_results)
        rag_context = self.format_rag_context(rag_results)
        prompt = self.prompt_a_template.format(
            user_input=user_input,
            format_instructions=format_instructions,
            rag_context=rag_context,
            structured_data=structured_data or "",
            citas_golden='\n'.join(citas_golden),
            citas_normativa='\n'.join(citas_normativa)
        )
        if self.debug_mode:
            print("Prompt A:", prompt)
        return prompt

    def build_prompt_b(self, user_input, format_instructions, rag_results=None, structured_data=None):
        """
        Construye el prompt para el generador B, integrando contexto RAG y citas.
        """
        citas_golden, citas_normativa = self.extract_citas(rag_results)
        rag_context = self.format_rag_context(rag_results)
        prompt = self.prompt_b_template.format(
            user_input=user_input,
            format_instructions=format_instructions,
            rag_context=rag_context,
            structured_data=structured_data or "",
            citas_golden='\n'.join(citas_golden),
            citas_normativa='\n'.join(citas_normativa)
        )
        if self.debug_mode:
            print("Prompt B:", prompt)
        return prompt

    def set_debug_mode(self, debug):
        """
        Activa o desactiva el modo debug para mostrar los prompts generados.
        """
        self.debug_mode = debug

    async def ainvoke(self, inputs: dict) -> dict:
        """
        inputs esperados:
        {
          "user_input": "Texto del usuario...",
          "format_instructions": "Instrucciones de formato Pydantic para Prompt A",
          "rag_context": "Contexto RAG para Prompt A",
          "structured_data": "Datos estructurados para Prompt B (JSON o dict)",
          "citas_golden": ["cita1", "cita2"], # Opcional, si se extraen antes
          "citas_normativa": ["norma1", "norma2"] # Opcional, si se extraen antes
        }
        """
        user_input = inputs.get("user_input", "")
        format_instructions = inputs.get("format_instructions", "")
        rag_context = inputs.get("rag_context", "")
        structured_data = inputs.get("structured_data", {})
        citas_golden = inputs.get("citas_golden", [])
        citas_normativa = inputs.get("citas_normativa", [])

        # Construir Prompt A
        prompt_a_messages = prompt_a_template.format_messages(
            format_instructions=format_instructions,
            rag_context=rag_context,
            user_input=user_input
        )
        
        # Construir Prompt B
        # Asegurarse de que structured_data sea un diccionario para la plantilla Jinja2
        if isinstance(structured_data, JustificacionNecesidadStructured):
            structured_data_dict = structured_data.model_dump()
        elif isinstance(structured_data, dict):
            structured_data_dict = structured_data
        else:
            structured_data_dict = {} # Fallback

        # Añadir citas al structured_data_dict si existen para que Jinja2 las vea
        if citas_golden:
            structured_data_dict["citas_golden"] = citas_golden
        if citas_normativa:
            structured_data_dict["citas_normativa"] = citas_normativa

        prompt_b_messages = prompt_b_template.format_messages(
            structured_data=structured_data_dict,
            citas_golden='\n'.join(citas_golden),
            citas_normativa='\n'.join(citas_normativa)
        )

        return {
            "prompt_a_messages": prompt_a_messages,
            "prompt_b_messages": prompt_b_messages
        }
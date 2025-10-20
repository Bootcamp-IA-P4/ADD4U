"""
PromptManager
---------------------
Gestiona la construcción de prompts dinámicos para los generadores A y B,
utilizando las plantillas definidas en jn_prompts.py.
"""
from backend.prompts.jn_prompts import prompt_a_template, prompt_b_template, PROMPT_PARSER_SLOTS_JN
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

    def build_prompt_a(self, user_input, section_key: str = None, rag_results=None, section_specific_instructions: str = None, format_instructions: str = None):
        """
        Construye el prompt para el generador A, integrando contexto RAG.
        """
        rag_context = self.format_rag_context(rag_results)
        # Usa la instrucción refinada si se proporciona, de lo contrario, usa la estática
        final_section_instructions = section_specific_instructions if section_specific_instructions is not None else \
                                     PROMPT_PARSER_SLOTS_JN.get(section_key, {}).get("instruction", "")
        prompt_messages = self.prompt_a_template.format_messages(
            user_input=user_input,
            section_specific_instructions=final_section_instructions,
            rag_context=rag_context,
            format_instructions=format_instructions
        )
        if self.debug_mode:
            print("Prompt A Messages:", prompt_messages)
        return prompt_messages

    def build_prompt_b(self, structured_data, citas_golden=None, citas_normativa=None):
        """
        Construye el prompt para el generador B, integrando citas.
        """
        citas_golden = citas_golden or []
        citas_normativa = citas_normativa or []
        prompt_messages = self.prompt_b_template.format_messages(
            structured_data=structured_data,
            citas_golden='\n'.join(citas_golden),
            citas_normativa='\n'.join(citas_normativa)
        )
        if self.debug_mode:
            print("Prompt B Messages:", prompt_messages)
        return prompt_messages

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
          "rag_context": "Contexto RAG para Prompt A",
          "structured_data": "Datos estructurados para Prompt B (JSON o dict)",
          "citas_golden": ["cita1", "cita2"], # Opcional, si se extraen antes
          "citas_normativa": ["norma1", "norma2"] # Opcional, si se extraen antes
          "section_specific_instructions": "Instrucciones refinadas para la sección",
          "json_schema": "Esquema JSON para Prompt A"
        }
        """
        user_input = inputs.get("user_input", "")
        rag_context = inputs.get("rag_context", "")
        structured_data = inputs.get("structured_data", {})
        citas_golden = inputs.get("citas_golden", [])
        citas_normativa = inputs.get("citas_normativa", [])
        section_specific_instructions = inputs.get("section_specific_instructions", None)
        json_schema = inputs.get("json_schema", None)

        # Construir Prompt A
        prompt_a_messages = self.build_prompt_a(
            user_input=user_input,
            rag_results=inputs.get("rag_results"),
            section_specific_instructions=section_specific_instructions,
            format_instructions=json_schema
        )
        
        # Construir Prompt B
        # Asegurarse de que structured_data sea un diccionario para la plantilla Jinja2
        if isinstance(structured_data, JustificacionNecesidadStructured):
            structured_data_dict = structured_data.model_dump()
        elif isinstance(structured_data, dict):
            structured_data_dict = structured_data
        else:
            structured_data_dict = {} # Fallback

        prompt_b_messages = self.build_prompt_b(
            structured_data=structured_data_dict,
            citas_golden=citas_golden,
            citas_normativa=citas_normativa
        )

        return {
            "prompt_a_messages": prompt_a_messages,
            "prompt_b_messages": prompt_b_messages
        }
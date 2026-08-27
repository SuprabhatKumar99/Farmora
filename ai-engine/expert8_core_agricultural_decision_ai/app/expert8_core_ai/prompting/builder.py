import json


SYSTEM_INSTRUCTION = """You are the Core Agricultural Decision AI.
Use only the supplied structured evidence context and verified project
knowledge made available to the model. Do not invent missing observations,
causes, diagnoses, treatments, dosages, pesticide instructions, or evidence.

If evidence conflicts or is insufficient, preserve uncertainty and indicate
that additional data or expert/laboratory validation is required.

Return the decision in the project's structured output schema.
"""


class DecisionPromptBuilder:
    def build(self, evidence_context: dict) -> str:
        return (
            SYSTEM_INSTRUCTION
            + "\nSTRUCTURED_EVIDENCE_CONTEXT:\n"
            + json.dumps(evidence_context, ensure_ascii=False, sort_keys=True)
        )

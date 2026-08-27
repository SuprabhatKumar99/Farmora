import json


class DecisionOutputParser:
    """Parse model output into a JSON-compatible decision object.

    The supplied model should be trained/instructed to emit the project
    decision schema. No semantic agricultural facts are fabricated here.
    """

    def parse(self, raw_output: str) -> dict:
        text = raw_output.strip()

        if text.startswith("```"):
            lines = text.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines).strip()

        data = json.loads(text)

        if not isinstance(data, dict):
            raise ValueError("MODEL_OUTPUT_MUST_BE_OBJECT")

        return data

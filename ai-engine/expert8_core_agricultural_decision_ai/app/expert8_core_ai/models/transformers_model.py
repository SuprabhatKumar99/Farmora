from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .base import AgriculturalDecisionModel


class LocalCausalLM(AgriculturalDecisionModel):
    """Adapter for a supplied local Hugging Face causal language model.

    The exact model, tokenizer, prompt contract, and decoding settings must
    match the supplied artifact. This class provides the loading/execution
    mechanism; it does not claim a model was trained when none was supplied.
    """

    def __init__(
        self,
        model_path: str,
        name: str = "user_provided_agricultural_decision_model",
        version: str = "provided",
        device: str | None = None,
        max_new_tokens: int = 512,
    ):
        self.model_path = Path(model_path)
        self.name = name
        self.version = version
        self.device = device or (
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.max_new_tokens = max_new_tokens
        self.tokenizer = None
        self.model = None

    def load(self):
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model directory not found: {self.model_path}"
            )

        self.tokenizer = AutoTokenizer.from_pretrained(
            str(self.model_path)
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            str(self.model_path),
            torch_dtype=(
                torch.float16
                if self.device == "cuda"
                else torch.float32
            ),
        )
        self.model.to(self.device)
        self.model.eval()

    def predict(self, prompt: str) -> str:
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("MODEL_NOT_LOADED")

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
        ).to(self.device)

        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,
            )

        generated = outputs[0][inputs["input_ids"].shape[1]:]
        return self.tokenizer.decode(
            generated,
            skip_special_tokens=True,
        )

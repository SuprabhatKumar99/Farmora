from .transformers_model import LocalCausalLM


class DecisionModelLoader:
    def load_huggingface(
        self,
        model_path,
        name="user_provided_agricultural_decision_model",
        version="provided",
        device=None,
        max_new_tokens=512,
    ):
        model = LocalCausalLM(
            model_path=model_path,
            name=name,
            version=version,
            device=device,
            max_new_tokens=max_new_tokens,
        )
        model.load()
        return model

from .pytorch_model import TorchScriptPreventionIPMModel


class PreventionIPMModelLoader:
    def load_torchscript(
        self,
        model_path,
        name="user_provided_prevention_ipm_model",
        version="provided",
        task="RECOMMENDATION",
        device=None,
    ):
        model = TorchScriptPreventionIPMModel(
            model_path=model_path,
            name=name,
            version=version,
            task=task,
            device=device,
        )
        model.load()
        return model

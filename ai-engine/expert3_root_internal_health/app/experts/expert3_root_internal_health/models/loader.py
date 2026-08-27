from .pytorch_model import TorchScriptRootInternalHealthModel


class RootInternalHealthModelLoader:
    def load_torchscript(
        self,
        model_path,
        name="user_provided_root_internal_health_model",
        version="provided",
        task="CLASSIFICATION",
        device=None,
    ):
        model = TorchScriptRootInternalHealthModel(
            model_path=model_path,
            name=name,
            version=version,
            task=task,
            device=device,
        )
        model.load()
        return model

from .pytorch_model import TorchScriptWholeCropHealthModel


class WholeCropHealthModelLoader:
    def load_torchscript(
        self,
        model_path,
        name="user_provided_whole_crop_health_model",
        version="provided",
        task="CLASSIFICATION",
        device=None,
    ):
        model = TorchScriptWholeCropHealthModel(
            model_path=model_path,
            name=name,
            version=version,
            task=task,
            device=device,
        )
        model.load()
        return model

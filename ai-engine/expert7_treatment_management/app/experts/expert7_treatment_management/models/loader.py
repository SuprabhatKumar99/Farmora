from .pytorch_model import TorchScriptTreatmentManagementModel


class TreatmentManagementModelLoader:
    def load_torchscript(
        self,
        model_path,
        name="user_provided_treatment_management_model",
        version="provided",
        task="RECOMMENDATION",
        device=None,
    ):
        model = TorchScriptTreatmentManagementModel(
            model_path=model_path,
            name=name,
            version=version,
            task=task,
            device=device,
        )
        model.load()
        return model

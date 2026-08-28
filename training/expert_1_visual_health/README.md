# Expert 1 — Visual Health

Modular training package for Expert 1 of the Crop Health Intelligence MoE.

## Design principles
- Preserves the project's canonical 01–11 dataset structure.
- Expert 1 adds its own modular code under `expert_1_visual_health/`.
- Existing datasets are referenced by path/IDs; raw data is not duplicated.
- Supports classification, detection/segmentation, severity estimation, inference, evaluation, and structured evidence output.
- Farm/case-aware splitting is used to reduce temporal/farm leakage.

## Expected canonical dataset
See `DATASET_CONTRACT.md` and the supplied project dataset specification.

## Start
1. Put/keep canonical data under the 01–11 directories.
2. Run `python -m expert_1_visual_health.data_pipeline.prepare_dataset`.
3. Train the desired task using the task module.
4. Run evaluation.
5. Export structured Expert 1 outputs for Evidence Fusion.

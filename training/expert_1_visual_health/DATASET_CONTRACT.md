# Dataset Contract — Expert 1

The canonical project structure remains:

01_crop_knowledge/
02_disease_pest_knowledge/
03_farm/
04_observations/
05_environment/
06_remote_sensing/
07_disease_events/
08_moe/
09_decision/
10_validation/
11_followup/

Expert 1 primarily consumes:
- 04_observations/images/
- 04_observations/videos/
- 04_observations/image_metadata.csv
- 04_observations/video_metadata.csv
- 04_observations/annotations.csv
- supporting crop/disease/farm/validation records.

Key IDs must be preserved:
farm_id, zone_id, crop_id, variety_id, case_id, image_id, timestamp.

Do not randomly split correlated images from the same farm/case across train and test.

# Crop Health Intelligence — Dataset Structure

```text
crop_health_dataset/
│
├── 01_crop_knowledge/
│   ├── crops.csv
│   ├── varieties.csv
│   ├── growth_stages.csv
│   ├── crop_lifecycle.csv
│   └── crop_requirements.csv
│
├── 02_disease_pest_knowledge/
│   ├── diseases.csv
│   ├── pests.csv
│   ├── symptoms.csv
│   ├── disease_progression.csv
│   ├── disease_conditions.csv
│   └── management.csv
│
├── 03_farm/
│   ├── farms.csv
│   ├── fields.csv
│   ├── zones.csv
│   └── crop_cycles.csv
│
├── 04_observations/
│   ├── images/
│   ├── videos/
│   ├── image_metadata.csv
│   ├── video_metadata.csv
│   ├── annotations.csv
│   └── field_observations.csv
│
├── 05_environment/
│   ├── weather.csv
│   ├── weather_forecast.csv
│   ├── soil.csv
│   ├── sensor_readings.csv
│   └── pest_traps.csv
│
├── 06_remote_sensing/
│   ├── satellite_images/
│   ├── drone_images/
│   ├── remote_sensing_metadata.csv
│   └── vegetation_indices.csv
│
├── 07_disease_events/
│   ├── disease_cases.csv
│   ├── disease_progression.csv
│   ├── affected_zones.csv
│   └── severity_records.csv
│
├── 08_moe/
│   ├── expert_outputs.csv
│   ├── evidence.csv
│   ├── expert_confidence.csv
│   └── expert_disagreements.csv
│
├── 09_decision/
│   ├── orchestrator_decisions.csv
│   ├── risk_scores.csv
│   └── recommendations.csv
│
├── 10_validation/
│   ├── expert_validation.csv
│   ├── laboratory_results.csv
│   └── ground_truth.csv
│
└── 11_followup/
    ├── followup_observations.csv
    ├── treatment_actions.csv
    ├── treatment_outcomes.csv
    └── model_feedback.csv
```

---

## 1. Crop Knowledge

### `crops.csv`

```csv
crop_id,crop_name,scientific_name,family,lifecycle
C001,Tomato,Solanum lycopersicum,Solanaceae,Annual
```

### `varieties.csv`

```csv
variety_id,crop_id,variety_name,maturity_days,disease_susceptibility
V001,C001,Variety_A,90,Medium
```

### `growth_stages.csv`

```csv
stage_id,crop_id,stage_name,start_day,end_day,expected_features
GS01,C001,Germination,0,10,...
GS02,C001,Vegetative,11,40,...
GS03,C001,Flowering,41,55,...
GS04,C001,Fruiting,56,75,...
GS05,C001,Maturity,76,90,...
```

### `crop_requirements.csv`

```csv
crop_id,variety_id,temperature_min,temperature_max,humidity_min,humidity_max,soil_moisture_min,soil_moisture_max
C001,V001,...,...,...,...,...,...
```

---

# 2. Disease & Pest Knowledge

### `diseases.csv`

```csv
disease_id,disease_name,crop_id,pathogen_type,pathogen_name,affected_parts,typical_stage
D001,Late_Blight,C001,Fungus,...,Leaf|Stem|Fruit,Fruiting
```

### `pests.csv`

```csv
pest_id,pest_name,crop_id,affected_parts,typical_stage
P001,Example_Pest,C001,Leaf|Fruit,Fruiting
```

### `symptoms.csv`

```csv
symptom_id,disease_id,crop_id,plant_part,symptom_type,color,pattern,severity_stage,description
S001,D001,C001,Leaf,Lesion,Brown,Irregular,Early,...
```

This dataset is particularly important for **early detection**, because you want to record **early-stage symptoms**, not only severe symptoms.

---

# 3. Farm Dataset

### `farms.csv`

```csv
farm_id,location,latitude,longitude,area_hectares,soil_type
F001,Location_A,...,...,2.5,Loamy
```

### `zones.csv`

```csv
zone_id,farm_id,zone_number,area_m2,latitude,longitude
Z001,F001,1,400,...,...
Z002,F001,2,400,...,...
```

### `crop_cycles.csv`

```csv
cycle_id,farm_id,zone_id,crop_id,variety_id,sowing_date,expected_harvest_date,current_stage
CC001,F001,Z001,C001,V001,2026-06-01,2026-09-01,Fruiting
```

This connects your **farm → zone → crop → growth stage**.

---

# 4. Image Dataset

```text
04_observations/
└── images/
    ├── healthy/
    ├── early_disease/
    ├── moderate_disease/
    ├── severe_disease/
    ├── pest/
    └── chemical_damage/
```

### `image_metadata.csv`

```csv
image_id,file_path,farm_id,zone_id,crop_id,variety_id,growth_stage,plant_part,capture_date,source,disease_id,severity,validation_status
IMG001,images/early_disease/IMG001.jpg,F001,Z001,C001,V001,Fruiting,Leaf,2026-08-20,Smartphone,D001,Mild,Expert_Verified
```

---

# 5. Image Annotation Dataset

For object detection/segmentation:

### `annotations.csv`

```csv
annotation_id,image_id,object_type,class_name,x_min,y_min,x_max,y_max,segmentation_mask,annotator
A001,IMG001,Disease_Lesion,Late_Blight,120,80,250,190,...,Expert_01
A002,IMG001,Pest,Example_Pest,300,150,360,220,...,Expert_01
```

This is what you need for **YOLO/object detection or segmentation models**.

---

# 6. Video Dataset

### `video_metadata.csv`

```csv
video_id,file_path,farm_id,zone_id,crop_id,growth_stage,capture_date,duration,source,disease_id,pest_id
VID001,videos/VID001.mp4,F001,Z001,C001,Fruiting,2026-08-20,20,Smartphone,D001,
```

You can later extract frames and associate them with disease progression.

---

# 7. Weather Dataset

### `weather.csv`

```csv
location_id,timestamp,temperature,humidity,rainfall,wind_speed,solar_radiation,leaf_wetness
LOC001,2026-08-20T10:00,29.5,88,4.2,7.1,...,...
```

### `weather_forecast.csv`

```csv
location_id,forecast_time,temperature,humidity,rainfall,wind_speed
LOC001,2026-08-21T10:00,30.2,91,8.4,6.8
```

The historical weather + forecast combination feeds your **Environmental Expert** and **Risk Engine**.

---

# 8. Sensor Dataset

### `sensor_readings.csv`

```csv
sensor_id,farm_id,zone_id,timestamp,temperature,humidity,soil_moisture,soil_temperature,ph,ec
S001,F001,Z001,2026-08-20T10:00,29.5,88,72,27.2,6.4,1.2
```

---

# 9. Pest Trap Dataset

### `pest_traps.csv`

```csv
trap_id,farm_id,zone_id,timestamp,pest_id,count,trap_type,verified
T001,F001,Z001,2026-08-20T10:00,P001,21,Sticky,Yes
```

This gives you a time series:

```text
Day 1 → 4 pests
Day 2 → 7 pests
Day 3 → 12 pests
Day 4 → 21 pests
```

which can become an early-warning signal.

---

# 10. Drone/Satellite Dataset

### `remote_sensing_metadata.csv`

```csv
remote_image_id,farm_id,zone_id,capture_date,sensor_type,resolution,image_path
RS001,F001,Z001,2026-08-20,Drone,5cm,drone/RS001.jpg
```

### `vegetation_indices.csv`

```csv
remote_image_id,zone_id,ndvi,ndre,evi,vegetation_health,anomaly_score
RS001,Z001,0.42,0.31,0.38,Low,0.81
```

This feeds your:

**Whole Farm → Zone → Anomaly Detection**

pipeline.

---

# 11. Disease Case Dataset

### `disease_cases.csv`

```csv
case_id,farm_id,zone_id,crop_id,variety_id,growth_stage,first_observed_date,first_detected_date,suspected_disease,confirmed_disease,severity,affected_area_m2
CASE001,F001,Z001,C001,V001,Fruiting,2026-08-18,2026-08-19,D001,D001,Moderate,120
```

This dataset is extremely valuable because you can calculate:

> **How much earlier did our system detect the disease compared with normal observation?**

---

# 12. Disease Progression Dataset

### `disease_progression.csv`

```csv
case_id,timestamp,health_score,symptom_score,severity_score,vegetation_score,pest_count,environmental_risk
CASE001,2026-08-18,94,10,5,0.71,4,35
CASE001,2026-08-19,89,18,10,0.66,7,55
CASE001,2026-08-20,78,32,20,0.58,12,72
CASE001,2026-08-21,65,51,35,0.47,21,86
```

This is one of the most important datasets for your **early-warning model**.

---

# 13. MoE Expert Dataset

### `expert_outputs.csv`

```csv
case_id,expert_id,expert_type,prediction,probability,evidence,timestamp
CASE001,E01,Visual,Late_Blight,0.91,"Dark lesions",...
CASE001,E02,Chemical,Chemical_Injury,0.12,"No typical burn pattern",...
CASE001,E05,Environmental,Fungal_Risk,0.88,"High humidity",...
```

Your experts can therefore disagree, and the orchestrator can reason over that disagreement.

---

# 14. Evidence Dataset

### `evidence.csv`

```csv
evidence_id,case_id,source_type,source_id,feature,value,importance,expert_id
EV001,CASE001,Image,IMG001,Leaf_Lesion,Detected,High,E01
EV002,CASE001,Weather,LOC001,Humidity,88,High,E05
EV003,CASE001,PestTrap,T001,Pest_Count,21,Medium,E05
```

This makes your system more **explainable**.

---

# 15. Risk Dataset

### `risk_scores.csv`

```csv
risk_id,case_id,zone_id,disease_id,timestamp,risk_score,risk_level,main_factors
R001,CASE001,Z001,D001,2026-08-20,86,High,"Humidity|Rainfall|CropStage|Anomaly"
```

This is the output of your **Early Risk Engine**.

---

# 16. Orchestrator Decision Dataset

### `orchestrator_decisions.csv`

```csv
decision_id,case_id,final_diagnosis,confidence,severity,risk_score,affected_zone,validation_required,decision
DEC001,CASE001,D001,0.92,Moderate,86,Z001,No,Immediate_IPM
```

---

# 17. Recommendation Dataset

### `recommendations.csv`

```csv
recommendation_id,case_id,recommendation_type,priority,action,source,language
REC001,CASE001,Prevention,High,"Inspect affected zone",KnowledgeBase,English
REC002,CASE001,IPM,High,"Apply recommended IPM measure",ExpertValidated,English
```

Keep **prevention, monitoring, biological/mechanical/cultural controls, chemical management, and referral** as separate recommendation categories.

---

# 18. Expert/Laboratory Validation

### `expert_validation.csv`

```csv
validation_id,case_id,validator_type,initial_prediction,confirmed_diagnosis,confidence,validation_date,notes
VAL001,CASE001,Agricultural_Expert,D001,D001,0.97,2026-08-21,...
```

### `laboratory_results.csv`

```csv
lab_id,case_id,sample_id,test_type,result,confirmed_disease,test_date
LAB001,CASE001,SAMPLE001,Pathogen_Test,Positive,D001,2026-08-22
```

This becomes your **ground truth**.

---

# 19. Follow-up Dataset

### `followup_observations.csv`

```csv
followup_id,case_id,date,image_id,health_score,symptom_score,severity,outcome
FU001,CASE001,2026-08-24,IMG009,81,20,Low,Improved
```

### `treatment_outcomes.csv`

```csv
case_id,action_id,action_date,outcome_date,outcome,health_change,expert_confirmed
CASE001,A001,2026-08-21,2026-08-24,Improved,+18,Yes
```

This closes your learning loop.

---

# 20. Final Dataset Relationships

```text
                         ┌──────────────┐
                         │     CROP     │
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │   VARIETY    │
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │ GROWTH STAGE │
                         └──────┬───────┘
                                │
              ┌─────────────────▼─────────────────┐
              │               FARM                │
              └─────────────────┬─────────────────┘
                                │
                         ┌──────▼───────┐
                         │     ZONE     │
                         └──────┬───────┘
                                │
       ┌────────────────────────┼────────────────────────┐
       │                        │                        │
       ▼                        ▼                        ▼
    Images                  Weather                 Sensors
       │                        │                        │
       ▼                        ▼                        ▼
  Video/Pests              Environment             Soil/Trap
       │                        │                        │
       └────────────────────────┼────────────────────────┘
                                ▼
                         ┌──────────────┐
                         │   ANOMALY    │
                         └──────┬───────┘
                                ▼
                         ┌──────────────┐
                         │  RISK SCORE  │
                         └──────┬───────┘
                                ▼
                         ┌──────────────┐
                         │     MoE      │
                         └──────┬───────┘
                                ▼
                       ┌─────────────────┐
                       │ EVIDENCE FUSION │
                       └────────┬────────┘
                                ▼
                       ┌─────────────────┐
                       │  ORCHESTRATOR   │
                       └────────┬────────┘
                                ▼
                         DIAGNOSIS +
                       RECOMMENDATION
                                │
                                ▼
                         EXPERT / LAB
                         VALIDATION
                                │
                                ▼
                           FOLLOW-UP
                                │
                                ▼
                       GROUND TRUTH /
                         MODEL UPDATE
```


**The key is to preserve the relationships between them using IDs** such as `farm_id`, `zone_id`, `crop_id`, `case_id`, `image_id`, and `timestamp`. That's reconstruct the complete story of a crop from **planting → monitoring → anomaly → disease → intervention → recovery**
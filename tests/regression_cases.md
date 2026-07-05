# Regression Cases — v0.6.1 Execution-Controlled System

Each case must include risk level, expected structure_score, and expected layout_type.

| Case | risk level | expected structure_score | expected layout_type | Expected control behavior |
|---|---:|---:|---|---|
| 一个人住收纳 | SAFE | >=88 | single_scene_editorial | allow image_gen under SAFE |
| 学习方法 | SAFE | >=88 | title_scene_bullets | allow image_gen under SAFE |
| 情绪管理 | WARNING | 70-84 before repair, >=85 after repair | single_scene_editorial | repair once |
| 房间整理 | WARNING | 70-84 before repair, >=85 after repair | title_scene_bullets | reduce props |
| 补课无效 | SAFE | >=88 | single_scene_editorial | one character, one workbook |
| 信息压缩类内容 | WARNING | >=85 after grouping | list_scene_hybrid | group text, limit props |
| 多步骤清单类 | WARNING | >=85 after grouping | title_scene_bullets | bullets ≤ 5 |
| 习惯养成 | SAFE | >=88 | title_scene_bullets | checklist + static pose |
| 方法论内容 | WARNING | >=85 after layout selection | title_object_ring | abstract content becomes title/object ring |
| 认知类内容 | WARNING | >=85 after simplification | title_object_ring | avoid multi-scene metaphor overload |

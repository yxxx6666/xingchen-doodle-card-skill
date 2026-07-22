# Runtime Tests v0.8.10

| Case | Expected |
|---|---|
| 1086x1448 | PASS ratio |
| 1080x1440 | PASS ratio |
| 1536x2048 | PASS ratio, not fixed-size |
| 768x1024 | PASS ratio |
| 1024x1536 | FAIL ratio |
| no OPENAI_API_KEY | PASS preflight |
| user says 1536x2048 ratio | interpret as 3:4 ratio only |

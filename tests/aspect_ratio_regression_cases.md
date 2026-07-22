# Aspect Ratio Regression Cases v0.8.10

## Pass

- 1086x1448
- 1080x1440
- 1536x2048
- 768x1024

All pass because width/height is 0.75. None creates a fixed-pixel requirement.

## Fail

- 1024x1536
- 1080x1920
- 1200x1500

Failure action: discard and regenerate the same page. No repair.

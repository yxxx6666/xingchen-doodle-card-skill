# Aspect Ratio Lock v0.8.10

`3:4` describes a relationship between width and height. It does not prescribe a fixed pixel size.

Valid 3:4 examples include:

- `1086x1448`
- `1080x1440`
- `1536x2048`
- `768x1024`

The only hard acceptance rule is:

```text
abs(actual_width / actual_height - 0.75) <= 0.001
```

`1024x1536` is 2:3 and must fail.

Do not infer exact pixels from a ratio request. Do not use external APIs or post-processing to force dimensions.

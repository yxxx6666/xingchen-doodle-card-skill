# encoding_guard — v0.8.10 Encoding and Text Integrity Guard

Purpose: prevent Chinese mojibake, metadata corruption, text loss, and prompt encoding error.

## Mandatory rules

- 全系统 UTF-8 强制锁定
- SKILL.md / README.md / metadata 必须一致编码
- 所有中文文本必须可读验证
- prompt 中文必须保留
- image_gen text 必须可解析

## Installation gate

```text
IF any file encoding != UTF-8:
  BLOCK installation
  REQUIRE repair
```

## Text validation

- SKILL.md 中文必须完整
- README.md 中文必须完整
- prompt 中文必须保留
- metadata corruption must block installation
- image_gen text must be parseable as UTF-8

## Controller integration

```text
IF encoding_guard FAIL:
  STOP SYSTEM
```

The encoding_guard must run before content_graph construction.

## Production target

```text
encoding safety before pipeline
```

## Explicit corruption risks

The encoding_guard prevents 中文乱码, metadata corruption, 文本丢失, and prompt encoding error.

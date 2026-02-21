# `/tests` AGENTS.md

## Context

Test harness directory. Testing primarily is done using `pytest`.

## Rules

- When fixing issues or developing new features, implement matching tests.
- Keep tests isolated utilizing pure unit approaches (like mocking `google-genai` clients on embedder testing) or isolated setup/teardowns for DB logic depending on depth.
- Mirror the `src` folder structure here to make tracking tests straightforward.

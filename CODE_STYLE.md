# Duck Native Code Style Guide

> This guide applies specifically to the Duck codebase (tourist destination finder app) and must be strictly followed by every contributor on that project.

## Everything you neeed to know

> Please refer to Duck's [CODE STYLE GUIDE](https://github.com/duckframework/duck/blob/main/ai/CODE_STYLE_GUIDE.md)

## Use of AI assistance

AI is permitted to be used in this codebase but it must not disrupt the code structure, rules, performance and security. For best 
results, Claude Code is recommended. Please refer to these [AI Guides](https://github.com/duckframework/duck/blob/main/ai).

## Final Checklist

Before completing code:

- Does it follow existing project patterns?
- Are docstrings present and Google-style?
- Are comments present and do they clearly separate distinct operations (variables, calls, component updates)?
- Is spacing consistent (blank lines between definitions and logical blocks, no compressed code)?
- Are names clear and unambiguous?
- Is there duplicated functionality?
- Are there unnecessary variables or functions?
- Are configuration values (colors, spacing, URLs) centralized in `components/theme.py`
- Is the code easy for another contributor to understand at a glance?

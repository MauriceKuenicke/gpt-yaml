<p align="center">
    <em>Defining Open AI Prompts using YAML Syntax.</em>
</p>

---

**Documentation**: <a href="https://mauricekuenicke.github.io/gpt-yaml/" target="_blank">https://mauricekuenicke.github.io/gpt-yaml/</a>

**Source Code**: <a href="https://github.com/MauriceKuenicke/gpt-yaml" target="_blank">https://github.com/MauriceKuenicke/gpt-yaml</a>

---

Use YAML files to store and manage your Open AI prompts.

---
## ⚠️ Important
This project is in very early development and currently not safe for use in a production environment. Use at your own risk.


## Example 

```yaml
# chat_completion.yaml
model: "gpt-3.5-turbo"
settings:
  top_p: 1
  temperature: 1
  choices: 1
prompt:
  system: You are a helpful assistant.
  context:
    - Who won the world series in 2020?
    - The Los Angeles Dodgers won the World Series in 2020.
  message: Where was it played?
```

```Python
from gptyaml.prompts import ChatCompletionPrompt
import openai

prompt = ChatCompletionPrompt.from_file("chat_completion.yaml")

# Use the configuration directly from the prompt instance
openai.ChatCompletion.create(**prompt.cfg)

# or extract single values
model = prompt.model
messages = prompt.messages
openai.ChatCompletion.create(model=model, messages=messages)
```
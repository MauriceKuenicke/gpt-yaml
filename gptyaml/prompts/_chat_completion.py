from schema import Schema, And, Use, Optional
import yaml
from typing import Any

# Model endpoint compatibility:
# https://platform.openai.com/docs/models/model-endpoint-compatibility
available_models = [
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-32k",
    "gpt-4-32k-0314",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
]

setting_schema = Schema(
    {
        Optional("temperature", default=1): And(
            Use(float), Use(float), lambda i: 0 <= i <= 2
        ),
        Optional("top_p", default=1): And(
            Use(float), Use(float), lambda i: 0 <= i <= 1
        ),
        Optional("choices", default=1): And(Use(int), lambda i: i > 0),
    },
)

prompt_schema = Schema(
    {
        "model": And(str, Use(str.lower), lambda s: s in available_models),
        Optional("settings", default=setting_schema.validate({})): setting_schema,
        "prompt": {
            Optional("system"): And(str),
            Optional("context"): And(list),
            "message": And(str),
        },
    }
)


class ChatCompletionPrompt:
    """Prompt Configuration for Chat Completions Requests to the API."""

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Initialize the ChatCompletionPrompt object.

        Args:
        - config (dict): A dictionary object containing prompt configuration data.

        Returns:
        - None.

        """
        self.config = prompt_schema.validate(config)
        self.model = self.config["model"]

    @classmethod
    def _load_yaml_config(cls, file_path: str) -> dict[str, Any]:
        """
        Load a YAML configuration file.

        Args:
        - file_path (str): A string representing the path to
        the YAML configuration file.

        Returns:
        - raw_config (dict): A dictionary object containing the
        loaded YAML configuration data.

        """
        with open(file_path, "r") as stream:
            raw_config: dict[str, Any] = yaml.safe_load(stream)
        return raw_config

    @classmethod
    def from_file(cls, yaml_path: str) -> "ChatCompletionPrompt":
        """
        Create a ChatCompletionPrompt object from a YAML configuration file.

        Args:
        - yaml_path (str): A string representing the path to
        the YAML configuration file.

        Returns:
        - chat_completion_prompt (ChatCompletionPrompt): A ChatCompletionPrompt object
        created from the YAML configuration data.

        """
        config = cls._load_yaml_config(yaml_path)
        return ChatCompletionPrompt(config)

    @property
    def cfg(self) -> dict[str, Any]:
        """
        Return a dictionary object containing the configuration data.

        Args:
        - self (ChatCompletionPrompt): The class instance.

        Returns:
        - config_dict (dict): A dictionary object containing the configuration data.

        """
        return {
            "model": self.model,
            "messages": self._messages(),
            "top_p": self.config["settings"]["top_p"],
            "temperature": self.config["settings"]["temperature"],
            "choices": self.config["settings"]["choices"],
        }

    @property
    def messages(self) -> list[dict[str, Any]]:
        """
        Return a list of messages based on the prompt configuration.

        Args:
        - self (ChatCompletionPrompt): The class instance.

        Returns:
        - messages (list): A list of messages.

        """
        return self._messages()

    def _messages(self) -> list[dict[str, Any]]:
        messages = []
        prompt_config = self.config["prompt"]
        if "system" in prompt_config.keys():
            entry = {"role": "system", "content": prompt_config["system"]}
            messages.append(entry)

        if "context" in prompt_config.keys():
            for cnt, msg in enumerate(prompt_config["context"]):
                if cnt % 2 == 0:
                    role = "user"
                else:
                    role = "assistant"
                messages.append({role: msg})

        messages.append({"role": "user", "content": prompt_config["message"]})
        return messages

from gptyaml.prompts import ChatCompletionPrompt
import pytest


@pytest.fixture
def test_files_base_dir() -> str:
    """Base Directory for the test files."""
    return "tests/files/"


def test_load_config_successfull(test_files_base_dir: str) -> None:
    """Test a successfull load from a yaml file."""
    prompt = ChatCompletionPrompt.from_file(
        test_files_base_dir + "chat_completion_base.yaml"
    )

    print(prompt.cfg)
    assert prompt


def test_load_invalid_config_throws_exception(test_files_base_dir: str) -> None:
    """Loading an invalid config will raise an exception."""
    with pytest.raises(Exception):
        ChatCompletionPrompt.from_file(
            test_files_base_dir + "chat_completion_invalid.yaml"
        )

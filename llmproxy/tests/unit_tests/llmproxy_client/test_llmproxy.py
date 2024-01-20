from llmproxy.llmproxy import (
    _get_settings_from_yml,
    _setup_available_models,
    _setup_user_models,
)
import pytest

import os

from llmproxy.llmproxy import LLMProxy


CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

proxy_client = LLMProxy(
    path_to_user_configuration="llmproxy.config.yml",
)


# TODO: FIX
def test_empty_model() -> None:
    with pytest.raises(Exception, match="No models provided in llmproxy.config.yml"):
        settings = _get_settings_from_yml(
            path_to_yml=f"{CURRENT_DIRECTORY}/empty_model_test.yml"
        )
        available_model = _setup_available_models(settings=settings)
        user_model = _setup_user_models(
            settings=settings, available_models=available_model
        )


def test_invalid_model() -> None:
    with pytest.raises(Exception, match="test is not available"):
        settings = _get_settings_from_yml(
            path_to_yml=f"{CURRENT_DIRECTORY}/invalid_model_test.yml"
        )
        available_model = _setup_available_models(settings=settings)
        user_model = _setup_user_models(
            settings=settings, available_models=available_model
        )


# TODO: ADD TEST
def test_get_settings_from_yml() -> None:
    user_setting = _get_settings_from_yml(path_to_yml="llmproxy.config.yml")
    setting = _get_settings_from_yml(path_to_yml="llmproxy/config/internal.config.yml")


# TODO: ADD TEST
def test_setup_available_models() -> None:
    settings = _get_settings_from_yml(path_to_yml="llmproxy/config/internal.config.yml")
    available_model = _setup_available_models(settings=settings)


# TODO: ADD TEST
def test_setup_user_models() -> None:
    settings = _get_settings_from_yml(path_to_yml="llmproxy.config.yml")
    dev_setting = _get_settings_from_yml(
        path_to_yml="llmproxy/config/internal.config.yml"
    )
    available_model = _setup_available_models(settings=dev_setting)
    user_model = _setup_user_models(settings=settings, available_models=available_model)


# TODO: More of an integration test, move later
# TODO: figure out a way for the tests to be routed to the .env.test
def test_cost_routing() -> None:
    # Arrange
    prompt = "I am a man, not a man, but not a man, that is an apple, or a banana!"

    print(CURRENT_DIRECTORY)
    proxy_client = LLMProxy(
        path_to_user_configuration=f"{CURRENT_DIRECTORY}/test.yml",
        path_to_env_vars=".env.test",
    )

    # Act
    output = proxy_client.route(route_type="cost", prompt=prompt)
    # Assert
    assert "that is an apple" in output.response

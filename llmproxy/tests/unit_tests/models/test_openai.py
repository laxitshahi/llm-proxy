import os

from dotenv import load_dotenv
from llmproxy.models.openai import OpenAI
from openai import error
from unittest.mock import patch

load_dotenv(".env.test")

openai_api_key = os.getenv("OPENAI_API_KEY")

def test_invalid_temperature():
    chatbot = OpenAI(api_key = openai_api_key, temp=-1)
    response = chatbot.get_completion()
    assert isinstance(response.err, str)
    assert "temperature" in response.message.lower()

def test_invalid_api_key():
    chatbot = OpenAI(api_key="invalid_key2")
    response = chatbot.get_completion()
    assert isinstance(response.err, str)
    assert "incorrect api key provided" in response.message.lower()

def test_unsupported_model():
    chatbot = OpenAI(api_key=openai_api_key, model="unsupported_model")
    response = chatbot.get_completion()
    assert response.err == "ValueError"
    assert response.message == "Model not supported"

def test_generic_exception():
    with patch('openai.ChatCompletion.create', side_effect=Exception("Random error")):
        chatbot = OpenAI(api_key = openai_api_key)
        try:
            chatbot.get_completion()
        except Exception as e:
            assert str(e) == "Unknown Error"

def test_openai_rate_limit_error():
    with patch('openai.ChatCompletion.create', side_effect=error.OpenAIError("Rate limit exceeded")):
        chatbot = OpenAI(api_key = openai_api_key)
        response = chatbot.get_completion()
        assert response.err == "OpenAIError"
        assert "rate limit exceeded" in response.message.lower()
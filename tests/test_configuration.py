import pytest
from assistant.configuration import (
    ConfigurationInvalide,
    DEFAULT_MODEL,
    charger_configuration,
)

# Using monkeypatch feature from pytest
# Allows you to mock modules / environments, in our case using it to mock env variables
# See : https://docs.pytest.org/en/stable/how-to/monkeypatch.html


# TEST charger_configuration()
def test_charger_configuration_valid_default_model(monkeypatch):
    """Check empty model defaults to our constant DEFAULT_MODEL variable"""
    monkeypatch.setenv("SERVICE", "litellm")
    monkeypatch.setenv("LITELLM_BASE_URL", "https://fake_key.com")
    monkeypatch.setenv("LITELLM_API_KEY", "fake_key")
    monkeypatch.setenv("MODELE", "")
    result = charger_configuration()
    assert result["modele"] == DEFAULT_MODEL


def test_charger_configuration_fail_empty_api_key(monkeypatch):
    """Check empty api key raises ConfigurationInvalide exception"""
    monkeypatch.setenv("SERVICE", "litellm")
    monkeypatch.setenv("LITELLM_BASE_URL", "https://fake_key.com")
    monkeypatch.setenv("LITELLM_API_KEY", "")
    monkeypatch.setenv("MODELE", "gpt-luna")
    # Check pytest raises the ConfigurationInvalide exception, with a specific messages pattern matching
    with pytest.raises(ConfigurationInvalide, match="LITELLM_API_KEY"):
        charger_configuration()


def test_charger_configuration_fail_empty_url(monkeypatch):
    """Check empty url raises ConfigurationInvalide exception"""
    monkeypatch.setenv("SERVICE", "litellm")
    monkeypatch.setenv("LITELLM_BASE_URL", "")
    monkeypatch.setenv("LITELLM_API_KEY", "fake_key")
    monkeypatch.setenv("MODELE", "gpt-luna")
    with pytest.raises(ConfigurationInvalide, match="LITELLM_BASE_URL"):
        charger_configuration()

import pytest
import httpx2
import openai

from types import SimpleNamespace
from unittest.mock import Mock

from assistant.client import ServiceIndisponible, envoyer
from assistant.service_simule import (
    ServiceSimule,
    panne,
    delai_depasse,
    cle_refusee,
)

# Using parametrize since we are checking the exact same thing, but with diff parameters
# See: https://docs.pytest.org/en/stable/how-to/parametrize.html

FAKE_URL = "https://my-fake_url.com/v1"


def fake_http_error(error_class, status_code):
    """Build SDK HTTP error, same as in service_simule.py cle_refusee()
    So we can test the other errors we dont already have a function for in service_simule.py"""
    my_request = httpx2.Request("POST", FAKE_URL)
    return error_class(
        "Error", response=httpx2.Response(status_code, request=my_request), body=None
    )


def openai_generic_api_error():
    """Build SDK APIError without HTTP code"""
    return openai.APIError("Error", request=httpx2.Request("POST", FAKE_URL), body=None)


# These are based on the errors messages in client.py envoyer()
# id gives clearer names to each test
EXPECTED_ERRORS = [
    pytest.param(delai_depasse(), "in time", id="timeout"),
    pytest.param(panne(), "could not be reached", id="connection"),
    pytest.param(cle_refusee(), "LITELLM_API_KEY", id="api_key"),
    pytest.param(fake_http_error(openai.RateLimitError, 429), "quota", id="quota"),
    pytest.param(
        fake_http_error(openai.NotFoundError, 404), "NotFound", id="not_found"
    ),
    pytest.param(
        fake_http_error(openai.InternalServerError, 500), "HTTP 500", id="HTTP_error"
    ),
    pytest.param(
        openai_generic_api_error(), "returned an error", id="Generic_API_Error"
    ),
]
TEST_MSG = [{"role": "user", "content": "Coucou, ceci est un test"}]


@pytest.mark.parametrize(
    "error, expected_message",
    EXPECTED_ERRORS,
)
def test_envoyer_fail_service_errors(error, expected_message):
    """Check each SDK error is raised as ServiceIndisponible with proper message"""
    service = ServiceSimule([error])
    with pytest.raises(ServiceIndisponible, match=expected_message):
        envoyer(service, "simule", TEST_MSG)


def test_envoyer_fail_empty_response():
    """Check empty response raises ServiceIndisponible"""
    fake_client = Mock()
    # Mock create a fake object, when you try to access one of its attribute, it creates that fake attribute as well. return_value is what is returned by create when called
    fake_client.chat.completions.create.return_value = SimpleNamespace(choices=[])
    with pytest.raises(ServiceIndisponible, match="empty response"):
        envoyer(fake_client, "simule", TEST_MSG)

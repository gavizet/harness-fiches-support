import pytest
from assistant.interface import parse_join, handle_joindre
from assistant.outils import AccesRefuse


# TESTS: interface.parse_join()
def test_parse_join_valid_command():
    assert parse_join("/joindre fiche.md Résume cette fiche.") == (
        "fiche.md",
        "Résume cette fiche.",
    )


def test_parse_join_valid_multiple_whitespaces():
    assert parse_join("/joindre     fiche.md      Résume cette fiche.") == (
        "fiche.md",
        "Résume cette fiche.",
    )


def test_parse_join_fail_wrong_command():
    assert parse_join("/joindreabc fiche.md Résume cette fiche.") is None


def test_parse_join_fail_no_arg():
    assert parse_join("/joindre") is None


def test_parse_join_fail_missing_arg():
    assert parse_join("/joindre fiche.md") is None


def test_handle_joindre_fail_access_refused(limites):
    """Check /joindre to a file outside folder returns None"""
    result = handle_joindre("/joindre ../.env.md Résume", limites)
    assert result is None

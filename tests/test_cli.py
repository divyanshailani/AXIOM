import builtins

import pytest

from axiom.orchestrator import AxiomOrchestrator


def test_cli_handles_eof_without_infinite_loop(monkeypatch, capsys):
    # Ctrl-D on input() raises EOFError; the CLI must exit, not loop forever.
    import cli

    calls = {"n": 0}

    def fake_input(prompt=""):
        calls["n"] += 1
        raise EOFError

    monkeypatch.setattr(builtins, "input", fake_input)
    cli.main()
    assert calls["n"] == 1, "EOF should exit after one input attempt"
    out = capsys.readouterr().out
    assert "Shutting down AXIOM" in out


def test_cli_exits_on_quit(monkeypatch, capsys):
    import cli

    inputs = iter(["hello", "quit"])

    def fake_input(prompt=""):
        return next(inputs)

    monkeypatch.setattr(builtins, "input", fake_input)
    cli.main()
    out = capsys.readouterr().out
    assert "Shutting down AXIOM" in out


def test_cli_skips_blank_lines(monkeypatch, capsys):
    import cli

    inputs = iter(["", "   ", "bye", "exit"])

    def fake_input(prompt=""):
        return next(inputs)

    monkeypatch.setattr(builtins, "input", fake_input)
    cli.main()
    out = capsys.readouterr().out
    assert "Shutting down AXIOM" in out


def test_cli_init_failure_message(monkeypatch, capsys):
    import cli

    def boom(self):
        raise RuntimeError("no numpy")

    monkeypatch.setattr(AxiomOrchestrator, "__init__", boom)
    cli.main()
    out = capsys.readouterr().out
    assert "Failed to initialize" in out
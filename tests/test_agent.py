from app.agent.agent_llm import send_prompt, agent

def test_send_prompt():
    response = send_prompt("this is a test")
    assert not response.startswith("[AGENT ERROR]:"), f"Agent errored: {response}"
    assert response != "[No Valid AI response]"
    assert isinstance(response, str) and len(response) > 0

def make_msg(t, c):
    return type("Msg", (), {"type": t, "content": c})()

# When we get an ai response, we need to ensure that the last valid ai message is returned to the user at the terminal
def test_send_prompt_returns_latest_ai(monkeypatch):
    # fake two AI messages; we expect the last one
    msgs = [make_msg("ai", "first"), make_msg("ai", "second")]
    # patch agent.invoke to return our fake result
    monkeypatch.setattr(agent, "invoke", lambda *args, **kwargs: {"messages": msgs})
    assert send_prompt("anything") == "second"

def test_send_prompt_catches_exceptions(monkeypatch):
    # force invoke() to raise
    def bad_invoke(*args, **kwargs):
        raise RuntimeError("oops")
    monkeypatch.setattr(agent, "invoke", bad_invoke)

    result = send_prompt("trigger")
    assert result.startswith("[AGENT ERROR]:")
    assert "oops" in result


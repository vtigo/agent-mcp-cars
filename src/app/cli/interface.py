import typer
from app.agent.agent_llm import send_prompt

app = typer.Typer()

@app.command()
def start_prompt_loop():
    typer.echo("\nPress Ctrl+C to exit.\n\nMick: Hello! How can i assist you?")
    
    # TODO: Gracefully exit the loop
    while True:
        try:
            prompt = typer.prompt("you")
            if not prompt.strip():
                continue
            typer.echo("...")
            response = send_prompt(prompt)
            typer.echo(f"\nMick: {response}")
        except KeyboardInterrupt:
            typer.echo("\n bye bye")
            break


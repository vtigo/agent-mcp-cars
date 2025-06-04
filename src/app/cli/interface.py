import typer
from app.agent.agent_llm import send_prompt
from app.database.session import check_conn

app = typer.Typer()

@app.command()
def prompt():
    """Run a prompt loop to talk with the agent."""
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

@app.command()
def check_db():
    """Check if the connection to the database is working propperly."""
    check_conn()

def cli_interface():
    app()

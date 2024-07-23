import typer
from typing import List
from .config.config import get_db
from .api.user_api import UserAPI
from .models.user import User

app = typer.Typer(no_args_is_help=True)

@app.command()
def register(
    name: List[str] = typer.Argument(..., help='Name of the user'),
    phone: str = typer.Option(..., '--phone', '-p', help='Phone of the user')
):
    name = ' '.join(name)
    api = UserAPI(get_db())
    user = User(name, phone)
    api.register_user(user)
    print('User registered successfully!')
    
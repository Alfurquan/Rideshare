import typer
from typing import List
from .models.vehicle import Vehicle
from .api.vehicle_api import VehicleAPI
from .api.user_api import UserAPI
from .config.config import get_db

app = typer.Typer(no_args_is_help=True)

@app.command()
def register(
    model : List[str] = typer.Argument(..., help="model of vehicle"),
    number: str = typer.Option(..., "--number", "-n", help="Vehicle number"),
    owner: int = typer.Option(..., "--owner-id", "-o", help="Owner id of vehicle")
):
    model = ' '.join(model)
    api = VehicleAPI(get_db(), UserAPI(get_db()))
    api.register(Vehicle(model, number, owner))
    print('Vehicle registered succesfully!')
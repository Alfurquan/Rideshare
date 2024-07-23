import typer
from . import user
from . import vehicle
from . import ride

app = typer.Typer(no_args_is_help=True, help="Ride share is a small ride sharing CLI app")
app.add_typer(user.app, name='users')
app.add_typer(vehicle.app, name='vehicles')
app.add_typer(ride.app, name='rides')
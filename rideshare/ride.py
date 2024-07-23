import typer
import rich
from rich.table import Table
from io import StringIO
from .api.ride_api import RideAPI
from .api.vehicle_api import VehicleAPI
from .api.user_api import UserAPI
from .config.config import get_db
from .strategy.selection_strategy import Strategy

app = typer.Typer(no_args_is_help=True)

@app.command()
def offer(
    driver: int = typer.Option(...,"--driver-id", "-d", help="User offering the ride"),
    source: str = typer.Option(..., "--source", "-s", help="Source of ride"),
    destination: str = typer.Option(..., "--destination", "-d", help="Destination of ride"),
    seats: int = typer.Option(..., "--seats", "-se", help="Seats for ride"),
    fare: int = typer.Option(..., "--fare", "-f", help="Fare for the ride"),
    vehicle_id: int = typer.Option(..., "--vehicle-id", "-v", help="Vehicle id of the ride")
):
    user_api = UserAPI(get_db())
    api = RideAPI(get_db(), user_api, VehicleAPI(get_db(), user_api))
    api.offer_ride(driver, source, destination, seats, fare, vehicle_id)
    print('Ride offered successfully, waiting for passengers!')
    
@app.command()
def search(
    source: str = typer.Option(..., "--source", "-s", help="Source of ride"),
    destination: str = typer.Option(..., "--destination", "-d", help="Destination of ride"),
    seats: int = typer.Option(..., "--seats", "-se", help="Seats for ride"),
    selection_strategy: str = typer.Option(Strategy.MOST_VACANT.value, "--strategy", help="Strategy for selecting rides"),
):
    strategy = Strategy(selection_strategy)
    
    user_api = UserAPI(get_db())
    api = RideAPI(get_db(), user_api, VehicleAPI(get_db(), user_api))
    ride = api.search_ride(source, destination, seats, strategy)
    
    selected_ride = ride[0] if len(ride) > 0 else None
    
    if selected_ride is None:
        print("No rides found for given source and destination")
        raise typer.Exit(1)
        
    table = Table(box=rich.box.SIMPLE)
    table.add_column("RideId")
    table.add_column("Source")
    table.add_column("Destination")
    table.add_column("Driver name")
    table.add_column("Driver phone")
    table.add_column("Vehicle name")
    table.add_column("Ride fare")
    table.add_column("Seats")

    for ride in selected_ride.rides:
        table.add_row(str(ride.id), ride.source, ride.destination, ride.driver.name, ride.driver.phone, ride.vehicle.model, str(ride.fare), str(ride.seats))
    out = StringIO()
    rich.print(table, file=out)
    print(out.getvalue())
    
    table = Table(box=rich.box.SIMPLE)
    table.add_column("Total fare")
    table.add_column("Available seats")
    
    table.add_row(str(selected_ride.total_fare), str(selected_ride.available_seats))
    out = StringIO()
    rich.print(table, file=out)
    print(out.getvalue())
    
    select = typer.confirm("Do you want to select the rides ?")
    if not select:
        raise typer.Exit()
    
    user_ids : str = typer.prompt("Enter user ids seprated by comma of passengers to continue")
    user_ids = user_ids.split(",")
    
    if len(user_ids) != seats:
        print('User ids do not match no of seats, please check and re enter')
        raise typer.Exit()
    
    api.select_rides(selected_ride.rides, user_ids)
    print("Your ride has been confirmed!")

@app.command()
def end(
    ride_id: int = typer.Argument(..., help="Enter ride id to end")
):
    user_api = UserAPI(get_db())
    api = RideAPI(get_db(), user_api, VehicleAPI(get_db(), user_api))
    api.end_ride(ride_id)
    print('Ride has ended!')
    
@app.command()
def stats():
    user_api = UserAPI(get_db())
    api = RideAPI(get_db(), user_api, VehicleAPI(get_db(), user_api))
    ride_stats = api.get_ride_stats()
    #print(ride_stats)
    
    table = Table(box=rich.box.SIMPLE)
    table.add_column("Person")
    table.add_column("Rides Offered")
    table.add_column("Rides Taken")

    for ride_stat in ride_stats:
       table.add_row(ride_stat, str(ride_stats[ride_stat]['rides_offered']), str(ride_stats[ride_stat]['rides_taken']))
    out = StringIO()
    rich.print(table, file=out)
    print(out.getvalue())
    
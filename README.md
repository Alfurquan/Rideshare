# Rideshare

Rideshare is a small CLI ride booking and sharing app developed using [poetry](https://python-poetry.org/) and [typer](https://typer.tiangolo.com/)

### Requirements

Requirements can be found [here](/requirements.md)

### Design and models

Models and design can be found [here](./design.md)

### Usage
==========

```python

rideshare

 Usage: rideshare [OPTIONS] COMMAND [ARGS]...

 Ride share is a small ride sharing CLI app

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                                                                      │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                                                                               │
│ --help                        Show this message and exit.                                                                                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ rides                                                                                                                                                                                                                        │
│ users                                                                                                                                                                                                                        │
│ vehicles                                                                                                                                                                                                                     │
╰───────────

## Registering a user
rideshare users register Anil --phone 7803804265

## Registering a vehicle
rideshare vehicles register Maruti --number KA-19-16633 --owner-id 1

## Offering a ride
rideshare rides offer --driver-id 1 --source "Mysore" --destination "Ooty" --seats 5 --vehicle-id 6 --fare 200

## Searching a ride
rideshare rides search --source Bangalore --destination Ooty --seats 2 --strategy Most_cheapest

  RideId   Source      Destination   Driver name   Driver phone   Vehicle name   Ride fare   Seats  
 ────────────────────────────────────────────────────────────────────────────────────────────────── 
  2        Bangalore   Ooty          Rahul         7003404265     Activa         500         20     



  Total fare   Available seats  
 ────────────────────────────── 
  500          20


Do you want to select the rides ? [y/N]: y
Enter user ids seprated by comma of passengers to continue: 4,5
Your ride has been confirmed!

## Ending a ride
rideshare rides end 6

## Printing ride stats
rideshare rides stats

  Person     Rides Offered   Rides Taken  
 ──────────────────────────────────────── 
  John       3               0
  Rahul      1               0
  Rohan      1               0
  Shashank   1               3
  Ankita     0               3
  Suhana     0               2

```

### How to setup and run
- Install poetry from [here](https://python-poetry.org/docs/)
- Git clone the repo
- Go to repo directory and run these commands
    ```shell
    poetry install
    poetry shell
    ```
- Start running off the cli commands.

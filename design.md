## Ride sharing application design

Simple ride sharing application models and classes

1. User
========
- id
- name
- phone

2. Vehicle
===========
- id
- model
- vehicle_no
- owner_id

3. Ride
==========
- id
- source
- destination
- avl_seats
- vehicle
- driver : userid
- passengers: [user]
- fare
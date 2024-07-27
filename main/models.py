from django.db import models
from django.contrib.auth.models import User

class customer(models.Model):
    uid = models.AutoField(primary_key=True)
    company = models.CharField(max_length=255, unique=True)
    phone_number = models.BigIntegerField()

    def __str__(self):
        return f"Customer ID: {self.uid}, Company: {self.company}, Phone Number: {self.phone_number}"

class location(models.Model):
    city = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    def __str__(self):
         return f"Location ID: {self.id}, City: {self.city}, Country: {self.country}"

class supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    phone = models.BigIntegerField()

    def __str__(self):
         return f"Supplier ID: {self.id}, Name: {self.name}, Phone: {self.phone}"

class warehouse(models.Model):
    warehouse_name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Warehouse ID: {self.id}, Name: {self.warehouse_name}, Capacity: {self.capacity}"

class package(models.Model):
    sup = models.ForeignKey(supplier, on_delete=models.CASCADE,to_field='name')
    ware = models.ForeignKey(warehouse, on_delete=models.CASCADE,to_field='warehouse_name')
    contents = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Package ID: {self.id}, Supplier ID: {self.sup}, Warehouse ID: {self.ware}, Contents: {self.contents}"

class payment(models.Model):
    company_name = models.ForeignKey(customer, on_delete=models.CASCADE,to_field='company')
    amount_in_crores = models.IntegerField()

    def __str__(self):
        return f"Payment ID: {self.id}, Customer ID: {self.company_name}, Amount in Crores: {self.amount_in_crores}"

class route(models.Model):
    name = models.CharField(max_length=255, unique=True)
    startlocation = models.ForeignKey(location, on_delete=models.CASCADE, related_name='start_routes',to_field='city')
    destination = models.ForeignKey(location, on_delete=models.CASCADE, related_name='destination_routes',to_field='city')
    duration = models.CharField(max_length=255)
    distance = models.CharField(max_length=20)

    def __str__(self):
        return f"Route ID: {self.id}, Route Name: {self.name}, Start Location: {self.startlocation}, Destination: {self.destination}, Duration: {self.duration}, Distance: {self.distance}"

class ship(models.Model):
    ship_name = models.CharField(max_length=255, unique=True)
    ship_type = models.CharField(max_length=255)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Ship ID: {self.id}, Ship Name: {self.ship_name}, Ship Type: {self.ship_type}, Capacity: {self.capacity}"

class shipment(models.Model):
    cust = models.ForeignKey(customer, on_delete=models.CASCADE,to_field='company')
    ships = models.ForeignKey(ship, on_delete=models.CASCADE, to_field='ship_name')
    routes = models.ForeignKey(route, on_delete=models.CASCADE,to_field='name')
    package = models.ForeignKey(package, on_delete=models.CASCADE ,to_field='contents')
    departure_date = models.DateField()
    arrival_date = models.DateField()

    def __str__(self):
        return f"Shipment ID: {self.id}, Customer ID: {self.cust}, Ship ID: {self.ships}, Route ID: {self.routes}, Departure Date: {self.departure_date}, Arrival Date: {self.arrival_date}"


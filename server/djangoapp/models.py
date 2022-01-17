from django.db import models
from django.utils.timezone import now


# Create your models here.
SEDAN = "SEDAN"
SUV = "SUV"
WAGON = "WAGON"
# (...)

CAR_MODELS_CHOICES = (
    (SEDAN, "Sedan"),
    (SUV, "SUV"),
    (WAGON, "WAGON"),
)

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)

    def __str__(self):
      return ("Car name: {0}, description: {1}".format(self.name, self.description))


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    car_makes = models.ManyToManyField(CarMake, related_name='carModels')
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=30)
    car_type = models.CharField(max_length=30, choices=CAR_MODELS_CHOICES)
    year = models.DateField()

    def __str__(self):
      return ("Car name: {0}, type: {1}".format(self.name, self.car_type))


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    company = models.CharField(max_length=100, help_text="Company Name")

    def __str__(self):
        return str(self.username)


class Gateway(models.Model):
    gps_lat = models.DecimalField(max_digits=11, decimal_places=8, help_text=
    'Latitudinal coordinate of the gateway.')
    gps_lon = models.DecimalField(max_digits=11, decimal_places=8, help_text=
    'Longitudinal coordinate of the gateway.')
    last_seen = models.DateTimeField(default=timezone.now)
    mac = models.UUIDField(help_text="The device's MAC address.")
    user = models.ForeignKey(User, null=False)
    serial = models.CharField(max_length=100, help_text="The device's serial number")

    def __str__(self):
        return str(self.__dict__)


class Node(models.Model):
    app_eui = models.UUIDField()
    app_key = models.CharField(max_length=100)
    dev_addr = models.CharField(max_length=100)
    dev_eui = models.UUIDField()
    last_gateway = models.ForeignKey(Gateway, null=True, blank=True)
    last_seen = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=False)

    def __str__(self):
        return str(self.__dict__)


class Swarm(models.Model):
    created = models.DateTimeField()
    last_seen = models.DateTimeField()
    name = models.CharField(max_length=100)
    nodes = models.ForeignKey(Node)
    user = models.ForeignKey(User, null=False)

    def __str__(self):
        return str(self.__dict__)


# {
#   "applicationID": "bd60ba7f-a94e-466c-a26f-ea2d5e517173",
#   "applicationName": "wind-sensor",
#   "data": 532.9433,
#   "devEUI": "87832a8a-7c05-4568-bef5-9e81b44d282f",
#   "fCnt": 25,
#   "fPort": 1,
#   "nodeName": "sensor",
#   "frequency": 868500000

class Message(models.Model):
    applicationName = models.CharField(max_length=100)
    applicationID = models.UUIDField()
    devEUI = models.UUIDField()
    nodeName = models.CharField(max_length=100)
    data = models.TextField()
    fCnt = models.IntegerField()
    fPort = models.IntegerField()
    node = models.ForeignKey(Node, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    rxInfo = models.ForeignKey('RxInfo', blank=True, null=True)
    txInfo = models.ForeignKey('TxInfo', blank=True, null=True)

    def __str__(self):
        return str(self.__dict__)

# "rxInfo": [
#     {
#       "altitude": 1845,
#       "latitude": 27.7452,
#       "loRaSNR": 18,
#       "longitude": 14.5545,
#       "mac": "a8911506-23b1-4b0f-b333-3ad5ce4d3d24",
#       "name": "gateway",
#       "rssi": -44,
#       "time": "2002-05-27T06:01:09.000Z"
#     }
#   ],
class RxInfo(models.Model):
    altitude = models.IntegerField()
    latitude = models.DecimalField(max_digits=11, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    loRaSNR = models.IntegerField()
    gateway = models.ForeignKey(Gateway, blank=True, null=True)
    gatewayMac = models.UUIDField()
    gatewayName = models.CharField(max_length=100)
    rssi = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return str(self.__dict__)


#   "txInfo": {
#     "adr": false,
#     "codeRate": "4/8",
#     "dataRate": {
#       "bandwidth": 5,
#       "modulation": "LORA",
#       "spreadFactor": 12
#     }
#   }
# }
class TxInfo(models.Model):
    adr = models.BooleanField(default=False)
    codeRate = models.CharField(max_length=10)
    bandwidth = models.IntegerField(default=0)
    modulation = models.CharField(max_length=10)
    spreadFactor = models.IntegerField(default=0)
    frequency = models.IntegerField(default=0)

    def __str__(self):
        return str(self.__dict__)


class ErrorModel(models.Model):
    type = models.CharField(max_length=100)
    errorCode = models.IntegerField()

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework import serializers


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    gateways = models.ForeignKey('api.Gateway')
    nodes = models.ForeignKey('api.Node')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'company')


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        profile.save()


class Gateway(models.Model):
    gps_lat = models.FloatField()
    gps_lon = models.FloatField()
    last_seen = models.CharField(max_length=100)
    mac = models.CharField(max_length=100)
    serial = models.CharField(max_length=100)


class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway


class Node(models.Model):
    app_eui = models.CharField(max_length=100)
    app_key = models.CharField(max_length=100)
    dev_addr = models.CharField(max_length=100)
    dev_eui = models.CharField(max_length=100)
    last_gateway = models.ForeignKey(Gateway)
    last_seen = models.DateTimeField()
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node


class Swarm(models.Model):
    created = models.DateTimeField()
    last_seen = models.DateTimeField()
    name = models.CharField(max_length=100)
    nodes = models.ForeignKey(Node)


class SwarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swarm


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
    latitude = models.FloatField()
    loRaSNR = models.IntegerField()
    longitude = models.FloatField()
    gateway = models.ForeignKey(Gateway, blank=True, null=True)
    gatwayMac = models.UUIDField()
    gatwayName = models.CharField(max_length=100)
    rssi = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return str(self.__dict__)


class RxInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RxInfo


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


class TxInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TxInfo


class ErrorModel(models.Model):
    type = models.CharField(max_length=100)
    errorCode = models.IntegerField()

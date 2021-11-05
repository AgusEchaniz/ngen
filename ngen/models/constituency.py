# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import ipaddress
from abc import ABCMeta, ABC, abstractmethod

import validators
from django.db import models
from netfields import InetAddressField, NetManager, CidrAddressField

from .incident import NgenModel


class AbstractModelMeta(ABCMeta, type(models.Model)):
    pass


class NetworkElement(NgenModel, metaclass=AbstractModelMeta):
    id = models.BigAutoField(primary_key=True)
    cidr = CidrAddressField(blank=True, null=True)
    domain = models.CharField(max_length=255, blank=True, null=True)
    _address = None
    DOMAIN_ADDRESS: int = 1
    IPV4_ADDRESS: int = 2
    IPV6_ADDRESS: int = 3
    objects = NetManager()

    def guess_address_type(self, address: str):
        if validators.domain(address):
            return self.DOMAIN_ADDRESS
        if validators.ipv4_cidr(address):
            return self.IPV4_ADDRESS
        if validators.ipv6_cidr(address):
            return self

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.cidr:
            self.address = self.cidr.exploded
        elif self.domain:
            self.address = self.domain

    @classmethod
    def create(cls, address: str):
        model = cls(address)
        model.cidr = address
        return model

    @property
    def address(self) -> "Address":
        return self._address

    @address.setter
    def address(self, value: str):
        if self.guess_address_type(value) == self.DOMAIN_ADDRESS:
            self._address = AddressDomain(value)
            self.domain = self.address.address
        elif self.guess_address_type(value) in [self.IPV4_ADDRESS, self.IPV6_ADDRESS]:
            self._address = AddressIp(value)
            self.ip = str(self.address.address)
            self.ip_mask = self.address.address_mask
        else:
            raise ValueError()

    def __eq__(self, other: "Address"):
        return self.address == other.address

    def __repr__(self):
        return self.address.address

    def __contains__(self, other: "Address"):
        # b.address._address.subnet_of(a.address._address)
        return other.address in self.address

    def is_default(self):
        return self.address.address_mask == 0

    class Meta:
        abstract = True
        ordering = ['name']


class Host(NetworkElement):
    network = models.ForeignKey('Network', models.DO_NOTHING, blank=True, null=True)
    slug = models.CharField(max_length=100, blank=True, null=True)
    active = models.IntegerField()
    created_by = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    ip = InetAddressField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.ip:
            self.address = self.ip.exploded
        elif self.domain:
            self.address = self.domain

    class Meta:
        db_table = 'host'


class Network(NetworkElement):
    network_admin = models.ForeignKey('NetworkAdmin', models.DO_NOTHING, blank=True, null=True)
    network_entity = models.ForeignKey('NetworkEntity', models.DO_NOTHING, blank=True, null=True)
    active = models.BooleanField(default=True)
    type = models.CharField(max_length=8, blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True, null=True)
    asn = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    @NetworkElement.address.setter
    def address(self, value: str):
        if self.guess_address_type(value) == self.DOMAIN_ADDRESS:
            self._address = AddressDomain(value)
            self.domain = self.address.address
        elif self.guess_address_type(value) in [self.IPV4_ADDRESS, self.IPV6_ADDRESS]:
            self._address = AddressIp(value)
            self.ip = str(self.address.address)
            self.ip_mask = self.address.address_mask
            self.ip_start_address = self.address._address.network_address.exploded
            self.ip_end_address = self.address._address.broadcast_address.exploded
        else:
            raise ValueError()

    def save(self, *args, **kwargs):
        if not self.is_default() and self.cidr:
            self.host_set.clear()
            Host.objects.filter(ip__net_contained=self.cidr.exploded).update(network=self)

        super(Network, self).save(*args, **kwargs)

    class Meta:
        db_table = 'network'
        ordering = ['cidr']


class NetworkAdmin(NgenModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=100, blank=True, null=True)
    active = models.IntegerField()
    created_by = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'network_admin'


class NetworkEntity(NgenModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, blank=True, null=True)
    active = models.IntegerField()
    created_by = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'network_entity'


class Address(ABC):
    _address = None
    _address_mask = None

    def __init__(self, address):
        self.address = address

    @property
    @abstractmethod
    def address(self):
        pass

    @address.setter
    def address(self, value):
        self._address = self.create_address_object(value)

    @property
    @abstractmethod
    def address_mask(self):
        pass

    @address_mask.setter
    def address_mask(self, value):
        self._address_mask = value

    @abstractmethod
    def in_range(self, other):
        pass

    @abstractmethod
    def create_address_object(self, address):
        pass

    def __eq__(self, other: "Address"):
        return self.address == other.address

    def __contains__(self, other: "Address"):
        return self.in_range(other)


class AddressIp(Address):

    @Address.address.getter
    def address(self):
        return self._address.exploded

    def address_mask(self):
        return self._address.prefixlen

    def create_address_object(self, address: str):
        return ipaddress.ip_network(address)

    def in_range(self, other: Address):
        return other._address > self._address


class AddressDomain(Address):
    @Address.address.getter
    def address(self) -> str:
        return self._address

    def address_mask(self: Address):
        return len(self.address.split('.'))

    def create_address_object(self, address):
        return address

    def in_range(self: Address, other: Address):
        address_set = set(self.address.split('.'))
        address_set_other = set(other.address.split('.'))

        if address_set == address_set_other:
            return True

        if address_set_other > address_set:
            return address_set & address_set_other == address_set

        return False

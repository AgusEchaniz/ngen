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
from django.db.models import F
from netfields import NetManager, CidrAddressField
from treebeard.al_tree import AL_Node

from .incident import NgenModel


class AbstractModelMeta(ABCMeta, type(models.Model)):
    pass


class NetworkElement(NgenModel, metaclass=AbstractModelMeta):
    id = models.BigAutoField(primary_key=True)
    cidr = CidrAddressField(null=True, unique=True)
    domain = models.CharField(max_length=255, null=True, unique=True, default=None)
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
            return self.IPV6_ADDRESS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.cidr:
            if isinstance(self.cidr, str):
                self.address = self.cidr
            else:
                self.address = self.cidr.exploded
        elif self.domain:
            self.address = self.domain

    @classmethod
    def create(cls, address: str):
        model = cls(address)
        model.address = address
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
        else:
            raise ValueError()

    def __eq__(self, other: "NetworkElement"):
        if isinstance(other, NetworkElement):
            return self.address == other.address

    def __repr__(self):
        return self.address.address

    def __contains__(self, other: "NetworkElement"):
        # b.address._address.subnet_of(a.address._address)
        if isinstance(other, NetworkElement):
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

    class Meta:
        db_table = 'host'


class Network(NetworkElement, AL_Node):
    network_admin = models.ForeignKey('NetworkAdmin', models.DO_NOTHING, blank=True, null=True)
    network_entity = models.ForeignKey('NetworkEntity', models.DO_NOTHING, blank=True, null=True)
    active = models.BooleanField(default=True)
    type = models.CharField(max_length=8, blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True, null=True)
    asn = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, null=True, db_index=True)
    node_order_by = ['parent', '-cidr', '-domain']

    @classmethod
    def find_problems(cls):
        pass

    @classmethod
    def fix_tree(cls):
        pass

    @NetworkElement.address.setter
    def address(self, value: str):
        if self.guess_address_type(value) == self.DOMAIN_ADDRESS:
            self._address = AddressDomain(value)
            self.domain = self.address.address
        elif self.guess_address_type(value) in [self.IPV4_ADDRESS, self.IPV6_ADDRESS]:
            self._address = AddressIp(value)
        else:
            raise ValueError()

    def save(self, *args, **kwargs):
        super(Network, self).save(*args, **kwargs)
        networks = None
        if not self.is_default():
            if self.cidr:
                parent = Network.objects.filter(cidr__net_contains=self.cidr.exploded).order_by('-cidr').first()
                children = parent.get_children().filter(cidr__net_contained=self.cidr.exploded)
            elif self.domain:
                parent =
                children =
                networks = Network.objects.filter(domain__endswith=self.domain).exclude(
                    parent__domain__exact=self.domain).annotate(
                    network_domain_length=F('parent__domain')).filter(
                    network_domain_length__lt=len(self.domain))
            if networks:
                self.parent = parent
                self.get_children().difference(children).update(parent=self.parent)
                children.update(parent=self)

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

    def __init__(self, address):
        self.address = address

    @property
    @abstractmethod
    def address(self):
        pass

    @address.setter
    def address(self, value):
        self._address = self.create_address_object(value)

    @abstractmethod
    def address_mask(self):
        pass

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

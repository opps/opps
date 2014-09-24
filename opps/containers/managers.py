from opps.core.managers import PublishableManager, PublishableQuerySet

from polymorphic.manager import PolymorphicManager
from polymorphic.query import PolymorphicQuerySet


class ContainerQuerySet(PolymorphicQuerySet, PublishableQuerySet):
    pass


class ContainerManager(PolymorphicManager, PublishableManager):
    queryset_class = ContainerQuerySet

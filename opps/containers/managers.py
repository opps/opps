from polymorphic.manager import PolymorphicManager

from opps.core.managers import PublishableManager


class ContainerManager(PolymorphicManager, PublishableManager):
    pass

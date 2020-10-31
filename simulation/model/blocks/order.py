import logging

from casymda.blocks.entity import Entity
from simpy.core import Environment


class Order(Entity):
    def __init__(self, env: Environment, name: str):
        super().__init__(env, name)

        self._time_of_acceptance = -1
        self._initial_eta = -1
        self._eta = -1
        self._ready_at = -1
        self._sop_at = -1
        self._finished_at = -1

    @property
    def time_of_acceptance(self):
        return self._time_of_acceptance

    @time_of_acceptance.setter
    def time_of_acceptance(self, value):
        self._time_of_acceptance = value
        update(
            self.name,
            "time_of_acceptance",
            self._time_of_acceptance,
            self.env.now,
            self,
        )

    @property
    def initial_eta(self):
        return self._initial_eta

    @initial_eta.setter
    def initial_eta(self, value):
        self._initial_eta = value
        update(self.name, "initial_eta", self._initial_eta, self.env.now, self)

    @property
    def eta(self):
        return self._eta

    @eta.setter
    def eta(self, value):
        self._eta = value
        update(self.name, "eta", self._eta, self.env.now, self)

    @property
    def ready_at(self):
        return self._ready_at

    @ready_at.setter
    def ready_at(self, value):
        self._ready_at = value
        update(self.name, "ready_at", self._ready_at, self.env.now, self)

    @property
    def sop_at(self):
        return self._sop_at

    @sop_at.setter
    def sop_at(self, value):
        self._sop_at = value
        update(self.name, "sop_at", self._sop_at, self.env.now, self)

    @property
    def finished_at(self):
        return self._finished_at

    @finished_at.setter
    def finished_at(self, value):
        self._finished_at = value
        update(self.name, "finished_at", self._finished_at, self.env.now, self)


def update(name: str, attribute: str, value: float, t: float, order: Order):
    # (replaced by actual callback during emulation initialization)
    logging.info(
        f"order update - name: {name}, attribute: {attribute}, value: {value}, t: {t}"
    )

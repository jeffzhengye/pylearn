import random
from transitions import Machine, State


class Matter(object):
    heat = False
    attempts = 0

    def count_attempts(self):
        self.attempts += 1
        print("count")

    def heat_up(self):
        self.heat = random.random() < 0.5
        print(f"heat up {self.heat}")

    def before_test(self):
        print(f"before: current state: {self.state}")

    def stats(self):
        print("It took you %i attempts to melt the lump!" % self.attempts)
        print(f"after: current state: {self.state}")

    def make_hissing_noises(self):
        print("hisssss")

    def disappear(self):
        print("where'd all the liquid go?")

    @property
    def is_really_hot(self):
        return self.heat

    def raise_error(self, event): raise ValueError("Oh no")
    def prepare(self, event): print("I am ready!")
    def finalize(self, event): print("Result: ", type(event.error), event.error)

states = ["solid", "liquid", "gas", "plasma"]

transitions = [
    {
        "trigger": "melt",
        "source": "solid",
        "dest": "liquid",
        "prepare": ["heat_up", "count_attempts"],
        "conditions": "is_really_hot",
        "before": "before_test",
        "after": "stats",
    },
]

lump = Matter()
machine = Machine(
    lump,
    states,
    transitions=transitions,
    initial="solid",
    before_state_change="make_hissing_noises",
    after_state_change="disappear",
    # prepare_event='prepare',
    # finalize_event='finalize',
    send_event=True
)
lump.melt()
# lump.melt()
# lump.melt()
# lump.melt()
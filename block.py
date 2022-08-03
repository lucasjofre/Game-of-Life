import settings as s


class Block:
    def __init__(self, state: int) -> None:
        self.state = state
        self.color = s.BLACK

    @property
    def state(self) -> int:
        return self._state

    @state.setter
    def state(self, value: int) -> None:
        if value not in [0, 1]:
            raise ValueError("State should be either 0 or 1")
        self._state = value
        self.color = s.BLACK if self.state == 0 else s.WHITE

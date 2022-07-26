import settings as s


class Block:
    def __init__(self, state: int) -> None:
        self.state = state
        self._color = s.BLACK

    # todo: check if i can remove screen drawing as part of this class
    def draw_block(self, position: tuple) -> None:
        self._change_color()
        pygame.draw.rect(screen, self._color, pygame.Rect(position[0] * BLOCK_SIZE + GRID_WIDTH,
                                                          position[1] * BLOCK_SIZE + GRID_WIDTH,
                                                          BLOCK_SIZE - GRID_WIDTH, BLOCK_SIZE - GRID_WIDTH))

    def _change_color(self):
        self._color = s.BLACK if self.state == 0 else s.WHITE
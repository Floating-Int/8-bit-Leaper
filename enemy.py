from displaylib import *
from text_collider import TextCollider


class Enemy(Sprite, TextCollider):
    texture = [
        [*"  O"],
        [*"/ | \\"],
        [*" / \\"],
    ]
    
    def __init__(self, parent: Node | None = None, *, x: float = 0, y: float = 0, texture: list[list[str]] = 8, color: str = color.WHITE, offset: Vec2 = Vec2(0, 0), centered: bool = False, z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x=x, y=y, texture=texture, color=color, offset=offset, centered=centered, z_index=z_index, force_sort=force_sort)
        self._health = 10
        self._label = Label(self, x=0, y=-1, text="10HP".rjust(4))
    
    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int) -> None:
        self._health = value
        self._label.text = (str(value) + "HP").rjust(4)
        if value <= 0:
            self.queue_free()
    
    def queue_free(self) -> None:
        self._label.queue_free()
        super().queue_free()

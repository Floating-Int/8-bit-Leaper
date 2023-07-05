from displaylib import *
import keyboard
# from text_collider import TextCollider


RIGHT = 1
LEFT = -1


class Projectile(Sprite): # TextCollider
    texture = ["*"]
    direction: int = RIGHT

    def _update(self, _delta: float) -> None:
        # self.move_and_slide(Vec2(4 * self.direction, 0))
        self.position.x += 4 * self.direction


class Firearm(Sprite):
    texture = [[*"¨¨"]]

    def __init__(self, parent: Node | None = None, *, x: float = 0, y: float = 0, texture: list[list[str]] = [], color: str = color.WHITE, offset: Vec2 = Vec2(0, 0), centered: bool = False, z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x=x, y=y, texture=texture, color=color, offset=offset, centered=centered, z_index=z_index, force_sort=force_sort)
        self.frame_idx = 0
        self.initial_position = Vec2(x, y)
        self.direction = RIGHT
        self.ignore = False
        self.process_priority = 3
        # self.ammo = 50

    def _update(self, _delta: float) -> None:
        if self.is_globally_visible():
            self.frame_idx += 1
            if not self.ignore:
                if 5 <= self.frame_idx <= 7:
                    if self.direction == RIGHT:
                        self.position.x = self.initial_position.copy().x -1
                    elif self.direction == LEFT:
                        self.position.x = self.initial_position.copy().x -5
                else:
                    if self.direction == RIGHT:
                        self.position = self.initial_position.copy()
                    elif self.direction == LEFT:
                        self.position = self.initial_position.copy() - Vec2(6, 0)
            if keyboard.is_pressed("shift"):# and self.ammo > 0:
                # self.ammo -= 1
                self.shoot()

    def shoot(self) -> None:
        projectile = Projectile(color=color.AQUA)
        projectile.set_global_position(self.get_global_position())
        if self.direction == RIGHT:
            projectile.position.x += 2
        else:
            projectile.position.x -= 1
            projectile.direction = LEFT

from displaylib import *
import keyboard
from text_collider import TextCollider
from firearm import Firearm


GRAVITY = 0.2
JUMP_POWER = 1.4 * 1.5
ACELERATION = 1.5
FRICTION = Vec2(1, 0.1)
RIGHT = 1
LEFT = -1


class Player(TextCollider, Sprite):
    texture = [
        [*"   O  "],
        [*" / | \\"],
        [*"  / \\ "]
    ]
    def __init__(self, parent: Node = None, x: float = 0, y: float = 0, color: str = color.SLATE_BLUE):
        super().__init__(parent, x=x, y=y)
        self.color = color
        self.velocity = Vec2()
        self.anim_player = AnimationPlayer(
            self,
            Idle=Animation("./animations/idle"),
            IdleAir=Animation("./animations/idle_air"),
            WalkRight=Animation("./animations/walk"),
            WalkLeft=Animation("./animations/walk", fliph=True),
            FlyRight=Animation("./animations/fly"),
            FlyLeft=Animation("./animations/fly", fliph=True)
        )
        self.firearm = Firearm(self, x=5, y=1, color=color)
        self.firearm.hide()
    
    def _update(self, _delta: float) -> None:
        self.move_and_slide(self.velocity)
        self.velocity.x = lerp(self.velocity.x, 0, FRICTION.x)
        self.velocity.y = lerp(self.velocity.y, 0, FRICTION.y)
        if self.is_on_floor():
            self.firearm.show()
            self.velocity.y = 0
        else:
            self.firearm.hide()
            self.velocity.y += GRAVITY
        self.firearm.ignore = False
        if not any(keyboard.is_pressed(key) for key in "ad"):
            if self.is_on_floor():
                self.anim_player.play("Idle")
                self.firearm.frame_idx = 0
                if self.firearm.direction == LEFT:
                    self.firearm.position.x = self.firearm.initial_position.x - 5
                    self.firearm.ignore = True
            else:
                if not self.anim_player.is_playing:
                    self.anim_player.play("IdleAir")
        elif not all(keyboard.is_pressed(key) for key in "ad"):
            if keyboard.is_pressed("a"):
                self.firearm.direction = LEFT
                self.velocity.x -= ACELERATION
                if self.is_on_floor():
                    if not self.anim_player.is_playing:
                        self.anim_player.play("WalkLeft")
                        self.firearm.frame_idx = 0
                    elif not self.anim_player.current_animation == "WalkLeft":
                        self.anim_player.play("WalkLeft")
                        self.firearm.frame_idx = 0
                else:
                    if not self.anim_player.is_playing:
                        self.anim_player.play("FlyLeft")
                    elif not self.anim_player.current_animation == "FlyLeft":
                        self.anim_player.play("FlyLeft")
            if keyboard.is_pressed("d"):
                self.firearm.direction = RIGHT
                self.velocity.x += ACELERATION
                if self.is_on_floor():
                    if not self.anim_player.is_playing:
                        self.anim_player.play("WalkRight")
                        self.firearm.frame_idx = 0
                    elif not self.anim_player.current_animation == "WalkRight":
                        self.anim_player.play("WalkRight")
                        self.firearm.frame_idx = 0
                else:
                    if not self.anim_player.is_playing:
                        self.anim_player.play("FlyRight")
                    elif not self.anim_player.current_animation == "FlyRight":
                        self.anim_player.play("FlyRight")
        else:
            if self.is_on_floor():
                self.anim_player.play("Idle")
                self.firearm.frame_idx = 0
                if self.firearm.direction == LEFT:
                    self.firearm.position.x = self.firearm.initial_position.x - 5
                    self.firearm.ignore = True
        if keyboard.is_pressed("space") and self.is_on_floor():
            self.velocity.y = -JUMP_POWER
    
    # def is_on_floor(self) -> bool:
    #     return self.get_global_position().y + 3 == self.root.screen.height - 3

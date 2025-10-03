"""Animation framework for smooth UI transitions."""

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

from imgui_bundle import imgui
from loguru import logger


class EasingFunction(Enum):
    """Easing functions for animations."""

    LINEAR = "linear"
    EASE_IN_QUAD = "ease_in_quad"
    EASE_OUT_QUAD = "ease_out_quad"
    EASE_IN_OUT_QUAD = "ease_in_out_quad"
    EASE_IN_CUBIC = "ease_in_cubic"
    EASE_OUT_CUBIC = "ease_out_cubic"
    EASE_IN_OUT_CUBIC = "ease_in_out_cubic"
    EASE_IN_SINE = "ease_in_sine"
    EASE_OUT_SINE = "ease_out_sine"
    EASE_IN_OUT_SINE = "ease_in_out_sine"
    EASE_IN_EXPO = "ease_in_expo"
    EASE_OUT_EXPO = "ease_out_expo"
    EASE_IN_OUT_EXPO = "ease_in_out_expo"
    BOUNCE = "bounce"
    ELASTIC = "elastic"


class AnimationState(Enum):
    """Animation states."""

    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"


@dataclass
class Animation:
    """Animation data."""

    name: str
    start_value: float
    end_value: float
    duration: float
    easing: EasingFunction = EasingFunction.LINEAR
    start_time: float = 0.0
    current_value: float = 0.0
    state: AnimationState = AnimationState.IDLE
    loop: bool = False
    reverse: bool = False
    on_complete: Callable | None = None
    on_update: Callable | None = None


class Easing:
    """Easing function implementations."""

    @staticmethod
    def linear(t: float) -> float:
        """Linear interpolation."""
        return t

    @staticmethod
    def ease_in_quad(t: float) -> float:
        """Quadratic ease in."""
        return t * t

    @staticmethod
    def ease_out_quad(t: float) -> float:
        """Quadratic ease out."""
        return t * (2 - t)

    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """Quadratic ease in-out."""
        return t * t * (3 - 2 * t)

    @staticmethod
    def ease_in_cubic(t: float) -> float:
        """Cubic ease in."""
        return t * t * t

    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """Cubic ease out."""
        return (t - 1) * (t - 1) * (t - 1) + 1

    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        """Cubic ease in-out."""
        if t < 0.5:
            return 4 * t * t * t
        return 1 + (t - 1) * (2 * (t - 1)) * (2 * (t - 1))

    @staticmethod
    def ease_in_sine(t: float) -> float:
        """Sine ease in."""
        import math

        return 1 - math.cos(t * math.pi / 2)

    @staticmethod
    def ease_out_sine(t: float) -> float:
        """Sine ease out."""
        import math

        return math.sin(t * math.pi / 2)

    @staticmethod
    def ease_in_out_sine(t: float) -> float:
        """Sine ease in-out."""
        import math

        return -(math.cos(math.pi * t) - 1) / 2

    @staticmethod
    def ease_in_expo(t: float) -> float:
        """Exponential ease in."""
        return 0 if t == 0 else pow(2, 10 * (t - 1))

    @staticmethod
    def ease_out_expo(t: float) -> float:
        """Exponential ease out."""
        return 1 if t == 1 else 1 - pow(2, -10 * t)

    @staticmethod
    def ease_in_out_expo(t: float) -> float:
        """Exponential ease in-out."""
        if t == 0 or t == 1:
            return t
        if t < 0.5:
            return pow(2, 20 * t - 10) / 2
        return (2 - pow(2, -20 * t + 10)) / 2

    @staticmethod
    def bounce(t: float) -> float:
        """Bounce ease out."""
        if t < 1 / 2.75:
            return 7.5625 * t * t
        elif t < 2 / 2.75:
            t -= 1.5 / 2.75
            return 7.5625 * t * t + 0.75
        elif t < 2.5 / 2.75:
            t -= 2.25 / 2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625 / 2.75
            return 7.5625 * t * t + 0.984375

    @staticmethod
    def elastic(t: float) -> float:
        """Elastic ease out."""
        import math

        if t == 0 or t == 1:
            return t
        return pow(2, -10 * t) * math.sin((t - 0.1) * 5 * math.pi) + 1

    @staticmethod
    def apply(easing: EasingFunction, t: float) -> float:
        """Apply easing function."""
        if easing == EasingFunction.LINEAR:
            return Easing.linear(t)
        elif easing == EasingFunction.EASE_IN_QUAD:
            return Easing.ease_in_quad(t)
        elif easing == EasingFunction.EASE_OUT_QUAD:
            return Easing.ease_out_quad(t)
        elif easing == EasingFunction.EASE_IN_OUT_QUAD:
            return Easing.ease_in_out_quad(t)
        elif easing == EasingFunction.EASE_IN_CUBIC:
            return Easing.ease_in_cubic(t)
        elif easing == EasingFunction.EASE_OUT_CUBIC:
            return Easing.ease_out_cubic(t)
        elif easing == EasingFunction.EASE_IN_OUT_CUBIC:
            return Easing.ease_in_out_cubic(t)
        elif easing == EasingFunction.EASE_IN_SINE:
            return Easing.ease_in_sine(t)
        elif easing == EasingFunction.EASE_OUT_SINE:
            return Easing.ease_out_sine(t)
        elif easing == EasingFunction.EASE_IN_OUT_SINE:
            return Easing.ease_in_out_sine(t)
        elif easing == EasingFunction.EASE_IN_EXPO:
            return Easing.ease_in_expo(t)
        elif easing == EasingFunction.EASE_OUT_EXPO:
            return Easing.ease_out_expo(t)
        elif easing == EasingFunction.EASE_IN_OUT_EXPO:
            return Easing.ease_in_out_expo(t)
        elif easing == EasingFunction.BOUNCE:
            return Easing.bounce(t)
        elif easing == EasingFunction.ELASTIC:
            return Easing.elastic(t)
        else:
            return Easing.linear(t)


class AnimationManager:
    """Manager for animations."""

    def __init__(self):
        """Initialize animation manager."""
        self.animations: dict[str, Animation] = {}
        logger.debug("Initialized AnimationManager")

    def create(
        self,
        name: str,
        start_value: float,
        end_value: float,
        duration: float,
        easing: EasingFunction = EasingFunction.LINEAR,
        loop: bool = False,
        reverse: bool = False,
        on_complete: Callable | None = None,
        on_update: Callable | None = None,
    ) -> Animation:
        """
        Create a new animation.

        Args:
            name: Unique animation name
            start_value: Starting value
            end_value: Ending value
            duration: Duration in seconds
            easing: Easing function
            loop: Loop the animation
            reverse: Reverse on loop
            on_complete: Callback when animation completes
            on_update: Callback on each update

        Returns:
            Created animation
        """
        animation = Animation(
            name=name,
            start_value=start_value,
            end_value=end_value,
            duration=duration,
            easing=easing,
            current_value=start_value,
            loop=loop,
            reverse=reverse,
            on_complete=on_complete,
            on_update=on_update,
        )
        self.animations[name] = animation
        logger.debug(f"Created animation: {name}")
        return animation

    def start(self, name: str) -> bool:
        """
        Start an animation.

        Args:
            name: Animation name

        Returns:
            True if started successfully
        """
        if name not in self.animations:
            logger.warning(f"Animation not found: {name}")
            return False

        animation = self.animations[name]
        animation.state = AnimationState.RUNNING
        animation.start_time = imgui.get_time()
        animation.current_value = animation.start_value
        logger.debug(f"Started animation: {name}")
        return True

    def pause(self, name: str) -> bool:
        """Pause an animation."""
        if name not in self.animations:
            return False

        self.animations[name].state = AnimationState.PAUSED
        return True

    def resume(self, name: str) -> bool:
        """Resume a paused animation."""
        if name not in self.animations:
            return False

        animation = self.animations[name]
        if animation.state == AnimationState.PAUSED:
            animation.state = AnimationState.RUNNING
            return True
        return False

    def stop(self, name: str) -> bool:
        """Stop an animation."""
        if name not in self.animations:
            return False

        animation = self.animations[name]
        animation.state = AnimationState.COMPLETED
        animation.current_value = animation.end_value
        if animation.on_complete:
            animation.on_complete()
        return True

    def update(self) -> None:
        """Update all animations."""
        current_time = imgui.get_time()

        for animation in self.animations.values():
            if animation.state != AnimationState.RUNNING:
                continue

            # Calculate progress
            elapsed = current_time - animation.start_time
            progress = min(elapsed / animation.duration, 1.0)

            # Apply easing
            eased_progress = Easing.apply(animation.easing, progress)

            # Calculate current value
            animation.current_value = (
                animation.start_value
                + (animation.end_value - animation.start_value) * eased_progress
            )

            # Call update callback
            if animation.on_update:
                animation.on_update(animation.current_value)

            # Check if completed
            if progress >= 1.0:
                if animation.loop:
                    # Restart animation
                    animation.start_time = current_time
                    if animation.reverse:
                        # Swap start and end
                        animation.start_value, animation.end_value = (
                            animation.end_value,
                            animation.start_value,
                        )
                else:
                    animation.state = AnimationState.COMPLETED
                    if animation.on_complete:
                        animation.on_complete()

    def get_value(self, name: str) -> float | None:
        """Get current animation value."""
        if name not in self.animations:
            return None
        return self.animations[name].current_value

    def is_running(self, name: str) -> bool:
        """Check if animation is running."""
        if name not in self.animations:
            return False
        return self.animations[name].state == AnimationState.RUNNING

    def remove(self, name: str) -> bool:
        """Remove an animation."""
        if name in self.animations:
            del self.animations[name]
            logger.debug(f"Removed animation: {name}")
            return True
        return False

    def clear(self) -> None:
        """Clear all animations."""
        self.animations.clear()
        logger.debug("Cleared all animations")


class AnimatedValue:
    """Helper class for animated values."""

    def __init__(
        self,
        initial_value: float,
        manager: AnimationManager,
        name: str | None = None,
    ):
        """
        Initialize animated value.

        Args:
            initial_value: Initial value
            manager: Animation manager
            name: Value name (auto-generated if None)
        """
        self.manager = manager
        self.name = name or f"animated_value_{id(self)}"
        self._value = initial_value
        self._target = initial_value

    def animate_to(
        self,
        target: float,
        duration: float = 0.3,
        easing: EasingFunction = EasingFunction.EASE_OUT_QUAD,
    ) -> None:
        """
        Animate to target value.

        Args:
            target: Target value
            duration: Animation duration
            easing: Easing function
        """
        self._target = target

        # Create or update animation
        self.manager.create(
            name=self.name,
            start_value=self._value,
            end_value=target,
            duration=duration,
            easing=easing,
            on_update=lambda v: setattr(self, "_value", v),
        )
        self.manager.start(self.name)

    def get(self) -> float:
        """Get current value."""
        return self._value

    def set(self, value: float) -> None:
        """Set value directly (no animation)."""
        self._value = value
        self._target = value


class TransitionGroup:
    """Group of animations that can be controlled together."""

    def __init__(self, manager: AnimationManager):
        """Initialize transition group."""
        self.manager = manager
        self.animation_names: list[str] = []

    def add_animation(
        self,
        name: str,
        start_value: float,
        end_value: float,
        duration: float,
        easing: EasingFunction = EasingFunction.LINEAR,
    ) -> None:
        """Add animation to group."""
        self.manager.create(
            name=name,
            start_value=start_value,
            end_value=end_value,
            duration=duration,
            easing=easing,
        )
        self.animation_names.append(name)

    def start_all(self) -> None:
        """Start all animations in group."""
        for name in self.animation_names:
            self.manager.start(name)

    def stop_all(self) -> None:
        """Stop all animations in group."""
        for name in self.animation_names:
            self.manager.stop(name)

    def pause_all(self) -> None:
        """Pause all animations in group."""
        for name in self.animation_names:
            self.manager.pause(name)

    def resume_all(self) -> None:
        """Resume all animations in group."""
        for name in self.animation_names:
            self.manager.resume(name)

    def are_all_complete(self) -> bool:
        """Check if all animations are complete."""
        return all(not self.manager.is_running(name) for name in self.animation_names)

"""Data binding system for reactive UI updates."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from blinker import Signal
from loguru import logger


@dataclass
class BindingConfig:
    """Configuration for a data binding."""

    source_path: str  # Path to source data (e.g., "user.name")
    target_widget: str  # Widget ID
    target_property: str  # Property name (e.g., "text", "value")
    transform: Callable[[Any], Any] | None = None  # Transform function
    bidirectional: bool = False  # Two-way binding


class DataStore:
    """Reactive data store with change notifications."""

    def __init__(self):
        """Initialize data store."""
        self._data: dict[str, Any] = {}
        self._signals: dict[str, Signal] = {}
        logger.debug("Initialized DataStore")

    def set(self, path: str, value: Any) -> None:
        """
        Set a value and notify listeners.

        Args:
            path: Data path (e.g., "user.name")
            value: New value
        """
        # Set the value
        self._set_nested(path, value)

        # Emit signal
        if path not in self._signals:
            self._signals[path] = Signal()
        self._signals[path].send(self, path=path, value=value)

        logger.debug(f"DataStore set: {path} = {value}")

    def get(self, path: str, default: Any = None) -> Any:
        """
        Get a value from the store.

        Args:
            path: Data path
            default: Default value if not found

        Returns:
            Value at path or default
        """
        return self._get_nested(path, default)

    def subscribe(self, path: str, callback: Callable) -> None:
        """
        Subscribe to changes at a path.

        Args:
            path: Data path to watch
            callback: Function to call on changes
        """
        if path not in self._signals:
            self._signals[path] = Signal()
        self._signals[path].connect(callback)
        logger.debug(f"Subscribed to {path}")

    def unsubscribe(self, path: str, callback: Callable) -> None:
        """
        Unsubscribe from changes.

        Args:
            path: Data path
            callback: Callback to remove
        """
        if path in self._signals:
            self._signals[path].disconnect(callback)
            logger.debug(f"Unsubscribed from {path}")

    def delete(self, path: str) -> bool:
        """
        Delete a value from the store.

        Args:
            path: Data path to delete

        Returns:
            True if deleted, False if not found
        """
        try:
            parts = path.split(".")
            if len(parts) == 1:
                if path in self._data:
                    del self._data[path]
                    return True
                return False

            # Navigate to parent
            current = self._data
            for part in parts[:-1]:
                if part not in current:
                    return False
                current = current[part]

            # Delete final key
            final_key = parts[-1]
            if final_key in current:
                del current[final_key]
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting {path}: {e}")
            return False

    def clear(self) -> None:
        """Clear all data."""
        self._data.clear()
        self._signals.clear()
        logger.debug("Cleared DataStore")

    def _set_nested(self, path: str, value: Any) -> None:
        """Set nested value using dot notation."""
        parts = path.split(".")
        current = self._data

        # Navigate/create structure
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]

        # Set final value
        current[parts[-1]] = value

    def _get_nested(self, path: str, default: Any = None) -> Any:
        """Get nested value using dot notation."""
        parts = path.split(".")
        current = self._data

        try:
            for part in parts:
                current = current[part]
            return current
        except (KeyError, TypeError):
            return default

    def to_dict(self) -> dict[str, Any]:
        """Export data as dictionary."""
        return self._data.copy()

    def from_dict(self, data: dict[str, Any]) -> None:
        """Import data from dictionary."""
        self._data = data.copy()
        logger.debug("Imported data to DataStore")


class BindingManager:
    """Manager for widget data bindings."""

    def __init__(self, data_store: DataStore):
        """
        Initialize binding manager.

        Args:
            data_store: DataStore instance
        """
        self.data_store = data_store
        self.bindings: dict[str, list[BindingConfig]] = {}
        logger.debug("Initialized BindingManager")

    def bind(
        self,
        source_path: str,
        target_widget: str,
        target_property: str,
        transform: Callable | None = None,
        bidirectional: bool = False,
    ) -> None:
        """
        Create a data binding.

        Args:
            source_path: Path in data store
            target_widget: Widget ID
            target_property: Widget property to bind
            transform: Optional transform function
            bidirectional: Enable two-way binding
        """
        binding = BindingConfig(
            source_path=source_path,
            target_widget=target_widget,
            target_property=target_property,
            transform=transform,
            bidirectional=bidirectional,
        )

        if source_path not in self.bindings:
            self.bindings[source_path] = []
        self.bindings[source_path].append(binding)

        # Subscribe to data changes
        self.data_store.subscribe(source_path, self._on_data_change)

        logger.debug(
            f"Created binding: {source_path} -> {target_widget}.{target_property}"
        )

    def unbind(self, source_path: str, target_widget: str | None = None) -> None:
        """
        Remove bindings.

        Args:
            source_path: Data path
            target_widget: Optional widget ID (removes all if None)
        """
        if source_path not in self.bindings:
            return

        if target_widget:
            # Remove specific widget binding
            self.bindings[source_path] = [
                b
                for b in self.bindings[source_path]
                if b.target_widget != target_widget
            ]
        else:
            # Remove all bindings for path
            del self.bindings[source_path]
            self.data_store.unsubscribe(source_path, self._on_data_change)

        logger.debug(f"Removed binding for {source_path}")

    def _on_data_change(self, sender, **kwargs) -> None:
        """Handle data store changes."""
        path = kwargs.get("path")
        value = kwargs.get("value")

        if path not in self.bindings:
            return

        # Update all bound widgets
        for binding in self.bindings[path]:
            # Apply transform if provided
            final_value = binding.transform(value) if binding.transform else value

            # Update widget property
            self._update_widget_property(
                binding.target_widget, binding.target_property, final_value
            )

    def _update_widget_property(
        self, widget_id: str, property_name: str, value: Any
    ) -> None:
        """
        Update a widget property.

        Note: This would need access to the widget registry.
        For now, this is a placeholder that emits a signal.
        """
        # Emit signal that can be caught by canvas/widget manager
        from champi_gen_ui.core.state import widget_updated

        widget_updated.send(
            self, widget_id=widget_id, property=property_name, value=value
        )

    def get_bindings(self, source_path: str) -> list[BindingConfig]:
        """Get all bindings for a data path."""
        return self.bindings.get(source_path, [])

    def clear(self) -> None:
        """Clear all bindings."""
        self.bindings.clear()
        logger.debug("Cleared all bindings")


class ComputedProperty:
    """Computed property that updates when dependencies change."""

    def __init__(
        self,
        name: str,
        dependencies: list[str],
        compute_fn: Callable,
        data_store: DataStore,
    ):
        """
        Initialize computed property.

        Args:
            name: Property name/path
            dependencies: List of data paths to watch
            compute_fn: Function to compute value
            data_store: DataStore instance
        """
        self.name = name
        self.dependencies = dependencies
        self.compute_fn = compute_fn
        self.data_store = data_store

        # Subscribe to all dependencies
        for dep in dependencies:
            data_store.subscribe(dep, self._recompute)

        # Initial computation
        self._recompute()

    def _recompute(self, *args, **kwargs) -> None:
        """Recompute the property value."""
        # Get all dependency values
        dep_values = {dep: self.data_store.get(dep) for dep in self.dependencies}

        # Compute new value
        try:
            new_value = self.compute_fn(**dep_values)
            self.data_store.set(self.name, new_value)
        except Exception as e:
            logger.error(f"Error computing {self.name}: {e}")


class Validator:
    """Validation for data binding."""

    @staticmethod
    def required(value: Any) -> bool:
        """Check if value is not None/empty."""
        if value is None:
            return False
        if isinstance(value, str):
            return len(value.strip()) > 0
        return True

    @staticmethod
    def min_length(min_len: int) -> Callable:
        """Create min length validator."""

        def validate(value: Any) -> bool:
            if not isinstance(value, str | list | tuple):
                return False
            return len(value) >= min_len

        return validate

    @staticmethod
    def max_length(max_len: int) -> Callable:
        """Create max length validator."""

        def validate(value: Any) -> bool:
            if not isinstance(value, str | list | tuple):
                return False
            return len(value) <= max_len

        return validate

    @staticmethod
    def range_validator(min_val: float, max_val: float) -> Callable:
        """Create range validator."""

        def validate(value: Any) -> bool:
            try:
                num_val = float(value)
                return min_val <= num_val <= max_val
            except (ValueError, TypeError):
                return False

        return validate

    @staticmethod
    def email(value: str) -> bool:
        """Validate email format."""
        import re

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, str(value)))


class ValidationManager:
    """Manager for data validation."""

    def __init__(self):
        """Initialize validation manager."""
        self.validators: dict[str, list[Callable]] = {}
        self.errors: dict[str, list[str]] = {}
        logger.debug("Initialized ValidationManager")

    def add_validator(
        self, path: str, validator: Callable, error_msg: str | None = None
    ):
        """
        Add a validator for a data path.

        Args:
            path: Data path
            validator: Validation function
            error_msg: Error message if validation fails
        """
        if path not in self.validators:
            self.validators[path] = []

        # Wrap validator with error message
        def wrapped_validator(value):
            result = validator(value)
            if not result and error_msg:
                self.add_error(path, error_msg)
            return result

        self.validators[path].append(wrapped_validator)

    def validate(self, path: str, value: Any) -> bool:
        """
        Validate a value.

        Args:
            path: Data path
            value: Value to validate

        Returns:
            True if valid, False otherwise
        """
        if path not in self.validators:
            return True

        # Clear previous errors
        if path in self.errors:
            del self.errors[path]

        # Run all validators
        return all(validator(value) for validator in self.validators[path])

    def add_error(self, path: str, error: str) -> None:
        """Add validation error."""
        if path not in self.errors:
            self.errors[path] = []
        self.errors[path].append(error)

    def get_errors(self, path: str) -> list[str]:
        """Get validation errors for a path."""
        return self.errors.get(path, [])

    def has_errors(self, path: str | None = None) -> bool:
        """Check if there are errors."""
        if path:
            return path in self.errors and len(self.errors[path]) > 0
        return len(self.errors) > 0

    def clear_errors(self, path: str | None = None) -> None:
        """Clear errors."""
        if path:
            if path in self.errors:
                del self.errors[path]
        else:
            self.errors.clear()

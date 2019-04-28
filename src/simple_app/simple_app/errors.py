"""Module contains all custom exceptions raised from simple_app package."""

__all__ = (
    'InvalidConfigurationError',
)


class InvalidConfigurationError(Exception):
    """Error raised when unable to parse provided configuration file."""

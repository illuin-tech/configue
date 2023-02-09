class ConfigueError(Exception):
    pass


class SubPathNotFound(ConfigueError):
    pass


class NonCallableError(ConfigueError):
    pass


class ConfigueRecursionError(ConfigueError):
    pass


class NotFoundError(ConfigueError):
    pass


class InvalidNodeType(Exception):
    pass

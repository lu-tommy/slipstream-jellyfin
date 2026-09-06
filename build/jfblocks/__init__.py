"""Payload constants for jf_patch.py, grouped by feature area.

Every module is imported here in the original definition order. Each
declares an explicit __all__ so underscore-prefixed blocks (_LS_01..16)
are re-exported too -- `import *` alone would silently skip them.
"""
from .livetv import *  # noqa: F401,F403
from .home import *  # noqa: F401,F403
from .misc import *  # noqa: F401,F403
from .livesports import *  # noqa: F401,F403
from .shell import *  # noqa: F401,F403
from .i18n import *  # noqa: F401,F403
from .search import *  # noqa: F401,F403
from .audiobook import *  # noqa: F401,F403
from .music import *  # noqa: F401,F403

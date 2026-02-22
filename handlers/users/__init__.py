import aiogram

router = aiogram.Router()

from .start import *
from .cats import *
from .make_order import *
from .help import *
from .hacking import *
from .quiz import *
from .admin_commands import *
from .reactions import *
from .orders import *
from .admin import *
from .advertisement import *
from .feedback import *
from .statistics import *
from .ref_link import *

from .echo import *
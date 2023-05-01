from src.bot import dp
from src.filters import BotAdminFilter
from src.keys import TextKeyFilter
from src.i18n import i18n

dp.bind_filter(TextKeyFilter, )
dp.bind_filter(BotAdminFilter, )
dp.middleware.setup(i18n)

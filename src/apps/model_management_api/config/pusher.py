import pusher
from src.config.settings import settings

pusher_client = pusher.Pusher(
  app_id=settings.PUSHER_APP_ID,
  key=settings.PUSHER_APP_KEY,
  secret=settings.PUSHER_APP_SECRET,
  cluster=settings.PUSHER_APP_CLUSTER,
  ssl=True
)
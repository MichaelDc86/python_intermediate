import settings


DEFAULT_SECRET_KEY = 'zp5bK7Ah'.encode()

SECRET_KEY = getattr(settings, 'SECRET_KEY', DEFAULT_SECRET_KEY)

from .Youtube.youtube import YouTube
from .Youtube.database import Database

assert all((YouTube, Database))

name = "wildbook_social"
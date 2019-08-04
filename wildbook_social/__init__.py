from .Youtube.youtube import YouTube
from .Database.database import Database

assert all((YouTube, Database))

name = "wildbook_social"
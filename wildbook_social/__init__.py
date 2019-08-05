from .Youtube.youtube import YouTube
from .Twitter.twitter import Twitter
from .Database.database import Database

assert all((YouTube, Twitter, Database))

name = "wildbook_social"
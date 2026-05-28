"""Data models"""

from app.models.joke import Joke
from app.models.rating import JokeRating
from app.models.favorite import Favorite

__all__ = ["Joke", "JokeRating", "Favorite"]

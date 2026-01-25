from . import admin, auth, activity, team, team_member, operator, lookups, explorer
from typing import Annotated, Literal

from fastapi import Query
from fastapi import APIRouter, Depends, status
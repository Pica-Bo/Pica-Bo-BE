from pydantic import BaseModel as _BaseModel, Field, field_validator
from bson import ObjectId
from typing import Optional, List
from datetime import datetime
from datetime import date, datetime

class PB_BaseModel(_BaseModel):
    @field_validator("id", mode="before", check_fields=False)
    def convert_objectid_to_str(cls, v):
        return str(v)
    
    # Pydantic v2 configuration: prefer `model_config` to avoid v1->v2 warnings
    model_config = {"from_attributes": True}

class ListingQuery(_BaseModel):
    page: int = Field(1, ge=1, description="Page number, starting from 1.")
    page_size: int = Field(20, ge=1, le=200, description="Number of items per page (max 200).")

    @field_validator("page_size")
    def page_size_max_200(cls, v):
        if v > 200:
            raise ValueError("page_size cannot be more than 200 items.")
        return v

    model_config = {
        "populate_by_name": True
    }
    
class ListingResult(PB_BaseModel):
    total: int = Field(..., description="Total number of items available.")
    items: List = Field(..., description="List of items for the current page.")
    page: int = Field(..., description="Current page number.")
    page_size: int = Field(..., description="Number of items per page.")
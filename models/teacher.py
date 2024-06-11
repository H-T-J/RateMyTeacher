from fastapi import Request
from pydantic import BaseModel
from beanie import Document, Indexed

from typing import List


class Review(BaseModel):
    title: str
    body: str
    rating: float
    amount_of_self_study: float
    amount_of_study_guide: float
    late_work_strictness: float
    time_to_grade: float


class ReviewForm:

    def __init__(self, request: Request):
        self.request: Request = request
        self.form_data = {}

    async def create_form_data(self):
        form = await self.request.form()
        for (key, value) in form.items():
            if key in ["rating", "amount_of_self_study", "amount_of_study_guide", "late_work_strictness", "time_to_grade"]:
                self.form_data[key] = float(value)
            else:
                self.form_data[key] = value


class Teachers(Document):
    name: Indexed(str, unique=True)
    subjects: str
    years_at_smic_hset: int
    is_full_time: bool
    no_of_reviews: int = 0
    reviews_list: List[Review] = []

    class Settings:
        name = "teachers"


class TeacherForm:

    def __init__(self, request: Request):
        self.request: Request = request
        self.form_data = {}

    async def create_form_data(self):
        form = await self.request.form()
        for (key, value) in form.items():
            self.form_data[key] = value

        if "is_full_time" in self.form_data:
            self.form_data["is_full_time"] = True
        else:
            self.form_data["is_full_time"] = False

        self.form_data["years_at_smic_hset"] = int(self.form_data["years_at_smic_hset"])

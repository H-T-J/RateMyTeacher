from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models.teacher import Teachers, TeacherForm, ReviewForm, Review

router = APIRouter(prefix="", tags=["home"])
templates = Jinja2Templates(directory="templates")


@router.get(path="/", response_class=HTMLResponse)
async def get_index(request: Request):
    teachers = await Teachers.find().to_list()
    # print(teachers)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "teachers": teachers
        }
    )


@router.get("/teachers/delete/{teacher_id}", response_class=RedirectResponse)
async def remove_teacher(teacher_id: str):

    try:
        teacher = await Teachers.get(teacher_id)
        await teacher.delete()
        return RedirectResponse(url="/")

    except Exception as err:
        return RedirectResponse(url=f"/teachers/{teacher_id}")


@router.get(path="/teachers/add", response_class=HTMLResponse)
async def get_teacher_add(request: Request):
    return templates.TemplateResponse(
        "teacher_add.html",
        {"request": request}
    )


@router.post(path="/teachers/add", response_class=HTMLResponse)
async def add_teacher(request: Request):
    form = TeacherForm(request=request)

    await form.create_form_data()

    new_teacher = Teachers(
        name=form.form_data["name"],
        subjects=form.form_data["subjects"],
        years_at_smic_hset=form.form_data["years_at_smic_hset"],
        is_full_time=form.form_data["is_full_time"],
        image_link=form.form_data["image_link"]
    )

    try:
        await new_teacher.insert()
        return templates.TemplateResponse("teacher_add.html",
            {
                "request": request,
                "msg": "Success"
            }
        )
    except Exception as err:
        return templates.TemplateResponse("teacher_add.html",
            {
                "request": request,
                "msg": "Error",
                "err": err
            }
        )


@router.post("/teachers/{teacher_id}/new_review", response_class=HTMLResponse)
async def new_review(request: Request, teacher_id: str):
    teacher = await Teachers.get(teacher_id)

    try:

        form = ReviewForm(request=request)
        await form.create_form_data()

        print(form.form_data)

        review = Review(
            rating=form.form_data["rating"],
            title=form.form_data["title"],
            body=form.form_data["body"],
            amount_of_self_study=form.form_data["amount_of_self_study"],
            amount_of_study_guide=form.form_data["amount_of_study_guide"],
            late_work_strictness=form.form_data["late_work_strictness"],
            time_to_grade=form.form_data["time_to_grade"]
        )

        teacher.reviews_list.append(review)
        teacher.no_of_reviews = len(teacher.reviews_list)

        print("Everything was updated")

        await teacher.save()

        return RedirectResponse(url=f"/teachers/{teacher_id}", status_code=303)

    except Exception as err:
        print(err)
        return templates.TemplateResponse("teacher_update.html",
            {
                "request": request,
                "teacher": teacher
            }
        )


@router.get(path="/teachers/{teacher_id}", response_class=HTMLResponse)
async def get_teacher_by_id(request: Request, teacher_id: str):
    teacher = await Teachers.get(teacher_id)

    return templates.TemplateResponse(
        "teacher_info.html",
        {
            "request": request,
            "teacher": teacher
        }
    )


@router.get(path="/teachers/update/{teacher_id}", response_class=HTMLResponse)
async def get_update_teacher_page(request: Request, teacher_id: str):
    teacher = await Teachers.get(teacher_id)

    return templates.TemplateResponse(
        "teacher_update.html",
        {
            "request": request,
            "teacher": teacher
        }
    )

import sqlalchemy as sa
from config.database import get_session
from fastapi import APIRouter, HTTPException, status
from models.student import Student
from models.user import Student
from schemas.car import CarOut
from schemas.student import StudentUpdate

student_router = APIRouter(
    prefix="/student",
    tags=["Student"],
)


@student_router.get(
    path="/",
    summary="Get all",
)
def get_all():
    with get_session() as s:
        stmt = sa.select(Student)
        result = s.scalars(stmt).all()

        return list(result)


@student_router.get(
    "/{student_id}/cars",
    summary="Get all cars by student_id",
    response_model=list[CarOut],
)
def get_cars_by_student_id(student_id: int):
    with get_session() as s:
        stmt = sa.select(Student).where(Student.id == student_id)
        result = s.scalars(stmt).first()

        if result is None:
            return
        for c in result.cars:
            print(c)
        return result.cars


@student_router.put(
    "/{student_id}",
    summary="Update a student",
)
def update_student_by_id(student_id: int, new_student: StudentUpdate):
    with get_session() as s:
        student_to_update = s.scalars(
            sa.select(Student).where(Student.id == student_id)
        ).first()
        if not student_to_update:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user_id not found: '{student_id}'",
            )
        stmt = (
            sa.update(Student)
            .where(Student.id == student_id)
            .values(
                firstname=new_student.firstname or student_to_update.firstname,
                lastname=new_student.lastname or student_to_update.lastname,
                school_id=new_student.school_id or student_to_update.school_id,
                address_id=new_student.address_id
                or student_to_update.address_id,
                email=new_student.email or student_to_update.email,
                driving_licence_nb=new_student.driving_licence_nb
                or student_to_update.driving_licence_nb,
                driving_licence_validity=new_student.driving_licence_validity
                or student_to_update.driving_licence_validity,
            )
        )
        s.execute(stmt)
        s.commit()
        return {"msg": f"Updated student: '{student_id}'"}

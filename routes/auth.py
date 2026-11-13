import os
import uuid
from typing import List

from fastapi import APIRouter, File, Form, UploadFile

import database

router = APIRouter()


@router.post("/complete-signup")
async def complete_signup(
    name: str = Form(...),
    lastname: str = Form(...),
    id: int = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    images: List[UploadFile] = File(...),
):
    if database.exists("email", email):
        return {"status": "error", "message": "البريد الإلكتروني مستخدم مسبقاً، يرجى استخدام بريد آخر."}
    if database.exists("id", id):
        return {"status": "error", "message": "الرقم الجامعي مسجل مسبقاً."}
    if database.name_exists(name, lastname):
        return {"status": "error", "message": "يوجد مستخدم مسجل بنفس الاسم والكنية تماماً."}

    user_dir = os.path.join("dataset", str(id))
    os.makedirs(user_dir, exist_ok=True)
    for i, img in enumerate(images):
        with open(os.path.join(user_dir, f"img_{i + 1}.jpg"), "wb") as f:
            f.write(await img.read())

    database.create_user(name, lastname, id, email, password)
    session_id = str(uuid.uuid4())
    database.create_session(session_id, id)
    return {"status": "success", "session_id": session_id}


@router.post("/login-check")
async def login_check(email: str = Form(...), password: str = Form(...)):
    user = database.check_login(email, password)
    if not user:
        return {"status": "error", "message": "البريد الإلكتروني أو كلمة المرور غير صحيحة"}

    session_id = str(uuid.uuid4())
    database.create_session(session_id, user[0])
    return {"status": "success", "session_id": session_id}


@router.post("/verify-session")
async def verify_session(session_id: str = Form(...)):
    user = database.get_user_by_session(session_id)
    if not user:
        return {"status": "invalid"}
    return {
        "status": "valid",
        "user": {"name": user[0], "lastname": user[1], "id": user[2], "email": user[3]},
    }


@router.post("/logout")
async def logout(session_id: str = Form(...)):
    database.delete_session(session_id)
    return {"status": "success"}

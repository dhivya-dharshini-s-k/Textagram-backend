from fastapi import Depends,APIRouter
from  utils.sessions import get_current_user, admin_required

router=APIRouter()

@router.get("/admin")
def admin_only_route(current_user: dict = Depends(admin_required)):
    return {"message": f"Hello Admin {current_user['username']}"}

@router.get("/profile")
def user_profile(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['username']}, your role id is {current_user['role_id']}"}


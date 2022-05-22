from aituNetwork.users import users
from aituNetwork.models import Users, ProfilePictures


@users.app_template_global()
def get_user(user_id: int):
    return Users.get(user_id)


@users.app_template_global()
def get_picture(user_id: int):
    return ProfilePictures.get_profile_picture(user_id)


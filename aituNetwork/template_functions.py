from aituNetwork.models import Users, ProfilePictures, PostLikes, UsersChats, Messages, Friends, Cities, EduPrograms, Admins


def get_user(user_id: int):
    return Users.get(user_id)


def is_user_liked(user_id: int, post_id: int):
    if PostLikes.get_post_like(user_id, post_id) is not None:
        return True
    return False


def get_picture(user_id: int):
    return ProfilePictures.get_profile_picture(user_id)


def get_second_chat_user(chat_id: int, user_id: int):
    return UsersChats.get_second_chat_user(chat_id, user_id)


def get_last_message(chat_id: int):
    return Messages.get_last_message(chat_id)


def is_friend(user_id: int, friend_id: int):
    return Friends.is_friend(user_id, friend_id)


def get_city_name(city_id: int):
    return Cities.get_city(city_id).name


def get_edu_program_name(edu_program_id: int):
    return EduPrograms.get_edu_program(edu_program_id).name


def is_admin(user_id: int):
    return Admins.is_admin(user_id)

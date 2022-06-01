function confirm_delete() {
    let result = prompt('To delete user, write "DELETE"');
    window.location.replace('/users/delete_user/' + profile_user_id);
}
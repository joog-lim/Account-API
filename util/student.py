def get_generation_from_email(email: str) -> int:
    return int(email[1:3]) - 16


def get_is_student_from_email(email: str) -> bool:
    return email[0] == "s"

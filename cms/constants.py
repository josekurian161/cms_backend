from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")



email_id_regex = RegexValidator(
    regex=r'[\w\.-]+@[\w\.-]+(?:\.[\w]+)+',
    message="please enter valid email_id")

ADMIN, USER = ("admin", "user")
ROLES = ((ADMIN, "admin"), (USER, "user"))

BLOG_WRITER, BRAND_JOURNALIST, TECHNICAL_WRITER = (
    "blog_writer", "brand_journalist", "technical_writer"
)
CATEGORIES = (
    (BLOG_WRITER, "blog writer"), (BRAND_JOURNALIST, "brand journalist"), (TECHNICAL_WRITER, "technical writer"))

password_regex = RegexValidator(
    regex=r'^(?=.*?[A-Z])(?=.*?[a-z]).{8,8}$',
    message="please enter valid email_id")

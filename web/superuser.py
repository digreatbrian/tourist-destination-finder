"""
Automatically create super user safely from environment variables.
"""
import os

from django.contrib.auth import get_user_model
from duck.logging import logger


def create_superuser():
    """
    Creates a Django superuser.

    Requirements:
        - SUPERUSER_USERNAME (required)
        - SUPERUSER_PWD (required)
        - SUPERUSER_EMAIL (optional)
    """
    username = os.getenv("SUPERUSER_USERNAME")
    password = os.getenv("SUPERUSER_PWD")
    email = os.getenv("SUPERUSER_EMAIL", "")

    # Fail fast if required variables are missing
    if not username or not password:
        logger.log(
            "Missing required environment variables: "
            + "SUPERUSER_USERNAME and/or SUPERUSER_PWD",
            level=logger.ERROR,
        )
        
        # Stop further processing
        return
    
    # Now attempt creating super user
    User = get_user_model()

    if User.objects.filter(username=username).exists():
        logger.log("Superuser already exists.", level=logger.WARNING)
        return

    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )

    logger.log("Superuser created successfully.", level=logger.SUCCESS)


if __name__ == "__main__":
    create_superuser()

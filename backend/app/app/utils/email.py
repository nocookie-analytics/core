from datetime import date
import logging
from pathlib import Path
from typing import Any, Dict

import emails
from emails.template import JinjaTemplate
from furl import furl

from app.core.config import settings
from app.logger import logger


def send_new_account_email(email_to: str, username: str) -> None:
    link = settings.SERVER_HOST
    if not link:
        logger.error("No server host provided, please set SERVER_NAME in config")
        return
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    docs_link = furl(link).add(path="/docs")
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "email": email_to,
            "link": link,
            "docs_link": str(docs_link),
        },
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    server_host = settings.SERVER_HOST
    if not server_host:
        logger.error("No server host provided, please set SERVER_NAME in config")
        return
    link = f"{server_host}/reset-password?token={token}"
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_trial_ending_email(email_to: str, trial_end_date: date) -> None:
    server_host = settings.SERVER_HOST
    if not server_host:
        logger.error("No server host provided, please set SERVER_NAME in config")
        return
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Trial ending soon"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "trial-ending.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "trial_end_date": trial_end_date,
            "link": settings.SERVER_HOST,
        },
    )


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")

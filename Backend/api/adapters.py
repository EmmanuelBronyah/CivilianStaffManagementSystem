from allauth.account.adapter import DefaultAccountAdapter
import logging


logger = logging.getLogger(__name__)


class CustomDefaultAccountAdapter(DefaultAccountAdapter):

    def format_email_subject(self, subject):
        subject = super().format_email_subject(subject)
        custom_subject = "Reset your CiviBase password"
        subject = custom_subject
        logger.debug(f"Password reset email subject({subject}) is set.")
        return subject

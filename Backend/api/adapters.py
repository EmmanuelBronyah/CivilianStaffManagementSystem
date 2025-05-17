from allauth.account.adapter import DefaultAccountAdapter


class CustomDefaultAccountAdapter(DefaultAccountAdapter):

    def format_email_subject(self, subject):
        custom_subject = "Reset your CiviBase password"
        subject = custom_subject
        return subject

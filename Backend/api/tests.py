from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser
from django.urls import reverse
from django.contrib.auth.models import Group
from django.core import mail
import re


class CreateUserAPITest(APITestCase):

    def setUp(self):
        self.url = reverse("register-user")
        self.user_data = {
            "fullname": "Savior Miles",
            "password": "lovesogreat",
            "username": "Saviour",
            "user_email": "Saviour@email.com",
            "role": "VIEWER",
            "grade": "COMPUTER TECHNICIAN GRADE III",
            "division": "DCE-IT",
        }
        Group.objects.create(name="Viewer")

    @staticmethod
    def modify_user_data(fullname, username, user_email, user_data):
        """
        User data dict is modified to avoid unique constraint errors on fields.
        """
        user_data.update(fullname=fullname, username=username, user_email=user_email)
        return user_data

    def test_create_user(self):
        user_data_copy = self.user_data.copy()
        response = self.client.post(self.url, user_data_copy, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username="Saviour").exists())

    def test_create_existing_user(self):
        user_data_copy = self.user_data.copy()
        response = self.client.post(self.url, user_data_copy, format="json")
        response = self.client.post(self.url, user_data_copy, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_omit_password_from_response(self):
        user_data_copy = self.user_data.copy()
        response = self.client.post(self.url, user_data_copy, format="json")
        del user_data_copy["password"]
        self.assertDictEqual(response.data, user_data_copy)

    def test_invalid_email_format(self):
        user_data_copy = self.user_data.copy()
        user_data_copy["user_email"] = "abc"
        response = self.client.post(self.url, user_data_copy, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_without_required_field(self):
        user_data_copy = self.user_data.copy()
        del user_data_copy["user_email"]
        response = self.client.post(self.url, user_data_copy, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_throttling(self):
        user_data_copy = self.user_data.copy()
        response = self.client.post(self.url, user_data_copy, format="json")
        response = self.client.post(self.url, user_data_copy, format="json")
        response = self.client.post(self.url, user_data_copy, format="json")
        response = self.client.post(self.url, user_data_copy, format="json")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class LoginAPITest(APITestCase):

    def setUp(self):
        self.login_url = reverse("user-login")
        self.register_url = reverse("register-user")

        self.user_data = {
            "fullname": "Savior Miles",
            "password": "lovesogreat",
            "username": "Saviour",
            "user_email": "Saviour@email.com",
            "role": "VIEWER",
            "grade": "COMPUTER TECHNICIAN GRADE III",
            "division": "DCE-IT",
        }
        self.login_data = {"username": "Saviour", "password": "lovesogreat"}
        Group.objects.create(name="Viewer")

    def test_login(self):
        self.client.post(self.register_url, self.user_data, format="json")
        response = self.client.post(self.login_url, self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("OTP sent to your email.", response.data["detail"])

    def test_not_registered_user(self):
        response = self.client.post(self.login_url, self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_throttling(self):
        self.client.post(self.register_url, self.user_data, format="json")
        response = self.client.post(self.login_url, self.login_data, format="json")
        response = self.client.post(self.login_url, self.login_data, format="json")
        response = self.client.post(self.login_url, self.login_data, format="json")
        response = self.client.post(self.login_url, self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class VerifyOTPAPITest(APITestCase):

    def setUp(self):
        self.login_url = reverse("user-login")
        self.register_url = reverse("register-user")
        self.verify_token_url = reverse("token-verification")

        self.user_data = {
            "fullname": "Savior Miles",
            "password": "lovesogreat",
            "username": "Saviour",
            "user_email": "Saviour@email.com",
            "role": "VIEWER",
            "grade": "COMPUTER TECHNICIAN GRADE III",
            "division": "DCE-IT",
        }
        self.login_data = {"username": "Saviour", "password": "lovesogreat"}
        Group.objects.create(name="Viewer")

    def retrieve_tokens(self):
        self.client.post(self.register_url, self.user_data, format="json")
        login_response = self.client.post(
            self.login_url, self.login_data, format="json"
        )
        temp_token = login_response.data.get("temp_token", None)
        email_body = mail.outbox[-1].body
        otp_token = re.search(r"\b\d{6}\b", email_body).group()
        return {"tokens": {"temp_token": temp_token, "otp_token": otp_token}}

    def test_verify_tokens(self):
        tokens = self.retrieve_tokens()
        otp_token, temp_token = tokens["tokens"].get("otp_token"), tokens["tokens"].get(
            "temp_token"
        )
        self.assertTrue(otp_token.isdigit())
        self.assertEqual(len(otp_token), 6)
        self.assertNotEqual(temp_token, "")
        response = self.client.post(self.verify_token_url, tokens, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh_token", response.data)
        self.assertIn("access_token", response.data)

    def test_throttling(self):
        tokens = self.retrieve_tokens()
        response = self.client.post(self.verify_token_url, tokens, format="json")
        response = self.client.post(self.verify_token_url, tokens, format="json")
        response = self.client.post(self.verify_token_url, tokens, format="json")
        response = self.client.post(self.verify_token_url, tokens, format="json")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class ResendOTPAPITest(APITestCase):

    def setUp(self):
        self.register_url = reverse("register-user")
        self.login_url = reverse("user-login")
        self.resend_otp_url = reverse("otp-resend")

        self.user_data = {
            "fullname": "Savior Miles",
            "password": "lovesogreat",
            "username": "Saviour",
            "user_email": "Saviour@email.com",
            "role": "VIEWER",
            "grade": "COMPUTER TECHNICIAN GRADE III",
            "division": "DCE-IT",
        }
        self.login_data = {"username": "Saviour", "password": "lovesogreat"}
        Group.objects.create(name="Viewer")

    def retrieve_temp_token(self):
        self.client.post(self.register_url, self.user_data, format="json")
        login_response = self.client.post(
            self.login_url, self.login_data, format="json"
        )
        temp_token = login_response.data.get("temp_token", None)
        return {"tokens": {"temp_token": temp_token}}

    def test_resend_otp(self):
        tokens = self.retrieve_temp_token()
        response = self.client.post(self.resend_otp_url, tokens, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("OTP sent to your email.", response.data["detail"])
        self.assertIsNot(response.data.get("temp_token", None), "")

    def test_throttling(self):
        tokens = self.retrieve_temp_token()
        response = self.client.post(self.resend_otp_url, tokens, format="json")
        response = self.client.post(self.resend_otp_url, tokens, format="json")
        response = self.client.post(self.resend_otp_url, tokens, format="json")
        response = self.client.post(self.resend_otp_url, tokens, format="json")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class PasswordResetConfirmAPITest(APITestCase):

    def setUp(self):
        self.register_url = reverse("register-user")
        self.password_reset_url = reverse("rest_password_reset")

        self.user_data = {
            "fullname": "Emmanuel Bronyah",
            "password": "lovesogreat",
            "username": "Emmanuel",
            "user_email": "emmanuelbronyah@yahoo.com",
            "role": "VIEWER",
            "grade": "COMPUTER TECHNICIAN GRADE III",
            "division": "DCE-IT",
        }
        Group.objects.create(name="Viewer")
        self.client.post(self.register_url, self.user_data, format="json")

    def retrieve_uidb64_and_token(self):
        email = CustomUser.objects.get(
            user_email="emmanuelbronyah@yahoo.com"
        ).user_email
        response = self.client.post(
            self.password_reset_url, {"email": email}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        email_body = mail.outbox[0].body
        match = re.search(
            r"/password/reset/confirm/redirect/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z\-]+)/",
            email_body,
        )
        self.assertIsNotNone(match)
        uidb64 = match.group("uidb64")
        token = match.group("token")
        return uidb64, token

    def test_password_reset_confirm(self):
        uidb64, token = self.retrieve_uidb64_and_token()
        expected_redirect_url = (
            f"http://localhost:5173/password/reset/confirm/{uidb64}/{token}/"
        )
        self.password_reset_confirm_url = reverse(
            "password_reset_confirm", kwargs={"uidb64": uidb64, "token": token}
        )
        response = self.client.get(self.password_reset_confirm_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response["location"], expected_redirect_url)


class LogoutViewAPITest(APITestCase):

    def setUp(self):
        self.register_url = reverse("register-user")
        self.login_url = reverse("user-login")
        self.logout_url = reverse("user-logout")
        self.verify_token_url = reverse("token-verification")

        self.user_data = {
            "fullname": "Emmanuel Bronyah",
            "password": "lovesogreat",
            "username": "Emmanuel",
            "user_email": "emmanuelbronyah@yahoo.com",
            "role": "VIEWER",
            "grade": "COMPUTER TECHNICIAN GRADE III",
            "division": "DCE-IT",
        }
        self.login_data = {"username": "Emmanuel", "password": "lovesogreat"}
        Group.objects.create(name="Viewer")

    def retrieve_tokens(self):
        self.client.post(self.register_url, self.user_data, format="json")
        login_response = self.client.post(
            self.login_url, self.login_data, format="json"
        )
        temp_token = login_response.data.get("temp_token", None)
        email_body = mail.outbox[-1].body
        otp_token = re.search(r"\b\d{6}\b", email_body).group()
        tokens = {"tokens": {"temp_token": temp_token, "otp_token": otp_token}}
        response = self.client.post(self.verify_token_url, tokens, format="json")
        return {
            "refresh_token": response.data["refresh_token"],
            "access_token": response.data["access_token"],
        }

    def test_logout(self):
        tokens = self.retrieve_tokens()
        refresh_token, access_token = tokens.get("refresh_token"), tokens.get(
            "access_token"
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.post(
            self.logout_url, {"refresh_token": refresh_token}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn("You have been successfully logged out.", response.data["detail"])

    def test_throttling(self):
        tokens = self.retrieve_tokens()
        refresh_token, access_token = tokens.get("refresh_token"), tokens.get(
            "access_token"
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        refresh_token_dict = {"refresh_token": refresh_token}
        response = self.client.post(self.logout_url, refresh_token_dict, format="json")
        response = self.client.post(self.logout_url, refresh_token_dict, format="json")
        response = self.client.post(self.logout_url, refresh_token_dict, format="json")
        response = self.client.post(self.logout_url, refresh_token_dict, format="json")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
import sys


class Command(BaseCommand):
    help = 'Used to create user'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()

    def handle(self, *args, **options):
        try:
            username_input = input('Username: ')
            username = self._validate_username(username_input)

            email_input = input('Email Address: ')
            email = self._validate_email(email_input)

            password = input('Password: ')
            confirm_password = input('Confirm_password: ')

            if password and confirm_password and password == confirm_password:
                self.UserModel.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write('User Created Successfully')
            else:
                self.stderr.write("Error: password did't match!!")

        except KeyboardInterrupt:
            self.stderr.write("\nOperation cancelled.")
            sys.exit(1)

    def _validate_email(self, email):

        if self.UserModel.objects.filter(email=email).exists():
            self.stderr.write("Error: email is already taken")
            email = input('Email Address: ')
            return self._validate_email(email)

        if not '@' in email:
            self.stderr.write("Error: Enter valid email address")
            email = input('Email Address: ')
            return self._validate_email(email)
        return email

    def _validate_username(self, username):
        if self.UserModel.objects.filter(username=username).exists():
            self.stderr.write("Error: username is already taken")
            username = input('Username: ')
            return self._validate_username(username)
        return username

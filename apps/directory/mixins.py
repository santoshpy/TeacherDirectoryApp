from django.contrib.auth.mixins import LoginRequiredMixin


class LoggedInUserRequired(LoginRequiredMixin):
    login_url = "directory:login"

    def get_login_url(self):
        return self.login_url

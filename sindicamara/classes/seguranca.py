from django.contrib.auth.mixins import LoginRequiredMixin

class SindicamaraLoginRequired(LoginRequiredMixin):
	login_url = "/cadastro/loga/"
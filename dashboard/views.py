from django.shortcuts import render
from django.shortcuts import redirect

class DASHBOARD:

	def redirect(self, request, default="/dashboard"):
		return redirect( default )

	def validate(self, request):
		user = request.session.get( "username" )
		if user:
			return True
		else:
			return False

	def login(self, request):
		if request.method == "GET":
			if self.validate( request ):
				return self.redirect( request, "/dashboard" )
			else:
				return render( request, 'login.html' )
		else:
			return

	def home(self, request):
		if not self.validate( request ):
			return self.redirect( request, "/login" )
		else:
			return render(request, 'dashboard.html')

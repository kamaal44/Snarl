from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

class DASHBOARD:

	def redirect(self, request, default="/dashboard"):
		return redirect( default )

	def validate(self, request):
		user = request.session.get( "username" )
		if user:
			return True
		else:
			return False

	@csrf_exempt
	def login(self, request):
		if request.method == "GET":
			if self.validate( request ):
				return self.redirect( request, "/dashboard" )
			else:
				return render( request, 'login.html' )
		elif request.method == "POST":
			uname = request.POST.get( "username" )
			passw = request.POST.get( "password" )
			if uname and passw:
				veri = authenticate( username=uname, password=passw )
				if veri:
					request.session[ "username" ] = uname
					return HttpResponse( "OK" )
				else:
					return HttpResponse( "Wrong Credentials. " )
			else:
				return HttpResponse( "Username & Password, both fields are not supplied" )

	def home(self, request):
		if not self.validate( request ):
			return self.redirect( request, "/login" )
		else:
			return render(request, 'dashboard.html')

	def statistics(self, request):
		return render(request, 'tabulator.html')

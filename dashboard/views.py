from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import ASSET

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
		if not self.validate( request ):
			return self.redirect( request, '/login' )
		else:
			heading = "Statistics"
			cassets = ASSET.objects.all()
			iassets = ASSET.objects.filter( status="idle" ).all()
			passets = ASSET.objects.filter( status="processing" ).all()
			fassets = ASSET.objects.filter( status="finished" ).all()
			headers = [
				'Serial',
				'Domain',
				'In Process',
				'Subdomains',
				'Ports',
				'Screenshots'
			]

			return render(request, 'tabulator.html', {
					'heading': heading,
					'headers': headers,
					'cassets': cassets,
					'iassets': iassets,
					'passets': passets,
					'fassets': fassets
				})

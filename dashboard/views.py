from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import ASSET
import re
import json

class RECON:

	def __init__(self, obj):
		self.object  = obj
		self.name    = obj.name
		self.domain  = obj.domain
		self.status  = obj.status
		self.serial  = obj.serial
		self.subdoms = obj.subdoms
		self.tkovers = obj.tkovers
		self.ports   = obj.ports
		self.headers = obj.headers

	def enagage(self):
		return

class DASHBOARD:

	PROCESSES = []

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
			cassets = ASSET.objects.all()
			iassets = ASSET.objects.filter( status="idle" ).all()
			passets = ASSET.objects.filter( status="processing" ).all()
			fassets = ASSET.objects.filter( status="finished" ).all()
			return render(request, 'dashboard.html', {
					'cassets': cassets,
					'iassets': iassets,
					'passets': passets,
					'fassets': fassets
				})

	@csrf_exempt
	def status(self, request):
		if not self.validate( request ):
			return HttpResponseForbidden()
		else:
			if request.method == "POST":
				action = request.POST.get( "action" )
				domain = request.POST.get( "domain" )

				if action == "retreive":
					retval = {}
					if domain:
						if domain in self.PROCESSES:
							obj = self.PROCESSES[ domain ]
							retval = {
								obj.domain, obj.status, obj.serial, obj.subdoms, obj.tkovers, obj.ports, obj.headers
							}
							return HttpResponse(json.dumps( retval ))
						else:

							return HttpResponse('{}')
					else:
						for domain in list(self.PROCESSES.keys()):
							obj = self.PROCESSES[ domain ]

				else:
					return HttpResponse('{"error": "Invalid Action"}')
			else:
				return HttpResponseForbidden()


	def execute(self, request):
		if not self.validate( request ):
			return HttpResponseForbidden()
		else:
			if request.method == "GET":
				action = request.GET.get( "action" )
				domain = request.GET.get( "domain" )

				if re.match(r"^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$", domain):
					if action == "add": 
						if not len(ASSET.objects.filter( domain=domain ).all()):
							asset = ASSET(name=domain.split( "." )[0], domain=domain, status="idle")
							asset.save()
							return HttpResponse( '{"success": "true"}' )
						else:
							return HttpResponse( '{"error": "Domain Already in Database. "}' )
					elif action == "recon":
						if not len(ASSET.objects.filter( domain=domain ).all()):
							asset = ASSET(name=domain.split( "." )[0], domain=domain, status="processing")
							asset.save()
							recon = RECON( asset )
							recon.engage()
							self.PROCESSES[ domain ] = recon
							return HttpResponse( '{"success": "true"}' )
						else:
							return HttpResponse( '{"error": "Domain Already in Database. "}' )
					else:
						return HttpResponse( '{"error": "Invalid Action"}' )
				else:
					return HttpResponse( '{"error": "Invalid Domain"}' )

			else:
				return HttpResponseForbidden()

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

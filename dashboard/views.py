from django.shortcuts import render
from django.shortcuts import redirect

class DASHBOARD:

	def redirect(self, request):
		return redirect( "/dashboard" )

	def home(self, request):
		return render(request, 'dashboard.html')

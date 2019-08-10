from django.shortcuts import render
from django.shortcuts import redirect

class DASHBOARD:

	def home(self, request):
		return render(request, 'dashboard.html')

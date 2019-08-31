import hashlib
from django.db import models

# Create your models here.

class ASSET(models.Model):
	name     = models.CharField( max_length=30, verbose_name="Name" )
	domain   = models.CharField( max_length=50, verbose_name="Domain" )
	status   = models.CharField( max_length=50, verbose_name="Status", choices=(
			('processing', 'Processing'),
			('finished'  , 'Finished'),
			('idle'      , 'Idle')
		))
	serial   = models.CharField( max_length=80, verbose_name="Serial" )
	subdoms  = models.TextField( blank=True, verbose_name="Subdomains" )
	vsubdoms = models.TextField( blank=True, verbose_name="Validated Subdomains" )
	tkovers  = models.TextField( blank=True, verbose_name="TakeOvers" )
	ports    = models.TextField( blank=True, verbose_name="Ports" )
	headers  = models.TextField( blank=True, verbose_name="Headers" )

	def __str__(self):
		return self.domain

	class Meta:
		db_table = 'assets'
		verbose_name = 'Asset'
		verbose_name_plural = 'Assets'
from django.db import models

class Search(models.Model):
	query = models.CharField(max_length=20)
	result = models.CharField(max_length=20)
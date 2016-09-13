from django.db import models

class Business(models.Model):
	created_at = models.DateTimeField(
        auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(
        auto_now=True, editable=False)
	
	kolayrandevu_url
	name
	logo
	category
	province
	district
	full_address
	geoposition
	working_hours #json
	description
	professionals #json for name list
	franchise_branches #json for name and url

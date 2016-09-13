from django.db import models

class Category(models.Model):
	name

class Service(models.Model):
	category = models.ForeignKey(Category)
	name

class BusinessServiceRel(models.Model):
	created_at = models.DateTimeField(
        auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(
        auto_now=True, editable=False)

	GENDERS = (
		('m', 'Men'),
		('w', 'Women'),
	)

	business = models.ForeignKey('businesses.Business')
	service = models.ForeignKey(Service)
	gender = models.CharField(max_length=1, options=GENDERS)
	price
from django.db import models

# Create your models here.


# class Payment(models.Model):
#     api_id = models.IntegerField(blank=True, null=True)
#     access_code = models.CharField(max_length=100)
#     status = models.CharField(max_length=100)
#     reference = models.CharField(max_length=100)
#     email = models.CharField(max_length=100)
#     amount = models.FloatField(blank=True, null=True)
#     paid = models.BooleanField(default=False)
#     paid_at = models.DateTimeField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     authorization_url = models.URLField(max_length=200)

#     class Meta:
#         ordering = ['-created_at']

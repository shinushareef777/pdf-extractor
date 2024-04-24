from django.db import models

# Create your models here.
class BelegNumber(models.Model):
  assigned_integer = models.IntegerField()
  beleg_number = models.IntegerField(unique=True, primary_key=True)


class Entry(models.Model):
  pos_number = models.CharField(max_length=50)
  entry_body = models.TextField()
  beleg_number = models.ForeignKey(BelegNumber, on_delete=models.CASCADE)
  product_number = models.TextField()
  

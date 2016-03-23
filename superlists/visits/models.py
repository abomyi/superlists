from django.db import models

# Create your models here.
class VisitModel(models.Model):
    company = models.CharField(max_length=50)
    visitDate = models.DateField()
    visitTime = models.TimeField()
    
    def __str__(self):
        return self.company
    

class Demand(models.Model):
    type = models.CharField(max_length=50)
    
    def __str__(self):
        return self.type
    
    
class Department(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
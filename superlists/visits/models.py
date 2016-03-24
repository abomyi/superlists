from django.db import models

# Create your models here.
class Demand(models.Model):
    type = models.CharField(max_length=50)
    
    def __str__(self):
        return self.type
    
    
class Department(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    

class Teacher(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    
class VisitModel(models.Model):
    company = models.CharField(max_length=50)
    visitDate = models.DateField()
    visitTime = models.TimeField()
    partner = models.CharField(max_length=50)
    visitCount = models.IntegerField(default=1)
    people = models.TextField()
    content = models.TextField()
    outline = models.TextField()
    type = models.ManyToManyField(Demand)
    nextDate = models.DateField(null=True, blank=True)
    entrust_department = models.ForeignKey(Department, null=True, blank=True)
    entrust_teacher = models.ForeignKey(Teacher, null=True, blank=True)
    other = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.company
    


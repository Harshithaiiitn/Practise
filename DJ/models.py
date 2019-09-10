from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Regulations(models.Model):
    regulation = models.CharField(max_length = 200)
    description = models.TextField()
    link=models.CharField(max_length=255)
    content=models.TextField()

    objects = models.Manager() 
    def __str__(self):
        return self.regulation


class BusinessActivity(models.Model):
    businessdefinition_q = models.CharField(max_length=200)
    businessdefinition_a=models.TextField()
    jurisdiction=models.CharField(max_length=200)
    businessdefinition=models.TextField()
    objects = models.Manager()

    def __str__(self):
        return self.businessdefinition_q

class BAReg(models.Model):
    regulation = models.CharField(max_length=50)
    status = models.CharField(max_length=50,default='pending')
    edit_status = models.CharField(max_length=10,default='pending')
    businessdefinition_q = models.CharField(max_length=200)
    businessdefinition_a=models.TextField()
    jurisdiction=models.CharField(max_length=200)
    user= models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.businessdefinition_a

class ProcessReg(models.Model):
    regulation = models.CharField(max_length=50)
    businessdefinition_q = models.CharField(max_length=200)
    businessdefinition_a=models.TextField()
    jurisdiction=models.CharField(max_length=200)
    process = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=50, default='pending')
    edit_status = models.CharField(max_length=10, default='pending')
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()
    def __str__(self):
        return self.businessdefinition_a

class Process(models.Model):
    process = models.CharField(max_length=50)
    description = models.TextField()
    objects = models.Manager()
    
    def __str__(self):
        return self.process

class Controls(models.Model):
    control = models.CharField(max_length=50)
    description = models.TextField()
    content=models.TextField()
    objects = models.Manager()
    def __str__(self):
        return self.control

class ControlReg(models.Model):
    regulation = models.CharField(max_length=50)
    businessdefinition_q = models.CharField(max_length=200)
    businessdefinition_a=models.TextField()
    jurisdiction=models.CharField(max_length=200)
    process = models.CharField(max_length=50)
    description = models.TextField()
    controlarea = models.CharField(max_length=50)
    controlobjective = models.TextField()
    controldescription=models.TextField()
    status = models.CharField(max_length=50,default='pending')
    edit_status = models.CharField(max_length=10,default='pending')
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()
    def __str__(self):
        return self.businessdefinition_a

class Risk(models.Model):
    risk = models.CharField(max_length=50)
    comment = models.TextField()
    objects = models.Manager() 
    def __str__(self):
        return self.risk

class RiskReg(models.Model):
    regulation = models.CharField(max_length=50)
    businessdefinition_q = models.CharField(max_length=200)
    businessdefinition_a=models.TextField()
    jurisdiction=models.CharField(max_length=200)
    process = models.CharField(max_length=50)
    description = models.TextField()
    controlarea = models.CharField(max_length=50)
    controlobjective = models.TextField()
    controldescription=models.TextField()
    status = models.CharField(max_length=50,default='pending')
    edit_status = models.CharField(max_length=10,default='pending')
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    risk = models.CharField(max_length=50)
    comment=models.TextField()
    objects = models.Manager() 
    def __str__(self):
        return self.businessdefinition_a

# class FinalTable(models.Model):
#     regulation=models.CharField(max_length=50)
#     businessdefinition_a=models.TextField()
#     process = models.CharField(max_length=50)
#     controlarea = models.CharField(max_length=50)
#     risk = models.CharField(max_length=50)

#     objects = models.Manager()
#     def __str__(self):
#         return self.businessdefinition_a

class Maptable(models.Model):
    regulation=models.CharField(max_length=50)
    businessdefinition_a=models.TextField()
    process = models.CharField(max_length=50)
    controlarea = models.CharField(max_length=50)
    risk = models.CharField(max_length=50)
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    objects = models.Manager()
    def __str__(self):
        return self.businessdefinition_a

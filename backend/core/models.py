from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)
    flag = models.ImageField(upload_to='country_flags/', null=True, blank=True)
    
    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE , related_name='cities')

    def __str__(self):
        return self.name


class Hall(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.IntegerField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE,related_name='halls')

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()


    def __str__(self):
        return self.name



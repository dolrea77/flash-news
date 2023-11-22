from django.db import models
# Create your models here.
class Crawring(models.Model):
    title = models.CharField(max_length=100, unique=True, primary_key=True)
    content = models.TextField()
    img = models.CharField(max_length=100)
    src = models.CharField(max_length=100)
    summarize = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
class Crawring_ct(models.Model):
    title_ct = models.CharField(max_length=100, unique=True, primary_key=True)
    content_ct = models.TextField()
    img_ct = models.CharField(max_length=100)
    src_ct = models.CharField(max_length=100)
    category = models.CharField(max_length=15)
    summarize_ct = models.TextField()
    created_at_ct = models.DateTimeField(auto_now_add=True)
from django.db import models

class SavedNews(models.Model):
   title = models.CharField("タイトル", max_length=50)
   url = models.CharField(max_length=100)
   # created_at = models.DateTimeField(auto_now_add=True)
   # updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
        return self.title

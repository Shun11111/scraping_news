from django.db import models

class SavedNews(models.Model):
   title = models.CharField("タイトル", max_length=50)
   url = models.CharField(max_length=100)

   def __str__(self):
        return self.title

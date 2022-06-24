from django.db import models
from sso.models import User
from markdown2 import markdown


# Create your models here.
class NonStrippingTextField(models.TextField):
    def formfield(self, **kwargs):
        kwargs['strip'] = False
        return super(NonStrippingTextField, self).formfield(**kwargs)


class Information(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128, default="")
    markdown = NonStrippingTextField()
    time_created = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"<News ID {self.id}: {self.title}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.username,
            "title": self.title,
            "description": self.description,
            "markdown": markdown(self.markdown),
            "time": self.time_created.strftime("%b %d %Y, %I:%M %p"),
        }


class LikePair(models.Model):
    likednews = models.ForeignKey(Information, on_delete=models.CASCADE, related_name="likes")
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likednewspair")
    
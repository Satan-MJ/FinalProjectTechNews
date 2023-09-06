from django.db import models


# Create your models here.
class Articles3(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    url = models.URLField()
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    src = models.CharField(max_length=31)
    text = models.TextField()
    html = models.TextField()
    img_src = models.CharField(max_length=31)
    com_count = models.IntegerField()
    images = models.TextField(default=';')

    def count_comments(self):
        return self.comments.count()

    def to_dict(self):
        return {'title': self.title, 'src': self.src, 'content': self.text.replace('\n', '')[:70] + '...',
                          'link': f'/article{self.id}', 'date': self.date.isoformat(), 'time': self.time.isoformat(),
                          'com_count': self.com_count}

class Comments(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Articles3, on_delete=models.SET_NULL, null=True, related_name='comments')
    username = models.CharField(max_length=255)
    comment = models.TextField()
    date = models.DateField()
    time = models.TimeField()

class InvertedIndex(models.Model):
    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=31)
    article = models.ForeignKey(Articles3, on_delete=models.SET_NULL, null=True, related_name='words')

class InvertedIndex2(models.Model):
    objects = models.Manager()

    key = models.CharField(max_length=31, primary_key=True)
    articles = models.TextField()

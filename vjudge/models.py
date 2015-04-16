from django.db import models

# Create your models here.

class VjudgeID(models.Model):
    vjudge_id = models.IntegerField(primary_key=True)
    judge_source = models.CharField(max_length=11)
    judge_source_id = models.CharField(max_length=11)


    def __unicode__(self):
        return self.judge_source + '-' + self.judge_source_id

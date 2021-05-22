from django.db import models

# Create your models here.


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    label = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_deleted = models.BooleanField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=255)
    quiz = models.ManyToManyField(Quiz)
    question = models.TextField()
    choices = models.TextField()
    points = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_deleted = models.BooleanField()

    def __str__(self):
        return self.name


class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_deleted = models.BooleanField()


class Submission(models.Model):
    quiz = models.IntegerField()
    username = models.CharField(max_length=100)
    points_scored = models.IntegerField()
    submitted_data = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_deleted = models.BooleanField()




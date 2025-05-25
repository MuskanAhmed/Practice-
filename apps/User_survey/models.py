from django.db import models

# Create your models here.

class Question(models.Model):
    QUESTION_TYPES = (
        ('multiple', 'Multiple Choice'),
        ('text', 'Text Response'),
    )
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    order = models.PositiveIntegerField(default=0)  
    
    
    def __str__(self):
        return f"{self.order}. {self.text}"

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
    

class WaitlistEntry(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    company = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class UserResponse(models.Model):
    waitlist_entry = models.ForeignKey(WaitlistEntry, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    selected_options = models.ManyToManyField('Option', blank=True)
    text_answer = models.TextField(blank=True)

    def __str__(self):
        return f"{self.waitlist_entry.email} - Q{self.question.id}"

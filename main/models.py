from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# class User(AbstractUser,TimeStampMixin):
#     username = models.CharField(max_length=10,blank = True, null = True, unique = True)
#     first_name = models.CharField(max_length = 15)
#     last_name = models.CharField(max_length = 15,default="")
#     email = models.EmailField()

#     def __str__(self):
#         return self.username

#     @property
#     def full_name(self):
#         return self.first_name+" "+self.last_name

#     # def save(self,*args,**kwargs):
#     #     pass

class Classroom(TimeStampMixin):
    name = models.CharField(max_length=15)
    members = models.ManyToManyField(User,through="Membership")

    def __str__(self):
        return self.name
    
    @property
    def total_members(self):
        return Membership.objects.filter(classroom=self).count()
    
class Membership(TimeStampMixin):
    person = models.ForeignKey(User,on_delete = models.CASCADE)
    is_Admin = models.BooleanField(default=False)
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)

    class Meta:
        unique_together = ['person','classroom']

    def __str__(self):
        return f"{self.person.username} in {self.classroom.name}"


# -------------------------------------------------------------------------------

class ClassroomPost(TimeStampMixin):
    title = models.CharField(max_length=63)
    subtitle = models.CharField(max_length=63,blank=True, null=True)
    content = models.TextField()
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User',related_name="classroomposts",on_delete=models.CASCADE)
    attachment = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.author.username + " " +self.title[:10]
    
    
    @property
    def total_comments(self):
        return ClassroomPostComment.objects.filter(classroom_post=self).count()

class ClassroomPostComment(TimeStampMixin):
    classroom_post = models.ForeignKey(ClassroomPost,related_name= "comment",on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return str(self.author)+', '+self.classroom_post.title[:10]

    


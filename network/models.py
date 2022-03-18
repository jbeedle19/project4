from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', blank=True, related_name='followers', symmetrical=False)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'following': [user.username for user in self.following.all()],
            'followers': [user.username for user in self.followers.all()]
        }

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=300)
    likes = models.PositiveIntegerField(default=0)
    user_likes = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Post {self.id}: {self.user} said {self.content} on {self.created}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    liked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} liked {self.post}'
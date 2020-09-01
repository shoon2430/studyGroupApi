import os
from django.conf import settings
from django.db import models
from core.models import TimeStampModel


class Group(TimeStampModel):
    photo = models.ImageField(blank=True, upload_to="groups")
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    discription = models.TextField()
    leader = models.ForeignKey(
        "users.User", related_name="leader", on_delete=models.CASCADE
    )
    members = models.ManyToManyField("users.User", related_name="members", blank=True)
    time = models.IntegerField()

    def __str__(self):
        return self.title

    def delete(self, *args, **kargs):
        """
        테이블에서 데이터 삭제 후
        첨부파일이 첨부되어 있었을 경우
        첨부되어있는 파일도 서버 내에서 삭제
        """
        if self.photo:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.photo.path))
        super(Group, self).delete(*args, **kargs)

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        else:
            None
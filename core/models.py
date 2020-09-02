import uuid
from django.db import models

# 각 모델들에 공통적으로 필요한 컬럼
class TimeStampModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    # 데이터 베이스에 등록하지 않음
    class Mata:
        abstract = True
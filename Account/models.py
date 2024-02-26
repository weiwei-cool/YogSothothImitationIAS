import hashlib

from django.db import models


class Account(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # 存储密码哈希

    # 用户权限
    PERMISSION_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    permission_level = models.CharField(max_length=10, choices=PERMISSION_CHOICES, default='user')

    # 用户id
    models.IntegerField(unique=True, default=10000)

    # 用户状态
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('banned', 'Banned'),
        ('pending', 'Pending'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.email

    @classmethod
    def create_account(cls, email, username, password, permission_level='user', uid=10000, status='pending'):
        hashed_password = cls._hash_password(password)
        return cls.objects.create(email=email, username=username, password=hashed_password,
                                  permission_level=permission_level, uid=uid, status=status)

    # 更改用户状态
    def change_account_status(self, status):
        self.status = status
        self.save()

    # 删除账号
    def delete_account(self):
        self.delete()

    # 更改密码
    def change_password(self, new_password):
        self.password = self._hash_password(new_password)
        self.save()

    @staticmethod
    def _hash_password(password):
        # 计算密码的 MD5 哈希值
        return hashlib.md5(password.encode()).hexdigest()

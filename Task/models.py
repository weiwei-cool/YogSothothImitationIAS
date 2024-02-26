from django.db import models
from Account.models import Account


class TaskApplication(models.Model):
    STATUS_CHOICES = [
        ('unprocessed', 'Unprocessed'),
        ('processed', 'Processed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unprocessed')
    reply_status = models.CharField(max_length=20, choices=[('agreed', 'Agreed'), ('rejected', 'Rejected')],
                                    null=True,
                                    blank=True)
    reply_content = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    # 创建账号申请
    @classmethod
    def create_application(cls, title, content, email, username, password):
        # 获取用户数据库内的信息条数
        user_count = Account.objects.count()

        user = Account.create_account(email=email,
                                      username=username,
                                      password=password,
                                      uid=user_count + 99999,
                                      status='pending')
        return cls.objects.create(title=title, content=content, user=user)

    # 同意请求
    def agree_application(self, reply_content=None):
        self.user.change_account_status(status='active')
        self.reply_status = 'agreed'
        self.reply_content = reply_content
        self.save()

    # 拒绝请求
    def reject_application(self, reply_content=None):
        self.reply_status = 'rejected'
        self.reply_content = reply_content
        self.save()


# 申诉封禁
class BanAppeal(models.Model):
    STATUS_CHOICES = [
        ('unprocessed', 'Unprocessed'),
        ('processed', 'Processed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unprocessed')
    reply_content = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

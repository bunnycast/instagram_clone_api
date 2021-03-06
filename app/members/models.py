from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True,
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    relations_users = models.ManyToManyField(
        'self',
        through='Relations',
        # relations_users 에 대한 역방향 참조에 대해서 거부한다.
        related_name='+',
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # The Simplest possible answer : Yes, Always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app 'app_label'?"
        # The Simplest possible answer : Yes, Always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # The Simplest possible answer : All admins aer staff
        return self.is_admin

    # def save(self, *args, **kwargs):
    #     self.set_password(self.password)
    #     return super().save(*args, **kwargs)

    @property
    def follow(self):
        # 내가 팔로우 건 유저
        user = User.objects.filter(
            to_users_relation__from_user=self,
            to_users_ralation__related_type='f',
        )
        return user

    @property
    def follower(self):
        # 나를 팔로우한 유저
        user = User.objects.filter(
            from_users_relation__to_user=self,
            from_users_ralation__related_type='f',
        )
        return user

    @property
    def blocker(self):
        # 나를 차단한 유저
        user = User.objects.filter(
            from_users_relation__to_user=self,
            from_users_relation__related_type='b',
        )
        return user

    @property
    def block(self):
        # 내가 차단한 유저
        user = User.objects.filter(
            to_users_relation__from_user=self,
            to_users_relation__related_type='b',
        )
        return user


class Relations(models.Model):
    CHOICE_RELATIONS_TYPE = (
        ('f', 'follow'),
        ('b', 'block'),
    )
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='from_user_relations',
        related_query_name='from_users_relation',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='to_user_relations',
        related_query_name='to_users_relation',
    )
    related_type = models.CharField(
        max_length=10,
        choices=CHOICE_RELATIONS_TYPE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
            ('to_user', 'from_user'),
        )


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    username = models.CharField(max_length=15)
    introduce = models.CharField(max_length=100)

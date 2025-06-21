from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from django.db.models.signals import post_save
from django.dispatch import receiver

from base.models import (
    models,
    BaseRole,
    BaseActiveModel,
    BaseActiveOrderedModel,
    MAX_LENGTH_NAME
)


class Role(BaseRole):
    pass


class Profile(BaseActiveModel):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile')
    role = models.ForeignKey(Role,
                             on_delete=models.CASCADE,
                             related_name='profiles',
                             null=True, blank=True)

    type = models.CharField(max_length=MAX_LENGTH_NAME, null=True, blank=True)
    mobile = models.CharField(max_length=MAX_LENGTH_NAME, null=True, blank=True)
    status = models.BooleanField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, created, instance, **kwargs):
        """Signal, that creates a new profile for a new user."""
        if created:
            role_instance, created = Role.objects.get_or_create(name__iexact='consultant', type='consultant')
            profile_kws = {
                'user': instance,
                'role': role_instance,
                'active': True,
                'status': True
            }
            try:
                Profile.objects.create(**profile_kws)
            except IntegrityError:
                pass


class Permission(BaseActiveOrderedModel):
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    ref = models.CharField(max_length=MAX_LENGTH_NAME, null=True, blank=True)


class UserPermission(BaseActiveModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='user_permissions')

    class Meta(BaseActiveModel.Meta):
        ordering = (
            'profile', 'permission'
        )
        unique_together = (
            'profile', 'permission'
        )

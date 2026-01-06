from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Post


@receiver(post_migrate)
def create_user_groups_and_permissions(sender, **kwargs):
    """
    Create user groups and assign appropriate permissions after migrations
    """
    if sender.name == 'posts':
        # Create 'Blog Authors' group
        authors_group, created = Group.objects.get_or_create(name='Blog Authors')
        
        # Get permissions for Post model
        post_content_type = ContentType.objects.get_for_model(Post)
        
        # Get specific permissions
        add_post_perm = Permission.objects.get(
            content_type=post_content_type,
            codename='add_post'
        )
        change_post_perm = Permission.objects.get(
            content_type=post_content_type,
            codename='change_post'
        )
        delete_post_perm = Permission.objects.get(
            content_type=post_content_type,
            codename='delete_post'
        )
        
        # Assign permissions to Blog Authors group
        authors_group.permissions.add(add_post_perm, change_post_perm)
        
        # Create 'Blog Moderators' group with all post permissions
        moderators_group, created = Group.objects.get_or_create(name='Blog Moderators')
        moderators_group.permissions.add(add_post_perm, change_post_perm, delete_post_perm)
        
        # Create 'Blog Readers' group with read-only permissions
        readers_group, created = Group.objects.get_or_create(name='Blog Readers')
        # Readers only have view permissions (which are granted by default to all authenticated users)
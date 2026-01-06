from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'category', 'author')
    search_fields = ('title', 'summary', 'body')
    ordering = ('-created_at',)
    filter_horizontal = ('tags',)

    # Define which fields are editable in the admin
    fields = ('title', 'summary', 'body', 'author', 'category', 'tags')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Superusers can see all posts
        if request.user.is_superuser:
            return qs
        # Blog Moderators can see all posts
        elif request.user.groups.filter(name='Blog Moderators').exists():
            return qs
        # Blog Authors can only see their own posts
        elif request.user.groups.filter(name='Blog Authors').exists():
            return qs.filter(author=request.user)
        # For other users, only show their own posts
        else:
            return qs.filter(author=request.user)

    def has_change_permission(self, request, obj=None):
        # Superusers can change any post
        if request.user.is_superuser:
            return True
        # If object exists, check if user is the author or a moderator
        if obj:
            # Blog Moderators can change any post
            if request.user.groups.filter(name='Blog Moderators').exists():
                return True
            # Blog Authors can only change their own posts
            elif request.user.groups.filter(name='Blog Authors').exists():
                return obj.author == request.user
            # Other users can only change their own posts
            else:
                return obj.author == request.user
        # For adding new posts, check if user is in Blog Authors group or authenticated
        return request.user.is_authenticated and (
            request.user.groups.filter(name='Blog Authors').exists() or
            request.user.is_superuser
        )

    def has_delete_permission(self, request, obj=None):
        # Superusers can delete any post
        if request.user.is_superuser:
            return True
        # Blog Moderators can delete any post
        if request.user.groups.filter(name='Blog Moderators').exists():
            return True
        # If object exists, Blog Authors can only delete their own posts
        if obj:
            return obj.author == request.user
        # For bulk delete, only allow if user is moderator or superuser
        return False

    def has_add_permission(self, request):
        # Only authenticated users in Blog Authors group, moderators, or superusers can add posts
        return (request.user.is_authenticated and
                (request.user.is_superuser or
                 request.user.groups.filter(name='Blog Authors').exists() or
                 request.user.groups.filter(name='Blog Moderators').exists()))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Only allow users to select themselves as author if they're not a superuser or moderator
        if db_field.name == "author":
            if not request.user.is_superuser and not request.user.groups.filter(name='Blog Moderators').exists():
                kwargs["queryset"] = request.user.__class__.objects.filter(pk=request.user.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

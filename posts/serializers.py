from rest_framework import serializers
from .models import Post
from categories.serializers import CategorySerializer
from tags.serializers import TagSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at')

    def create(self, validated_data):
        # Extract additional fields
        category_id = validated_data.pop('category_id', None)
        tag_ids = validated_data.pop('tag_ids', [])
        
        # Get the current user from the context
        user = self.context['request'].user
        validated_data['author'] = user
        
        # Create the post
        post = Post.objects.create(**validated_data)
        
        # Set category if provided
        if category_id:
            from categories.models import Category
            try:
                category = Category.objects.get(id=category_id)
                post.category = category
                post.save()
            except Category.DoesNotExist:
                pass  # Category doesn't exist, skip setting it
        
        # Set tags if provided
        from tags.models import Tag
        for tag_id in tag_ids:
            try:
                tag = Tag.objects.get(id=tag_id)
                post.tags.add(tag)
            except Tag.DoesNotExist:
                pass  # Tag doesn't exist, skip adding it
        
        return post

    def update(self, instance, validated_data):
        # Extract additional fields
        category_id = validated_data.pop('category_id', None)
        tag_ids = validated_data.pop('tag_ids', None)
        
        # Update the post fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update category if provided
        if category_id is not None:
            from categories.models import Category
            try:
                category = Category.objects.get(id=category_id)
                instance.category = category
            except Category.DoesNotExist:
                instance.category = None
        
        instance.save()
        
        # Update tags if provided
        if tag_ids is not None:
            from tags.models import Tag
            instance.tags.clear()
            for tag_id in tag_ids:
                try:
                    tag = Tag.objects.get(id=tag_id)
                    instance.tags.add(tag)
                except Tag.DoesNotExist:
                    pass  # Tag doesn't exist, skip adding it
        
        return instance


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'summary', 'author', 'category', 'tags', 'created_at', 'updated_at']
from rest_framework import serializers

from core.models import Category, User, Word


    

class UserSerializer(serializers.ModelSerializer):
    """
    User serializer for create and list existing users
    """
    class Meta:
        model = User
        fields = ('telegram_user_id', 'username')

    def validate(self, attrs):
        """
        Validate makes sure that user is not exists.
        """
        user = User.objects.filter(telegram_user_id=attrs['telegram_user_id'])
        if user.exists():
            raise serializers.ValidationError("User is exists!")
        else:
            return attrs

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer for create and list the them
    """
    # user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'title')
        read_only_fields = ('id', )

    def validate(self, attrs):
        """
        Validate makes sure that given
        category with telegram user id not exists
        avoid repeted categories
        """
        telegram_user_id = self.context['view'].kwargs['telegram_user_id']
        category = Category.objects.filter(title= attrs['title'], user__telegram_user_id= telegram_user_id)
        if category.exists():
            raise serializers.ValidationError("user id or Category is invalid ")
        return attrs


class WordSerializer(serializers.ModelSerializer):
    """
    Serializer for creating category
    """
    class Meta:
        model = Word
        fields = ('id', 'english', 'persian')
        read_only_fields = ('id',)

    def validate(self, attrs):
        """
        Validate makes sure that user and
        user's category is exists or not!
        """
        data = self.context['request'].data
        user = User.objects.filter(telegram_user_id=data['telegram_user_id'])
        if user.exists():
            category = Category.objects.filter(title=data['category'], user=user.first())
            if category.exists():
                attrs.update({"category" : category.first(), "user": user.first()})
                return attrs
            else:
                raise serializers.ValidationError("Category not found",code=404)
        else:
            raise serializers.ValidationError("user not found",code=404)

    def create(self, validated_data):
        return Word.objects.create(**validated_data)


class WordDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for list and delete word
    """
    # user = UserSerializer(many=False, read_only=True)
    # category = CategorySerializer(many=False, read_only=True)
    
    class Meta:
        model = Word
        fields = ('id', 'english', 'persian')
        read_only_fields = ('id',)

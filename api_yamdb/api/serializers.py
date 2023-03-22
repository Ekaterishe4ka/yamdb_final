from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User


class SignupSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователя."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        required=True,
        max_length=50
    )
    email = serializers.EmailField(required=True, max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        """Проверка: username не равен me."""
        if value.lower() == "me":
            raise serializers.ValidationError(
                'Username "me" не разрешено.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор получения токена авторизации."""
    username = serializers.CharField(
        required=True
    )
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя"""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        required=True,
        max_length=50
    )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует!')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует!')
        return value

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50, min_length=None, allow_blank=False)

    def validate_slug(self, value):
        if Category.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'Такой slug уже используется!')
        return value

    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

        def validate_year(self, value):
            year_now = timezone.now.year
            if value <= 0 or value > year_now:
                raise serializers.ValidationError(
                    'Год создания должен быть нашей эры и не больше текущего.'
                )
            return value


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 1 > value or value > 10:
            raise serializers.ValidationError(
                'Оценка должна быть не менее 1 и не более 10'
            )
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST' and Review.objects.filter(
            title=title, author=author
        ).exists():
            raise serializers.ValidationError(
                'Автор может поставить только одну оценку')
        return data

    class Meta:
        model = Review
        fields = '__all__'

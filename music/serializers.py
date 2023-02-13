from rest_framework import serializers

from .models import MusicInfo, Comment, Rating, Basket, Vip, User
from django.db.models import Avg


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = MusicInfo
        fields = '__all__'

    def validate_title(self, title):
        if self.Meta.model.objects.filter(title=title).exists():
            raise serializers.ValidationError('Такой заголовок уже существует')
        return title

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        tags = validated_data.pop('tags', [])
        post = MusicInfo.objects.create(author=user, **validated_data)
        post.tags.add(*tags)
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.save()
        return super().update(instance, validated_data)

    def delete(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.save()
        return validated_data.pop(instance.title)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(
            Comment.objects.filter(post=instance.pk),
            many=True
        ).data
        representation['ratings'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        # obj = Like.objects.filter(is_liked=True)
        representation['likes_count'] = instance.likes.count()
        return representation


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicInfo
        fields = ['title', 'slug', 'image', 'music', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        comment = Comment.objects.create(author=user, **validated_data)
        return comment

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment')
        instance.save()
        return super().update(instance, validated_data)

    def delete(self, instance, validated_data):
        instance.comment = validated_data.get('comment')
        instance.save()
        return validated_data.pop(instance.comment)

    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Rating
        fields = ['id', 'rating', 'author', 'post']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        rating = Rating.objects.create(author=user, **validated_data)
        return rating

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError(
                'Рейтинг должен быть от 1 до 5'
            )
        return rating

    def delete(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return validated_data.pop(instance.rating)


# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Image
#         fields = ['image']

class BasketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basket
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        basket = Basket.objects.create(**validated_data)
        return basket

    def validate_product(self, product):
        if self.Meta.model.objects.filter(product=product).exists():
            raise serializers.ValidationError('Такой продукт уже сушествует в корзине')
        return product

    def update(self, instance, validated_data):
        instance.basket = validated_data.get('basket')
        instance.save()
        return super().update(instance, validated_data)

    def delete(self, instance, validated_data):
        instance.basket = validated_data.get('basket')
        instance.save()
        return validated_data.pop(instance.basket)


class VipSerializer(serializers.ModelSerializer):
    # email = serializers.CharField()
    author = serializers.ReadOnlyField(source='author.name')

    # def validate(self, data):
    #     email = data.get('email')
    #     if not User.objects.filter(email=email).exists():
    #         raise serializers.ValidationError('Пользователь не найден')
    #     return data
    #
    # def activate(self):
    #     email = self.validated_data.get('email')
    #     user = User.objects.get(email=email)
    #     user.is_active = True
    #     user.save()
    '''============================='''

    class Meta:
        model = Vip
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        vip = Vip.objects.create(author=user, **validated_data)
        return vip

    def validate_product(self, money):
        if self.Meta.model.objects.filter(money=money).exists():
            raise serializers.ValidationError('У вас уже есть VIP')
        return money

    def delete(self, instance, validated_data):
        instance.money = validated_data.get('money')
        instance.save()
        return validated_data.pop(instance.money)


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        his = Basket.objects.create(**validated_data)
        return his

    def validate_product(self, history):
        if self.Meta.model.objects.filter(history=history).exists():
            raise serializers.ValidationError('Уже сушествует в истории')
        return history

    def delete(self, instance, validated_data):
        instance.history = validated_data.get('history')
        instance.save()
        return validated_data.pop(instance.history)
    #
    # def update(self, instance, validated_data):
    #     instance.history = validated_data.get('history')
    #     instance.save()
    #     return super().update(instance, validated_data)
    #
    # def delete(self, instance, validated_data):
    #     instance.history = validated_data.get('history')
    #     instance.save()
    #     return validated_data.pop(instance.history)

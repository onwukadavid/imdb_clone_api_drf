from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ['watchlist']
        # fields ='__all__'
        
class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name')

    class Meta:
        model = WatchList
        fields = '__all__'
        
class StreamPlatformSerializers(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    
    class Meta:
        model = StreamPlatform
        fields = '__all__'


# def length_greater_than_2(value):
#     if len(value) < 2:
#         raise serializers.ValidationError('Name is too short')
#     return value

# class MovieSerializer(serializers.Serializer):
#     id          = serializers.IntegerField(read_only=True)
#     name        = serializers.CharField(validators=[length_greater_than_2])
#     description = serializers.CharField()
#     is_active   = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.is_active = validated_data.get('is_active', instance.is_active)
#         instance.save()
#         return instance
    
#     def validate_name(self, value):
        
#         if len(value) < 2:
#             raise serializers.ValidationError('Name is too short')
#         return value
    
#     def validate(self, data):
        
#         if data['name'] == data['description']:
#             raise serializers.ValidationError('Title and description should be different')
#         return data
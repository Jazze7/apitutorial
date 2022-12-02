from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from places.models import Place,Gallery,Comment

class PlaceSerializer(ModelSerializer):
    likes=serializers.SerializerMethodField()
    is_liked=serializers.SerializerMethodField()

    class Meta:
        fields=("id","place","name","featured_image","likes","is_liked")
        model=Place

    def get_likes(self, instance):
        return instance.likes.count()


    def get_is_liked(self, instances):
        request=self.context.get("request")

        if instances.likes.filter(username=request.user.username).exists():
            return True
        else:
            return False


class GallerySerializer(ModelSerializer):
    class Meta:
        fields=("id","image")
        model = Gallery



class PlaceDetailSerializer(ModelSerializer):

    category=serializers.SerializerMethodField()
    gallery=serializers.SerializerMethodField()

    class Meta:
        fields=("id","place","name","featured_image","category","description","gallery")
        model=Place

    def get_category(self, instance):
        return instance.category.name

    def get_gallery(self, instance):
         request=self.context.get("request")
         images=Gallery.objects.filter(place=instance)
         
         context={
            "request":request
         }

         serializers=GallerySerializer(images,many=True,context=context)
         return serializers.data


class CommentSerializer(ModelSerializer):
        user=serializers.SerializerMethodField()
        date=serializers.SerializerMethodField()
        reply=serializers.SerializerMethodField()


        class Meta:
            fields=("id","user","comment","date","reply")
            model = Comment

        def get_user(self, instance):
            return instance.user.username


        def get_date(self, instance):
            return instance.date.strftime("%d %B %Y")


        def get_reply(self, instance):
            instances=Comment.objects.filter(main_comment=instance)
            serializer=CommentSerializer(instances,many=True)
            return serializer.data
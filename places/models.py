from django.db import models

# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=100)
    featured_image = models.ImageField(upload_to="places/images/")
    place= models.CharField(max_length=100)
    category = models.ForeignKey("places.Category",on_delete=models.CASCADE)
    description = models.TextField()
    is_deleted= models.BooleanField(default=False)

    likes= models.ManyToManyField("auth.User")

    class Meta:
        db_table = 'places_place'
    
    def __str__(self):
        return self.name


class Category(models.Model):
    image= models.ImageField( upload_to="categories/images/")
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'places_category'
        verbose_name_plural="categories"
    
    def __str__(self):
        return self.name


class Gallery(models.Model):
    image= models.ImageField( upload_to="places/images/")
    place=models.ForeignKey("places.Place",on_delete=models.CASCADE)

    class Meta:
        db_table = 'places_gallery'
        verbose_name_plural="gallery"

    
    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    main_comment = models.ForeignKey("places.Comment",related_name="parent_comment",on_delete=models.CASCADE,blank=True,null=True)
    place=models.ForeignKey("places.Place",on_delete=models.CASCADE)
    user= models.ForeignKey("auth.User", on_delete=models.CASCADE)
    date= models.DateTimeField()
    comment= models.TextField()
    
    def __str__(self):
        return str(self.id)
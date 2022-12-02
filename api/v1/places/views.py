import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.v1.places.serializers import PlaceSerializer,PlaceDetailSerializer,CommentSerializer
from places.models import Place,Comment
from django.db.models import Q

from api.v1.places.pagination import StandardResultsSetPagination
@api_view(["GET"])
def places(request):
    instances=Place.objects.filter(is_deleted=False)

    q=request.GET.get('q')
    if q:
        instances=instances.filter(Q(name__icontains=q,is_deleted=False) | Q(place__icontains=q,is_deleted=False))
    

    paginator=StandardResultsSetPagination()
    paginated_result=paginator.paginate_queryset(instances,request)
    context={
        "request": request
    }
    serializer=PlaceSerializer(paginated_result,many=True,context=context)
    response_data={
        "status_code": "6000",
        "count":paginator.page.paginator.count,
        "links":{
            "next":paginator.get_next_link(),
            "previous":paginator.get_previous_link()
        },
        "data": serializer.data
    }
    return Response(response_data)


@api_view(["GET"])
def place(request,pk):
    if Place.objects.filter(pk=pk).exists():
        instances=Place.objects.get(pk=pk)
        context={
            "request": request
        }
        serializer=PlaceDetailSerializer(instances,context=context)
        response_data={
            "status_code": "6000",
            "data": serializer.data
        }
        return Response(response_data)
    else:
        response_data={
            "status_code": "6001",
            "message": "Place not found"
        }
        return Response(response_data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected(request,pk):
    if Place.objects.filter(pk=pk).exists():
        instances=Place.objects.get(pk=pk)
        context={
            "request": request
        }
        serializer=PlaceDetailSerializer(instances,context=context)
        response_data={
            "status_code": "6000",
            "data": serializer.data
        }
        return Response(response_data)
    else:
        response_data={
            "status_code": "6001",
            "message": "Place not found"
        }
        return Response(response_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_comments(request,pk):
    if Place.objects.filter(pk=pk).exists():
        instances=Place.objects.get(pk=pk)
        comment=request.data["comment"]
        try:
           main_comment=request.data["main_comment"]
        except:
            main_comment=None

        instance=Comment.objects.create(
            user=request.user,
            comment=comment,
            place=instances,
            date=datetime.datetime.now()
            )
        if main_comment:
            if Comment.objects.filter(pk=main_comment).exists():
                main=Comment.objects.get(pk=main_comment)
                instance.main_comment=main
                instance.save()


        response_data={
            "status_code": "6000",
            "message": "Comment added successfully"
        }
    else:
        response_data={
            "status_code": "6001",
            "message": "Place not found"
        }
    return Response(response_data)

@api_view(["GET"])
@permission_classes([AllowAny])
def view_comments(request,pk):
    if Place.objects.filter(pk=pk).exists():
        place=Place.objects.get(pk=pk)
        instances=Comment.objects.filter(place=place,main_comment=None)

        context={
            "request": request
        }

        serializer=CommentSerializer(instances,many=True,context=context)

        response_data={
            "status_code": "6000",
            "data": serializer.data
        }
        return Response(response_data)
    else:
        response_data={
            "status_code": "6001",
            "message": "Place not found"
        }
        return Response(response_data)    



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def like(request,pk):
    if Place.objects.filter(pk=pk).exists():
        instances=Place.objects.get(pk=pk)

        if instances.likes.filter(username=request.user.username).exists():
            instances.likes.remove(request.user)
            message="Like removed"
            
        else:
            instances.likes.add(request.user)
            message="Like added"
        response_data={
            "status_code": "6000",
            "message": message,
        } 

    else:
        response_data={
            "status_code": "6001",
            "message": "Place not found"
        }
    return Response(response_data)
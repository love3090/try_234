from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import status, generics, permissions 
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer 


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#@csrf_exempt 
#def snippet_list(request):
#    """
#    List all code snippets, or create a new snippet.
#    """
#    if request.method == "GET":
#        snippets = Snippet.objects.all()
#        serializer = SnippetSerializer(snippets, many=True)
#        return JsonResponse(serializer.data, safe=False)
#
#    elif request.method == "POST":
#        data = JSONParser().parser(request)
#        serializer = SnippetSerializer(data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data, status=201)
#        return JsonResponse(serializer.errors, status=400)


#@csrf_exempt 
#def snippet_detail(request, pk):
#    """
#    Retrieve, update or delete a code snippet.
#    """
#    try:
#        snippet = Snippet.objects.get(pk=pk)
#    except Snippet.DoesNotExist:
#        return HttpResponse(status=404)
#
#    if request.method == "GET":
#        serializer = SnippetSerializer(snippet)
#        return JsonResponse(serializer.data)
#    elif request.method == "PUT":
#        data = JSONParser().parse(request)
#        serializer = SnippetSerializer(snippet, data=data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data)
#        return JsonResponse(serializer.errors, status=404)
#    elif request.method == "DELETE":
#        snippet.delete()
#        return HttpResponse(status=204)


#@csrf_exempt
#@api_view(['GET', 'POST'])
#def snippet_list(request, format=None):
#    """
#    List all code snippets, or create a new snippet.
#    """
#    if request.method == "GET":
#        snippets = Snippet.objects.all()
#        serializer = SnippetSerializer(snippets, many=True)
#        return Response(serializer.data)
#
#    elif request.method == "POST":
#        serializer = SnippetSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#@csrf_exempt
#@api_view(['GET', 'PUT', 'DELETE'])
#def snippet_detail(request, pk, format=None):
#    """
#    Retrieve, update or delete a code snippet.
#    """
#    try:
#        snippet = Snippet.objects.get(pk=pk)
 #   except Snippet.DoesNotExist:
 #       return Response(status=status.HTTP_404_NOT_FOUND)

#    if request.method == "GET":
#        serializer = SnippetSerializer(snippet)
#        return Response(serializer.data)
#    elif request.method == "PUT":
#        serializer = SnippetSerializer(snippet, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#    elif reqeust.method == "DELETE":
#        snippet.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)


class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(APIView):
    """
    Retrive, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404 

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk=pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk=pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

permissions_classes = (permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly, )

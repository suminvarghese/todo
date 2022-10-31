
from multiprocessing import context
from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from api import serializers
from api.models import Todos
from api.serializers import Registrationserializer, Todoserializer 
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions

class TodosView(ViewSet):
    def list(self,request,*args,**kw):
        qs=Todos.objects.all()
        serializer=Todoserializer(qs,many=True)
        return Response(data=serializer.data)
    
    def create(self,request,*args,**kw):
        serialzers=Todoserializer(data=request.data)
        if serialzers.is_valid():
            serialzers.save()
            return Response(data=serialzers.data)
        else:
            return Response(data=serialzers.errors)

    def retrieve(self,request,*args,**kw):
        id=kw.get("pk")
        qs=Todos.objects.get(id=id)
        serializer=Todoserializer(qs,many=False)
        return Response(data=serializer.data)

    def destroy(self,request,*args,**kw):
        id=kw.get("pk")
        Todos.objects.get(id=id).delete()
        return Response(data="deleted")

    def update(self,request,*args,**kw):
        id=kw.get("pk")
        object=Todos.objects.get(id=id)
        serializer=Todoserializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    

    
class TodosModelViews(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=Todoserializer
    queryset=Todos.objects.all()
    
    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user) 

    def create(self, request, *args, **kwargs):
        serializers=Todoserializer(data=request.data,context={"user":request.user})
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data)
        else:
            return Response(data=serializers.errors)

    # def perform_create(self,serializer):
    #     return serializer.save (user=self.request.user)
    # def list(self, request, *args, **kw):
    #     qs=Todos.objects.filter(user=request.user)
    #     serializer=Todoserializer(qs,many=True)
    #     return Response(data=serializer.data)

    # def create(self,request,*args,**kw):
    #     serializer=Todoserializer(data=request.data)
    #     if serializer.is_valid():
    #         Todos.objects.create(**serializer.validated_data,user=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)


    @action(methods=["GET"],detail=False)

    def pending_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=False)
        serializers=Todoserializer(qs,many=True)
        return Response(data=serializers.data)

    @action(methods=["GET"],detail=False)
    def completed_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=True)
        serializers=Todoserializer(qs,many=True)
        return Response(data=serializers.data)

    @action(methods=["POST"],detail=True)
    def mark_as_done(self,request,*args,**kw):
        id=kw.get("pk")
        object=Todos.objects.get(id=id)
        object.status=True
        object.save()
        serializers=Todoserializer(object,many=False)
        return Response(data=serializers.data)

class UserView(ModelViewSet):
    serializer_class=Registrationserializer
    queryset=User.objects.all()

    # def create(self,request,*args,**kw):
    #     serializers=Registrationserializer(data=request.data)
    #     if serializers.is_valid():
    #         User.objects.create_user(**serializers.validated_data)
    #         return Response(data=serializers.data)
    #     else:
    #         return Response(data=serializers.errors)


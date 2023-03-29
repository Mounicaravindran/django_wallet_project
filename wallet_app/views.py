from http.client import ResponseNotReady, responses
from urllib import response
from rest_framework import generics
from .models import Wallet
from .serializers import WalletSerializer

class WalletCreateView(generics.CreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

class WalletActivateView(generics.UpdateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = True
        instance.save()
        serializer = self.get_serializer(instance)
        return response(serializer.data)

class WalletDisableView(generics.UpdateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        serializer = self.get_serializer(instance)
        return response(serializer.data)

class WalletAddMoneyView(generics.UpdateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        amount = request.data.get('amount')
        instance.balance += amount
        instance.save()
        serializer = self.get_serializer(instance)
        return response(serializer.data)

class WalletWithdrawMoneyView(generics.UpdateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        amount = request.data.get('amount')
        if instance.balance >= amount:
            instance.balance -= amount
            instance.save()
            serializer = self.get_serializer(instance)
            return responses(serializer.data)
        else:
            return response({'detail': 'Insufficient funds'}, status=400)

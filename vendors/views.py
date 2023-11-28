from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from django.views import View
from django.http import JsonResponse
from django.db.models import Count, Avg, Sum
from django.utils import timezone
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class VenorAPIView(APIView):

    def get(self,request):
        try:
            vendor_id = self.request.query_params.get('vendor_id')
            vendor=Vendor.objects.filter(id=vendor_id).last()
            serializer=VendorSerializer(vendor, many=False)
            return Response(serializer.data)
        except:
            vendors=Vendor.objects.all()
            serializer=VendorSerializer(vendors,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Vendor Created Successfully','success':True}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request):
        vendor_id = self.request.query_params.get('vendor_id')
        vendor=Vendor.objects.filter(id=vendor_id).last()
        serializer=VendorSerializer(instance=vendor,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Vendor Updated Successfully','success':True}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        vendor_id = self.request.query_params.get('vendor_id')
        vendor=get_object_or_404(Vendor,pk=vendor_id)
        vendor.delete()
        return Response({'msg':'Vendor Deleted Successfully','success':True}, status=status.HTTP_201_CREATED)
    
class PurchaseOrderAPIView(APIView):

    def get(self,request):
        try:
            po_id = self.request.query_params.get('po_id')
            purchase_orders=PurchaseOrder.objects.filter(id = po_id).last()
            serializer=PurchaseOrderSerializer(purchase_orders,many=False)
            return Response(serializer.data)
        except:
            purchase_orders=PurchaseOrder.objects.all()
            serializer=PurchaseOrderSerializer(purchase_orders,many=True)
            return Response(serializer.data)
        
    def post(self,request):
        serializer=PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Purchase Order Created Successfully','success':True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=400)
    
    def put(self,request):
        po_id = self.request.query_params.get('po_id')
        purchase_order=PurchaseOrder.objects.filter(id=po_id).last()
        serializer=PurchaseOrderSerializer(instance=purchase_order,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Purchase Order Updated Successfully','success':True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=400)
    
    def delete(self,request):
        po_id = self.request.query_params.get('po_id')
        purchase_orders=get_object_or_404(PurchaseOrder, id=po_id)
        purchase_orders.delete()
        return Response({'message':"Purchase Order deleted successfully"},status=204)
    
class vendorPerformanceAPIView(APIView):

    def get(self,request):
        v_id = self.request.query_params.get('vendor_id')
        vendor=Vendor.objects.filter(id=v_id).last()
        metrics={
            'on_time_delivery_rate':vendor.on_time_delivery_rate,
            'quality_rating_avg':vendor.quality_rating_average,
            'average_response_time':vendor.average_response_time,
            'fulfillment_rate':vendor.fulfillment_rate,
        }
        return Response(metrics)
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
    

class FilterPurchaseOrderAPIView(APIView):

    def get(self,request):
        v_id = self.request.query_params.get('vendor_id')
        purchase_orders=PurchaseOrder.objects.filter(vendor=v_id)
        serializer=PurchaseOrderSerializer(purchase_orders,many=True)
        return Response(serializer.data)
        
#-----------On-Time Delivery Rate: Percentage of orders delivered by the promised date.-------------------
def calculate_on_time_delivery_rate(vendor):
    total_orders = vendor.purchase_orders.count()
    on_time_deliveries = HistoricalPerformance.objects.filter(
        vendor=vendor, on_time_delivery_date=True
    ).count()

    if total_orders==0:
        return 0.0
    
    return f'{(on_time_deliveries /  total_orders)*100}%'

# ------Quality Rating: Average of quality ratings given to a vendor’s purchase orders--------------------------
def calculate_quality_rating_average(vendor):
    purchase_orders = vendor.purchase_orders.filter(
        quality_rating__isnull=False
    )
    if not purchase_orders.exists():
        return 0.0
    
    total_ratings = sum(po.quality_rating_average for po in purchase_orders)
    return f'{total_ratings / purchase_orders.count()}%'

#-------------Response Time: Average time taken by a vendor to acknowledge or respond to purchase orders-----------------
def calculate_average_response_time(vendor):
    purchase_orders = vendor.purchase_orders.filter(
        acknowledgment_date__isnull=False
    )
    if not purchase_orders.exists():
        return 0.0

    total_response_time = sum(
        (po.acknowledgment_date - po.issue_date).seconds
        for po in purchase_orders
    )
    return f'{total_response_time / purchase_orders.count()}'

#---------------Fulfilment Rate: Percentage of purchase orders fulfilled without issues.-----------------------
def calculate_fulfillment_rate(vendor):
    purchase_orders = vendor.purchase_orders.all()
    if not purchase_orders.exists():
        return 0.0

    fulfilled_orders = purchase_orders.filter(status='Fulfilled').count()
    return f'{(fulfilled_orders / purchase_orders.count()) * 100.0}%'


#----------- Vendor Performance Evaluation-----------------
class vendorPerformanceAPIView(APIView):
    def get(self,request):
        v_id = self.request.query_params.get('vendor_id')
        vendor=Vendor.objects.filter(id=v_id).last()

        on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
        quality_rating_average = calculate_quality_rating_average(vendor)
        average_response_time = calculate_average_response_time(vendor)
        fulfillment_rate = calculate_fulfillment_rate(vendor)

        metrics = {
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_average': quality_rating_average,
            'average_response_time': average_response_time,
            'fulfillment_rate': fulfillment_rate,
        }
        return Response(metrics)
    
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from django.views import View
from django.http import JsonResponse
from django.db.models import Count, Avg, Sum
from django.utils import timezone
import json
# Create your views here.

class VenorListView(View):
    def get(self,request):
        vendors=Vendor.objects.all()
        serializer=VendorSerializer(vendors,many=True)
        return JsonResponse(serializer.data,safe=False)
    
    def post(self,request):
        data=json.loads(request.body)
        serializer=VendorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)
    
class VendorDetailView(View):
    def get(self,request,vendor_id):
        vendor=get_object_or_404(Vendor,pk=vendor_id)
        serializer=VendorSerializer(vendor)
        return JsonResponse(serializer.data)
    
    def put(self,request,vendor_id):
        vendor=get_object_or_404(vendor,pk=vendor_id)
        data=json.loads(request.body)
        serializer=VendorSerializer(instance=vendor,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors,status=400)
    
    def delete(self,request,vendor_id):
        vendor=get_object_or_404(Vendor,pk=vendor_id)
        vendor.delete()
        return JsonResponse({'message':"Vendor deleted successfully"},status=204)
    

class PurchaseOrderListView(View):
    def get(self,request):
        purchase_orders=PurchaseOrder.objects.all()
        serializer=PurchaseOrderSerializer(purchase_orders,many=True)
        return JsonResponse(serializer.data,safe=False)
    
    def post(self,request):
        data=json.loads(request.body)
        serializer=PurchaseOrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)
    
class PurchaseOrderDetailView(View):
    def get(self,request,po_id):
        purchase_order=get_object_or_404(PurchaseOrder,pk=po_id)
        serializer=PurchaseOrderSerializer(purchase_order)
        return JsonResponse(serializer.data)
    
    def put(self,request,po_id):
        purchase_order=get_object_or_404(PurchaseOrder,pk=po_id)
        data=json.loads(request.body)
        serializer=PurchaseOrderSerializer(instance=purchase_order,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors,status=400)
    
    def delete(self,request,po_id):
        purchase_orders=get_object_or_404(PurchaseOrder,pk=po_id)
        purchase_orders.delete()
        return JsonResponse({'message':"Purchase Order deleted successfully"},status=204)
    
class vendorPerformanceView(View):
    def get(self,request,vendor_id):
        vendor=get_object_or_404(Vendor,pk=vendor_id)
        metrics={
            'on_time_delivery_rate':vendor.on_time_delivery_rate,
            'quality_rating_avg':vendor.quality_rating_average,
            'average_response_time':vendor.average_response_time,
            'fulfillment_rate':vendor.fulfillment_rate,
        }

        return JsonResponse(metrics)
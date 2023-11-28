from django.db import models
from django.db.models import Count, Avg, Sum
from django.utils import timezone

types_of_status = (('Fulfilled','Fulfilled'),)
class Vendor(models.Model):
    name=models.CharField(max_length=255)
    contact_details=models.TextField()
    address=models.TextField()
    vendor_code=models.CharField(max_length=20,unique=True)
    on_time_delivery_rate=models.FloatField(default=0.0)
    quality_rating_average=models.FloatField(default=0.0)
    average_response_time=models.FloatField(default=0.0)
    fulfillment_rate=models.FloatField(default=0.0)
    status = models.CharField(max_length=50, choices=types_of_status)

    def __str__(self):
        return self.name
    
class PurchaseOrder(models.Model):
    po_number=models.CharField(max_length=20)
    vendor=models.ForeignKey(Vendor,on_delete=models.PROTECT, related_name='purchase_orders')
    oredr_date=models.DateTimeField()
    delivery_date=models.DateTimeField()
    items=models.JSONField()
    quantity=models.PositiveIntegerField()
    status=models.CharField(max_length=20)
    quality_rating=models.FloatField(default=0)
    issue_date=models.DateTimeField()
    acknowledgment_date=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.po_number
 
class HistoricalPerformance(models.Model):
    vendor=models.ForeignKey(Vendor,on_delete=models.PROTECT, related_name='vendor')
    date=models.DateTimeField()
    on_time_delivery_date=models.FloatField(default=0)
    quality_rating_avg=models.FloatField(default=0)
    average_response_time=models.FloatField(default=0)
    fulfillment_rate=models.FloatField(default=0)

    def __str__(self):
        return self.vendor
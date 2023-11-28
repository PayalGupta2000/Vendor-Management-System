from django.db import models
from django.db.models import Count, Avg, Sum
from django.utils import timezone

# Create your models here.
class Vendor(models.Model):
    name=models.CharField(max_length=255)
    contact_details=models.TextField()
    address=models.TextField()
    vendor_code=models.CharField(max_length=20,unique=True)
    on_time_delivery_rate=models.FloatField(default=0.0)
    quality_rating_average=models.FloatField(default=0.0)
    average_response_time=models.FloatField(default=0.0)
    fulfillment_rate=models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    
    # def update_metrics(self):
    #     completed_pos = self.purchaseorder_set.filter(status='completed')
    #     total_completed_pos = completed_pos.count()

    #     # On-Time Delivery Rate
    #     on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now())
    #     self.on_time_delivery_rate = (on_time_deliveries.count() / total_completed_pos) * 100 if total_completed_pos else 0

    #     # Quality Rating Average
    #     self.quality_rating_avg = completed_pos.filter(quality_rating__isnull=False).aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0.0

    #     # Average Response Time
    #     response_times = completed_pos.filter(acknowledgment_date__isnull=False).annotate(response_time=models.F('acknowledgment_date') - models.F('issue_date'))
    #     self.average_response_time = response_times.aggregate(Avg('response_time'))['response_time__avg'].total_seconds() if response_times else 0.0

    #     # Fulfilment Rate
    #     successful_fulfillments = completed_pos.filter(status='completed', quality_rating__isnull=True)
    #     self.fulfillment_rate = (successful_fulfillments.count() / total_completed_pos) * 100 if total_completed_pos else 0

    #     self.save()

class PurchaseOrder(models.Model):
    po_number=models.CharField(max_length=20)
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
    oredr_date=models.DateTimeField()
    delivery_date=models.DateTimeField()
    items=models.JSONField()
    quantity=models.PositiveIntegerField()
    status=models.CharField(max_length=20)
    quality_rating=models.FloatField(null=True,blank=True)
    issue_date=models.DateTimeField()
    acknowledgment_date=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.po_number

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     # Update vendor metrics upon PO completion
    #     if self.status == 'completed':
    #         self.vendor.update_metrics()
    
class HistoricalPerformance(models.Model):
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
    date=models.DateTimeField()
    on_time_delivery_date=models.FloatField()
    quality_rating_avg=models.FloatField()
    average_response_time=models.FloatField()
    fulfillment_rate=models.FloatField()

    def __str__(self):
        return self.vendor
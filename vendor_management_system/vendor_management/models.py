from django.db import models
from django.db.models import Avg, Count, F, ExpressionWrapper, DurationField
from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def update_on_time_delivery_rate(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')
        total_completed_orders = completed_orders.count()
        if total_completed_orders > 0:
            on_time_orders = completed_orders.filter(delivery_date__lte=timezone.now())
            on_time_delivery_rate = (on_time_orders.count() / total_completed_orders) * 100
            self.on_time_delivery_rate = on_time_delivery_rate
            self.save()

    def update_quality_rating_avg(self):
        completed_orders = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
        if completed_orders.exists():
            quality_rating_avg = completed_orders.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
            self.quality_rating_avg = quality_rating_avg
            self.save()

    def update_average_response_time(self):
        completed_orders = self.purchaseorder_set.filter(status='completed', acknowledgment_date__isnull=False)
        if completed_orders.exists():
            avg_response_time = completed_orders.annotate(
                response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())
            ).aggregate(avg_response=Avg('response_time'))['avg_response']
            self.average_response_time = avg_response_time.total_seconds() / 3600  # Convert to hours
            self.save()

    def update_fulfillment_rate(self):
        total_orders = self.purchaseorder_set.count()
        if total_orders > 0:
            successful_orders = self.purchaseorder_set.filter(status='completed')
            fulfillment_rate = (successful_orders.count() / total_orders) * 100
            self.fulfillment_rate = fulfillment_rate
            self.save()

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'completed':
            self.vendor.update_on_time_delivery_rate()
            self.vendor.update_quality_rating_avg()
            self.vendor.update_fulfillment_rate()

    def acknowledge(self):
        if self.status == 'pending':
            self.acknowledgment_date = timezone.now()
            self.save()
            self.vendor.update_average_response_time()

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
from django.db import models
from django.urls import reverse


class TamerCustomer(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=200, verbose_name="Наименование")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        managed = False
        db_table = 'tamer_customer'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tamer-customer-view')


class TamerOpportunity(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    subject = models.TextField(blank=True, null=True, verbose_name="Тема")
    customer = models.ForeignKey(TamerCustomer, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="Заказчик")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        managed = False
        db_table = 'tamer_opportunity'

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('tamer-opportunity-view')


class TamerContract(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    contract = models.TextField(blank=True, null=True, verbose_name="Номер")
    customer = models.ForeignKey(TamerCustomer, on_delete=models.DO_NOTHING, verbose_name="Заказчик")
    amount = models.FloatField(blank=True, null=True, verbose_name="Сумма")
    margin = models.FloatField(blank=True, null=True, verbose_name="Прибыль")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        managed = False
        db_table = 'tamer_contract'

    def __str__(self):
        return self.contract

    def get_absolute_url(self):
        return reverse('tamer-contact-view')


# Integration with contact
try:
    from tamer_app_contact.models import TamerContact
except Exception as e:
    class TamerContactManager(models.Manager):
        def all(self):
            return []

        def get_queryset(self):
            return []


    class TamerContact(models.Model):
        objects = TamerContactManager()


class TamerOpportunityContact(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    opportunity = models.ForeignKey(TamerOpportunity, on_delete=models.DO_NOTHING, verbose_name="Возможность")
    contact = models.ForeignKey(TamerContact, on_delete=models.DO_NOTHING, verbose_name="Контакт")
    description = models.TextField(verbose_name="Дополнительное описание")

    class Meta:
        managed = False
        db_table = 'tamer_opportunity_contact'

    def __str__(self):
        return self.contact.__str__()

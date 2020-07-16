from django.db import models, connections
from django.urls import reverse
from django.utils.safestring import mark_safe


class TamerContact(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=200, verbose_name='Имя')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        managed = False
        db_table = 'tamer_contact'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tamer-contact-view')

    def note(self):
        query = ''' select kc.name, cn.note from tamer_contact_note cn
        join tamer_kind_contact kc on cn.kind_contact_id=kc.id
        where cn.contact_id = %s
        order by kc.sort 
        ''' % self.id
        with connections['default'].cursor() as cursor:
            cursor.execute(query)
            # submenu = [{'title': item[1], 'link': 'task?workflow=%s' % item[0]} for item in cursor.fetchall()]

            note_list = ['<span class="col-2">%s:</span><span class="col-10">%s</span>' % (item[0], item[1]) for
                     item in cursor.fetchall()]
        return mark_safe('\n'.join(note_list))


class TamerKindContact(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=200, verbose_name="Тип информации")
    sort = models.IntegerField(verbose_name="Порядок сортировки")

    class Meta:
        managed = False
        db_table = 'tamer_kind_contact'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tamer-kind-contact-view')


# ToDo добавить признак поля для фильтрации и группировки, например компанию, роль, должность


class TamerContactNote(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    contact = models.ForeignKey(TamerContact, on_delete=models.DO_NOTHING, verbose_name="Контакт")
    kind_contact = models.ForeignKey(TamerKindContact, on_delete=models.DO_NOTHING,
                                     verbose_name="Тип контактной информации")
    note = models.TextField(verbose_name="Контактная информация")

    class Meta:
        managed = False
        db_table = 'tamer_contact_note'

    def __str__(self):
        return self.kind_contact.name + ' ' + self.note


from django.core.urlresolvers import reverse
from django.db import models


# Create your models here.
class List(models.Model):
    text = models.TextField(default='')
    
    
    def get_absolute_url(self):
        #做完List時, 直接導向到這個url, 需在view作設定
        return reverse('lists:viewList', args=(self.id, ))
    

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)
    
    
    def __str__(self):
        return self.text   
    
    
    class Meta:
        ordering = ('id', ) #抓這個model時用id排序
        unique_together = ('list', 'text')

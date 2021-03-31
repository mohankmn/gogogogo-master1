import math
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from math import sqrt
# Create your models here.
def validate_positive(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s is a negative number. It should be >= 0'),
            params={'value': value},
        )

class Goods(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="good")
    good_name           = models.CharField(max_length=100)
    setup_cost          = models.FloatField(help_text='Rs./run', validators=[validate_positive])
    production_cost     = models.FloatField(help_text='Rs./unit', validators=[validate_positive])
    holding_cost        = models.FloatField(help_text='Rs./unit-year', validators=[validate_positive])
    production_rate     = models.FloatField(help_text='units/year', validators=[validate_positive])
    total_demand        = models.FloatField(help_text='units/year', validators=[validate_positive])
    production_quantity = models.FloatField(help_text='units/run', validators=[validate_positive])
    raw_material        = models.ManyToManyField(Product, through='Amount')
    epq                 = models.FloatField(blank=True,null=True)
    def __str__(self):
        return '{} => {}'.format(self.user, self.good_name)

    def save(self, *args, **kwargs):
        self.good_name = self.good_name.upper()
        if self.production_rate >= self.total_demand :
            a = float(self.setup_cost)*float(self.total_demand)
            x=float(self.total_demand)/float(self.production_rate)
            b=float(self.holding_cost)*float(1-x)
            self.epq=math.sqrt(a/b)
        return super().save(*args, **kwargs)



class Amount(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="amount")
    goods           = models.ForeignKey(Goods, on_delete=models.CASCADE)
    raw_mate        = models.ForeignKey(Product, on_delete=models.CASCADE)
    required_amount = models.FloatField(validators=[validate_positive]) 

    # To have unique pairs of goods and raw_material 
    class Meta:
        unique_together = [['goods', 'raw_mate']]

    def __str__(self):
        return '{} - {}'.format(self.goods, self.raw_mate.name)
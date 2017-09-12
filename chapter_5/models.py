from django.core.validators import ValidationError
from django.db import models
from django.utils.translation import (
    ugettext,
    ugettext_lazy,
)


def date_is_not_allowed(given_date):
    forbidden_dates = (
        (1, 1),  # New year
        (25, 12),  # Christmas
    )
    for day, month in forbidden_dates:
        if given_date.day == day and given_date.month == month:
            return True


class Result(models.Model):
    error_msg_forbidden_date = ugettext_lazy(
        'Field contains not allowed date.'
    )

    date_from = models.DateField(verbose_name=ugettext_lazy('From'))
    date_to = models.DateField(verbose_name=ugettext_lazy('To'))
    value = models.FloatField(verbose_name=ugettext_lazy('Value'))

    class Meta:
        verbose_name = ugettext_lazy('Result')
        verbose_name_plural = ugettext_lazy('Results')

    def clean(self):
        if self.date_from and date_is_not_allowed(self.date_from):
            raise ValidationError({
                'date_from': self.error_msg_forbidden_date,
            })

        if self.date_to and date_is_not_allowed(self.date_to):
            raise ValidationError({
                'date_to': self.error_msg_forbidden_date,
            })

        if self.date_from and self.date_to:
            if self.date_from > self.date_to:
                raise ValidationError(
                    ugettext('Date from cannot be after date to.')
                )
            elif self.date_from == self.date_to:
                raise ValidationError(
                    ugettext('Dates cannot equal.')
                )

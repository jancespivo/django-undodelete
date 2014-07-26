from django.dispatch import Signal

pre_soft_delete = Signal(providing_args=['instance', 'queryset'])
post_soft_delete = Signal(providing_args=['instance', 'queryset'])

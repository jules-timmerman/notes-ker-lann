import functools
import json
import operator

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class InstancedPermission:

    def __init__(self, model, query, type, field):
        self.model = model
        self.query = query
        self.type = type
        self.field = field

    def applies(self, obj, permission_type, field_name=None):
        """
        Returns True if the permission applies to
        the field `field_name` object `obj`
        """
        if ContentType.objects.get_for_model(obj) != self.model:
            # The permission does not apply to the model
            return False
        if self.permission is None:
            if permission_type == self.type:
                if field_name is not None:
                    return field_name == self.field
                else:
                    return True
            else:
                return False
        elif obj in self.model.objects.get(self.query):
            return True
        else:
            return False

    def __repr__(self):
        if self.field:
            return _("Can {type} {model}.{field} in {permission}").format(type=self.type, model=self.model, field=self.field, permission=self.permission)
        else:
            return _("Can {type} {model} in {permission}").format(type=self.type, model=self.model, permission=self.permission)


class Permission(models.Model):

    PERMISSION_TYPES = [
        ('add', 'add'),
        ('view', 'view'),
        ('change', 'change'),
        ('delete', 'delete')
    ]

    model = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='+')

    # A json encoded Q object with the following grammar
    #  query -> [] | {}  (the empty query representing all objects)
    #  query -> ['AND', query, …]
    #        -> ['OR', query, …]
    #        -> ['NOT', query]
    #  query -> {key: value, …}
    #  key   -> string
    #  value -> int | string | bool | null
    #        -> [parameter]
    #
    # Examples:
    #  Q(is_admin=True)  := {'is_admin': ['TYPE', 'bool', 'True']}
    #  ~Q(is_admin=True) := ['NOT', {'is_admin': ['TYPE', 'bool', 'True']}]
    query = models.TextField()

    type = models.CharField(max_length=15, choices=PERMISSION_TYPES)

    field = models.CharField(max_length=255, blank=True)

    description = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('model', 'query', 'type', 'field')

    def clean(self):
        if self.field and self.type not in {'view', 'change'}:
            raise ValidationError(_("Specifying field applies only to view and change permission types."))

    def save(self):
        self.full_clean()
        super().save()

    def _about(_self, _query, **kwargs):
        self = _self
        query = _query
        if len(query) == 0:
            # The query is either [] or {} and
            # applies to all objects of the model
            # to represent this we return None
            return None
        if isinstance(query, list):
            if query[0] == 'AND':
                return functools.reduce(operator.and_, [self._about(query, **kwargs) for query in query[1:]])
            elif query[0] == 'OR':
                return functools.reduce(operator.or_, [self._about(query, **kwargs) for query in query[1:]])
            elif query[0] == 'NOT':
                return ~self._about(query[1], **kwargs)
        elif isinstance(query, dict):
            q_kwargs = {}
            for key in query:
                value = query[key]
                if isinstance(value, list):
                    # It is a parameter we query its primary key
                    q_kwargs[key] = kwargs[value[0]].pk
                else:
                    q_kwargs[key] = value
            return Q(**q_kwargs)
        else:
            # TODO: find a better way to crash here
            raise Exception("query {} is wrong".format(self.query))

    def about(self, **kwargs):
        """
        Return an InstancedPermission with the parameters
        replaced by their values and the query interpreted
        """
        query = json.loads(self.query)
        query = self._about(query, **kwargs)
        return InstancedPermission(self.model, query, self.type, self.field)

    def __str__(self):
        if self.field:
            return _("Can {type} {model}.{field} in {query}").format(type=self.type, model=self.model, field=self.field, query=self.query)
        else:
            return _("Can {type} {model} in {query}").format(type=self.type, model=self.model, query=self.query)


class UserPermission(models.Model):

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)


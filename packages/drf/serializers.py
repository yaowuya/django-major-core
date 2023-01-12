# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField


class ManyToManyRelatedField(serializers.RelatedField):
    """自定义m2m关系字段, 用作既返回id, 也返回name"""

    def __init__(self, **kwargs):
        self.pk_field = kwargs.pop("pk_field", None)
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)
        return self.get_queryset().get(pk=data)

    def to_representation(self, value):
        return {"id": value.pk, "name": str(value)}


class ReadWriteSerializerMethodField(SerializerMethodField):
    """
    支持可读写的SerializerMethodField
    可实现Model字段和Serializer字段更加灵活地解绑
    通过实现get_xxx_field方法，实现从Model的某个字段读值映射到Serializer对应字段
    通过实现set_xxx_field方法，实现从Serializer字段回填值到Model对应字段
    """

    def __init__(self, method_name=None, write_method_name=None, **kwargs):
        self.method_name = method_name
        self.write_method_name = write_method_name
        kwargs["source"] = "*"
        super(SerializerMethodField, self).__init__(**kwargs)

    def bind(self, field_name, parent):
        default_method_name = f"get_{field_name}"
        default_write_method_name = f"set_{field_name}"

        if self.method_name is None:
            self.method_name = default_method_name
        if self.write_method_name is None:
            self.write_method_name = default_write_method_name
        super(SerializerMethodField, self).bind(field_name, parent)

    def to_representation(self, value):
        method = getattr(self.parent, self.method_name)
        return method(value)

    def to_internal_value(self, data):
        method = getattr(self.parent, self.write_method_name)
        return method(data)

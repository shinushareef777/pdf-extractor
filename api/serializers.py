from rest_framework.serializers import ModelSerializer
from .models import BelegNumber, Entry
from rest_framework import serializers

class BelegNumberSerializer(ModelSerializer):
  class Meta:
    model = BelegNumber
    fields = "__all__"

class EntrySerializer(ModelSerializer):
    class Meta:
        model = Entry
        fields = "__all__"


class EntryDetailSerializer(ModelSerializer):
    assigned_integer = serializers.IntegerField(
        source="beleg_number_id.assigned_integer", read_only=True
    )

    class Meta:
        model = Entry
        fields = ["pos_number", "product_number", "beleg_number_id", "assigned_integer"]

from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'


class BaseDetailSerializer(BaseModelSerializer):
    pass


class BaseListCreateSerializer(BaseDetailSerializer):
    def create(self, validated_data):
        self.modify_input(validated_data)
        return super().create(validated_data)

    def modify_input(self, validated_data):
        return


class BaseUpdateDetailSerializer(BaseDetailSerializer):
    def update(self, instance, validated_data):
        self.modify_validated_data(instance, validated_data)
        return super().update(instance, validated_data)

    def modify_validated_data(self, instance, validated_data):
        unmodified_field_names = [
            attr for attr, val in validated_data.items()
            if getattr(instance, attr, None) == val
        ]
        for attr in unmodified_field_names:
            validated_data.pop(attr, None)

        setattr(self, 'modified_data_dict', validated_data)

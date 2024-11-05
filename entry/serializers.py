from rest_framework import serializers
from entry.models import GuestEntry,User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='name', read_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'created_at')

class UserEntryReadSerializer(serializers.ModelSerializer):
    total_messages = serializers.IntegerField(read_only=True)
    last_entry = serializers.SerializerMethodField()
    username = serializers.CharField(source='name', read_only=True)

    def get_last_entry(self, obj):
        last_entry = obj.guest_user.order_by('-created_at').first()
        if last_entry:
            return f"{last_entry.subject} | {last_entry.message}"
        return None

    class Meta:
        model = User
        fields = ('username', 'total_messages', 'last_entry')
    
class GuestEntryCreateSerializer(serializers.Serializer):
    subject = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
    name = serializers.CharField(write_only=True,required=True)


    def create(self, validated_data):
        name = validated_data.get('name')
        
        # Check if user is unique
        user, created = User.objects.get_or_create(name=name)
        
        validated_data.pop('name', None)  # Remove name from validated_data if it exists  
        guest_entry = GuestEntry.objects.create(user=user, **validated_data)

        return guest_entry
    
class GuestEntryReadSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = GuestEntry
        fields = ('user','subject','message')



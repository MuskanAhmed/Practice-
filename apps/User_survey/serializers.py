from rest_framework import serializers
from apps.User_survey.models import Question, Option, UserResponse,WaitlistEntry

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'options']


class UserResponseSerializer(serializers.ModelSerializer):
    selected_options = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Option.objects.all()
    )

    class Meta:
        model = UserResponse
        fields = ['question', 'selected_options', 'text_answer']

class WaitlistEntrySerializer(serializers.ModelSerializer):
    responses = UserResponseSerializer(many=True)
    class Meta:
        model = WaitlistEntry
        fields = ['first_name', 'last_name', 'email', 'company', 'responses']

    def create(self, validated_data):
        responses_data = validated_data.pop('responses')
        waitlist_entry = WaitlistEntry.objects.create(**validated_data)

        for response_data in responses_data:
            selected_options = response_data.pop('selected_options', [])
        
            user_response = UserResponse.objects.create(waitlist_entry=waitlist_entry,**response_data)
        
            user_response.selected_options.set(selected_options)

        return waitlist_entry


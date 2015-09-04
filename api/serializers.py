from rest_framework import serializers

from api.models import Person, Message, Comment, News, Words, SystemMsg, Feedback, CampusAmbassador


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            'token', 'created', 'phone_number', 'password', 'name', 'portrait', 'location')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id', 'what', 'title', 'time', 'latlng', 'kind', 'information', 'image1', 'image2', 'image3', 'created',
            'contact_phone', 'commit_person', 'comments_number',
            'reading_number', 'share_number', 'location', 'commit_location')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'commit_person', 'content', 'created', 'message', 'news', 'to_person')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = (
        'id', 'title', 'information', 'image1', 'image2', 'image3', 'created', 'commit_person', 'comments_number',
        'reading_number', 'followers', 'following_number', 'share_number')


class WordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Words
        fields = ('id', 'created', 'content', 'to_person', 'from_person', 'if_read')


class SystemMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemMsg
        fields = ('id', 'content', 'created')


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('content', 'created', 'contact')


class CampusAmbassadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusAmbassador
        fields = ('name', 'school', 'grade', 'slogan', 'resume', 'experience')

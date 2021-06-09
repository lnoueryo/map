from users.models import NewUser, NewUser
from rest_framework import exceptions, serializers

class RegisterUserSerializer(serializers.ModelSerializer):
    confirmation_password = serializers.CharField(write_only=True, required=True)
    class Meta: #　表示したり、create時のrequiredのキー
        model = NewUser
        fields = ('email', 'user_name', 'password', 'confirmation_password',)#required?? 
        extra_kwargs = {'password': {'write_only': True}}#write_onlyなのでpasswordはkeyに入らない
        # read_only_fields = ('name',) 特定のカラムを読み込み専用(更新不可)
    def create(self, validated_data): #validated_dataはviews.pyから入ってくるデータ
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('confirmation_password')
        if password != confirm_password:
            raise serializers.ValidationError('パスワードが一致していません')
        return data

class UserSerializer(serializers.ModelSerializer):

    # time_since_publication = serializers.SerializerMethodField()

    class Meta:
        model = NewUser
        exclude  = ('password', 'email',)
        # fields = ('__all__')

    # def get_time_since_publication(self, object):
    #     publication_date = object.publication_date
    #     now = datetime.now()
    #     time_delta = timesince(publication_date, now)
    #     return time_delta
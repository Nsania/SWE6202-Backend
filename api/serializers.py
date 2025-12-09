from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Parent, Student, AttendanceLog, StudentBusPass, BusPassRequest
from django.db import transaction
from .schedule_utils import get_student_schedule_by_id
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):

        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        
        self.context['refresh_token'] = str(refresh)
        self.context['access_token'] = str(refresh.access_token)

        del data['refresh']
        del data['access']

        role = 'unknown'
        
        if self.user.is_staff:
            role = 'admin'

        elif hasattr(self.user, 'parent_profile'):
            role = 'parent'

        elif hasattr(self.user, 'student_profile'):
            role = 'student'
        
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'role': role
        }
        
        return data
    
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField(required=False)

    def validate(self, attrs):
        refresh_token = self.context['request'].COOKIES.get('refresh_token')
        
        if not refresh_token:
            raise serializers.ValidationError("No refresh token found in cookies.")
            
        attrs['refresh'] = refresh_token
        
        data = super().validate(attrs)
        
        self.context['access_token'] = data['access']
        
        if 'refresh' in data:
             self.context['refresh_token'] = data['refresh']

        return data

class ParentRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    child_university_id = serializers.CharField(write_only=True, required=True)
    child_registration_code = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Parent
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'phone_number',
            'child_university_id',
            'child_registration_code',
        )

    def validate(self, data):
        try:
            student = Student.objects.get(university_id=data['child_university_id'])
        except Student.DoesNotExist:
            raise serializers.ValidationError("No student found with this university id")
        
        if student.registration_code != data['child_registration_code']:
            raise serializers.ValidationError("Registration code is incorrect for this student")
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("An account with this email already exists")
        
        data['student_to_link'] = student
        return data
            
    @transaction.atomic
    def create(self, validated_data):
        user_account = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        parent_profile = Parent.objects.create(
            user=user_account,
            phone_number=validated_data.get('phone_number', '') 
        )
        
        student = validated_data['student_to_link']
        parent_profile.children.add(student)
        
        return parent_profile

class ParentProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Parent
        fields = (
            'id', 
            'first_name', 
            'last_name', 
            'email', 
            'phone_number', 
            'created_at'
        )

class StudentProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = Student
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'university_id',
            'registration_code',
            'schedule_id',
            'created_at'
        )
        read_only_fields = fields

class StudentScheduleSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    schedule_details = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = (
            'first_name',
            'last_name',
            'university_id',
            'schedule_id',
            'schedule_details'
        )

    def get_schedule_details(self, obj):
        try:
            return get_student_schedule_by_id(obj.schedule_id)
        except Exception as e:
            return {"error": str(e)}

class StudentBusPassSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(
        slug_field='university_id',
        queryset=Student.objects.all()
    )

    class Meta:
        model = StudentBusPass
        fields = [
            'id',
            'student',
            'reason',
            'valid_from',
            'valid_until',
            'admin_who_granted',
            'used_at',
        ]
        read_only_fields = ['admin_who_granted', 'used_at']

class AttendanceLogSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(source='student.university_id', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    
    class Meta:
        model = AttendanceLog
        fields = [
            'id',
            'student_id',
            'student_name',
            'timestamp',
            'bus_number',
            'status',
            'direction',
        ]


class ParentBasicProfileSerializer(serializers.ModelSerializer): 
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Parent
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number'
        ]


class BusPassRequestSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    class Meta:
        model = BusPassRequest
        fields = [
            'id',
            'student',
            'student_name',
            'status',
            'request_date',
            'requested_valid_from',
            'requested_valid_until',
            'reason',
            'admin_notes',
            'approved_valid_from',
            'approved_valid_until'
        ]
        read_only_fields = ['id', 'student', 'status', 'request_date', 'admin_notes', 'approved_valid_from', 'approved_valid_until']

    def get_student_name(self, obj):
        if obj.student.user:
            return obj.student.user.get_full_name()
        return obj.student.university_id
    

class AdminStudentDetailSerializer(serializers.ModelSerializer):
   
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    schedule_details = serializers.SerializerMethodField()
    parents = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id',
            'university_id',
            'first_name',
            'last_name',
            'email',
            'registration_code',
            'schedule_id',
            'schedule_details',
            'parents',
            'created_at'
        ]

    def get_schedule_details(self, obj):
        try:
            return get_student_schedule_by_id(obj.schedule_id)
        except Exception:
            return None

    def get_parents(self, obj):
        parents = obj.parents.all()
        return [
            {
                "id": p.id,
                "name": f"{p.user.first_name} {p.user.last_name}" if p.user else "Unknown",
                "phone": p.phone_number,
                "email": p.user.email if p.user else "Unknown"
            }
            for p in parents
        ]
    
class AdminParentDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    children = serializers.SerializerMethodField()

    class Meta:
        model = Parent
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'children',
            'created_at'
        ]

    def get_children(self, obj):
        children = obj.children.all()
        return [
            {
                "university_id": child.university_id,
                "name": f"{child.user.first_name} {child.user.last_name}" if child.user else "Unknown",
                "schedule_id": child.schedule_id
            }
            for child in children
        ]
    

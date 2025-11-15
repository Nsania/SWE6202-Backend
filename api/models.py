from django.db import models
from django.contrib.auth.models import User
import uuid

def generate_code():
    while True:
        code = str(uuid.uuid4().hex)[:10].upper()

        if not Student.objects.filter(registration_code=code).exists():
            return code

class Student(models.Model):
    university_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
    )
    
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_profile"
    )
    university_email = models.EmailField(unique=True)
    personal_email = models.EmailField(blank=True, null=True)
    
    registration_code = models.CharField(
        max_length=10, 
        unique=True,
        default=generate_code
    )
    
    schedule_id = models.CharField(max_length=50, blank=True, null=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name} ({self.university_id})"
        return f"Student Profile ({self.university_id}) - Unclaimed"
         

class Parent(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="parent_profile",
    )
    phone_number = models.CharField(max_length=255)
    children = models.ManyToManyField(
        Student,
        related_name="parents",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class AttendanceLog(models.Model):

    class ScanStatus(models.TextChoices):
        VALID = 'VALID', 'Valid Scan'
        INVALID = 'INVALID', 'Invalid Scan'
        OVERRIDE = 'OVERRIDE', 'Admin Pass Used'

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="attendance_logs", db_index=True
    )
    timestamp = models.DateTimeField(db_index=True)
    bus_number = models.CharField(
        max_length=50, blank=True, null=True
    )
    status = models.CharField(
        max_length=10, choices=ScanStatus.choices, db_index=True
    )
    
    def __str__(self):
        return f"[{self.status}] {self.student.university_id} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-timestamp']
    

class StudentBusPass(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="bus_passes", db_index=True
    )

    admin_who_granted = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    reason = models.TextField(blank=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Used" if self.used_at else "Active"
        return f"Pass for {self.student.university_id} (Status: {status})"
    
    class Meta:
        ordering = ['-valid_from']
    

#testchange
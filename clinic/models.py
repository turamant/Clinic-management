from django.db import models


class Clinic(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=50)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=50)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='doctors')

    def __str__(self):
        return f'{self.specialization}:{self.user.username}'


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedule')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor.user.username} - {self.date} ({self.start_time} - {self.end_time})"


class Room(models.Model):
    number = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='rooms')
    capacity = models.IntegerField()

    def __str__(self):
        return f'Кабинет № {self.number}'


class Patient(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    medical_history = models.TextField()

    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('cancelled', 'Cancelled'),
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_schedule = models.ForeignKey(DoctorSchedule, null=True, on_delete=models.CASCADE, related_name='appointments')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return (f"Доктор:{self.doctor.user.username}/Пациент:{self.patient.user.username}"
                f"/ дата:{self.doctor_schedule.date}/ время:{self.doctor_schedule.start_time}"
                f"/ status:{self.status}")


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return self.patient.user.username


class Comment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author}:{self.doctor}'

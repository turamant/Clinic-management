from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from .forms import AppointmentForm
from .models import Clinic, Department, Doctor, Patient, Room, Appointment, MedicalRecord, DoctorSchedule


def dashboard(request):
    # Получаем список всех докторов
    doctors = Doctor.objects.all()

    # Получаем список всех пациентов
    patients = Patient.objects.all()

    # Получаем список всех клиник
    clinics = Clinic.objects.all()

    # Получаем список всех департаментов
    departments = Department.objects.all()

    # Получаем список всех кабинетов
    rooms = Room.objects.all()

    appointments = Appointment.objects.all()

    medical_records = MedicalRecord.objects.all()

    context = {
        'doctors': doctors,
        'patients': patients,
        'clinics': clinics,
        'departments': departments,
        'rooms': rooms,
        'appointments': appointments,
        'medical_records': medical_records,
    }

    return render(request, 'clinic/dashboard.html', context)

def clinic_list(request):
    clinics = Clinic.objects.all()
    return render(request, 'clinic/clinic_list.html', {'clinics': clinics})

def clinic_detail(request, pk):
    clinic = get_object_or_404(Clinic, pk=pk)
    return render(request, 'clinic/clinic_detail.html', {'clinic': clinic})

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'clinic/department_list.html', {'departments': departments})

def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    return render(request, 'clinic/department_detail.html', {'department': department})

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'clinic/room_list.html', {'rooms': rooms})

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'clinic/room_detail.html', {'room': room})


def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'clinic/appointment_list.html', {'appointments': appointments})


def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'clinic/appointment_detail.html', {'appointment': appointment})


def medical_record_list(request):
    medical_records = MedicalRecord.objects.all()
    return render(request, 'clinic/medical_record_list.html', {'medical_records': medical_records})


def medical_record_detail(request, pk):
    medical_record = get_object_or_404(MedicalRecord, pk=pk)
    return render(request, 'clinic/medical_record_detail.html', {'medical_record': medical_record})


# @login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'clinic/patient_list.html', {'patients': patients})

def patient_detail(request, pk):
    patient = Patient.objects.get(pk=pk)
    appointments = Appointment.objects.filter(patient=patient)
    return render(request, 'clinic/patient_detail.html',
                  {'patient': patient,
                   'appointments': appointments,
                   })


@login_required
@permission_required('patients.add_patient')
def patient_create(request):
    if request.method == 'POST':
        # Обработка формы создания пациента
        pass
    return render(request, 'clinic/patient_form.html')

# @login_required
# @permission_required('patients.change_patient')
def patient_update(request, pk):
    patient = Patient.objects.get(pk=pk)
    if request.method == 'POST':
        # Обработка формы обновления пациента
        pass
    return render(request, 'clinic/patient_form.html', {'patient': patient})

@login_required
@permission_required('patients.delete_patient')
def patient_delete(request, pk):
    patient = Patient.objects.get(pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'clinic/patient_confirm_delete.html', {'patient': patient})


def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'clinic/doctor_list.html', {'doctors': doctors})

def doctor_detail(request, pk):
    doctor = Doctor.objects.get(pk=pk)
    appointments = Appointment.objects.filter(doctor=doctor)
    doctor_schedule = DoctorSchedule.objects.filter(doctor=doctor, is_available=True)
    return render(request, 'clinic/doctor_detail.html',
                  {'doctor': doctor,
                   'appointments': appointments,
                   'doctor_schedule': doctor_schedule
                   })


def doctor_schedule_create(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        DoctorSchedule.objects.create(doctor=doctor, date=date, start_time=start_time, end_time=end_time)
        return redirect('clinic:doctor_detail', pk=pk)
    return render(request, 'doctor_schedule_form.html', {'doctor': doctor})


def appointment_create(request, pk):
    doctor_schedule = get_object_or_404(DoctorSchedule, pk=pk)
    if request.method == 'POST':
        patient = request.user.patient
        appointment = Appointment.objects.create(doctor=doctor_schedule.doctor,
                                                 patient=patient,
                                                 doctor_schedule=doctor_schedule)
        appointment.save()
        doctor_schedule.is_available = False
        doctor_schedule.save()
        return redirect('clinic:patient_detail', pk=patient.pk)
    return render(request, 'clinic/appointment_form.html',
                  {'doctor_schedule': doctor_schedule})




@login_required
@permission_required('doctors.add_doctor')
def doctor_create(request):
    if request.method == 'POST':
        # Обработка формы создания пациента
        pass
    return render(request, 'doctor/doctor_form.html')

# @login_required
# @permission_required('doctors.change_doctor')
def doctor_update(request, pk):
    doctor = Doctor.objects.get(pk=pk)
    if request.method == 'POST':
        # Обработка формы обновления пациента
        pass
    return render(request, 'clinic/doctor_form.html', {'doctor': doctor})

# @login_required
# @permission_required('doctors.delete_doctor')
def doctor_delete(request, pk):
    doctor = Doctor.objects.get(pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctor_list')
    return render(request, 'clinic/doctor_confirm_delete.html', {'doctor': doctor})


def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = 'pending'
            appointment.save()
            return redirect('clinic:dashboard')
    else:
        form = AppointmentForm()

    return render(request, 'clinic/appointment_form.html', {'form': form})
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from clinics.models import Specialty, InsuranceProvider, Clinic
from patients.models import Patient
from referrals.models import Referral
from audit.models import AuditLog

CustomUser = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with Indian medical system data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting existing database records...")
        AuditLog.objects.all().delete()
        Referral.objects.all().delete()
        Patient.objects.all().delete()
        Clinic.objects.all().delete()
        CustomUser.objects.all().delete()
        Specialty.objects.all().delete()
        InsuranceProvider.objects.all().delete()

        self.stdout.write("Seeding Specialties...")
        specs_names = ['Cardiology', 'Dermatology', 'Orthopedics', 'Neurology', 'Pediatrics', 'Oncology', 'ENT', 'Psychiatry']
        specs = {}
        for name in specs_names:
            specs[name] = Specialty.objects.create(name=name)

        self.stdout.write("Seeding Indian Insurance Providers...")
        insurances_names = ['Star Health Insurance', 'HDFC Ergo', 'ICICI Lombard', 'Ayushman Bharat (PM-JAY)', 'Care Health Insurance', 'Niva Bupa', 'SBI General Insurance']
        insurances = {}
        for name in insurances_names:
            insurances[name] = InsuranceProvider.objects.create(provider_name=name)

        self.stdout.write("Seeding Indian Clinicians and Admins...")
        # Superuser
        superuser = CustomUser.objects.create_superuser('admin', 'admin@referral.in', 'admin123', first_name='System', last_name='Administrator')
        
        # Doctors (Indian names)
        doc1 = CustomUser.objects.create_user('dr_gupta', 'ramesh.gupta@referral.in', 'doctor123', first_name='Ramesh', last_name='Gupta', role='DOCTOR')
        doc2 = CustomUser.objects.create_user('dr_sharma', 'sunita.sharma@referral.in', 'doctor123', first_name='Sunita', last_name='Sharma', role='DOCTOR')
        
        # Clinic Admins
        cadmin1 = CustomUser.objects.create_user('admin_apollo', 'apollo@referral.in', 'admin123', first_name='Anil', last_name='Mehta', role='CLINIC_ADMIN')
        cadmin2 = CustomUser.objects.create_user('admin_medanta', 'medanta@referral.in', 'admin123', first_name='Sanjay', last_name='Verma', role='CLINIC_ADMIN')
        cadmin3 = CustomUser.objects.create_user('admin_maitri', 'maitri@referral.in', 'admin123', first_name='Karan', last_name='Joshi', role='CLINIC_ADMIN')
        cadmin4 = CustomUser.objects.create_user('admin_sector9', 'sector9@referral.in', 'admin123', first_name='Rajesh', last_name='Rao', role='CLINIC_ADMIN')

        self.stdout.write("Seeding Indian Specialized Clinics (Hospitals)...")
        # 1. Indraprastha Apollo Hospital (New Delhi)
        c1 = Clinic.objects.create(
            clinic_name='Indraprastha Apollo Hospital',
            address='Mathura Rd, Sarita Vihar',
            city='New Delhi',
            latitude=28.5359,
            longitude=77.2878,
            contact_number='+91 11 2692 5858',
            estimated_wait_days=4,
            description='A multi-specialty state-of-the-art facility. Known as one of the premier institutions for cardiovascular care, angioplasty, and heart transplants in Delhi NCR.',
            admin=cadmin1
        )
        c1.specialties.add(specs['Cardiology'], specs['Oncology'])
        c1.insurance_providers.add(insurances['Star Health Insurance'], insurances['HDFC Ergo'], insurances['ICICI Lombard'])

        # 2. Medanta - The Medicity (Gurugram / Delhi NCR)
        c2 = Clinic.objects.create(
            clinic_name='Medanta - The Medicity',
            address='CH Baktawar Singh Road, Sector 38',
            city='Gurugram',
            latitude=28.4376,
            longitude=77.0425,
            contact_number='+91 124 414 1414',
            estimated_wait_days=3,
            description='Medanta houses renowned clinical teams specializing in complex orthopedics, joint reconstruction, spinal therapies, and neurology.',
            admin=cadmin2
        )
        c2.specialties.add(specs['Orthopedics'], specs['Neurology'])
        c2.insurance_providers.add(insurances['Star Health Insurance'], insurances['Care Health Insurance'], insurances['Niva Bupa'], insurances['HDFC Ergo'])

        # 3. Maitri Hospital (Bhilai, Chhattisgarh)
        c3 = Clinic.objects.create(
            clinic_name='Maitri Hospital & Research Centre',
            address='G.E. Road, Risali',
            city='Bhilai',
            latitude=21.1923,
            longitude=81.3211,
            contact_number='+91 788 226 1500',
            estimated_wait_days=1,
            description='A leading community multi-specialty hospital in Bhilai. Highly reputed for child healthcare, neonatology (NICU), and orthopedic trauma management.',
            admin=cadmin3
        )
        c3.specialties.add(specs['Pediatrics'], specs['Orthopedics'])
        c3.insurance_providers.add(insurances['Ayushman Bharat (PM-JAY)'], insurances['Star Health Insurance'], insurances['SBI General Insurance'])

        # 4. JLN Sector 9 General Hospital (Bhilai, Chhattisgarh)
        c4 = Clinic.objects.create(
            clinic_name='Jawaharlal Nehru Hospital & Research Centre (Sector 9)',
            address='Sector 9, Bhilai Steel Plant Area',
            city='Bhilai',
            latitude=21.2052,
            longitude=81.3418,
            contact_number='+91 788 285 2444',
            estimated_wait_days=2,
            description='Established by BSP, this central medical hospital features complete trauma, cardiac diagnostics, and general pediatrics services for the region.',
            admin=cadmin4
        )
        c4.specialties.add(specs['Cardiology'], specs['Pediatrics'], specs['ENT'])
        c4.insurance_providers.add(insurances['Star Health Insurance'], insurances['Ayushman Bharat (PM-JAY)'], insurances['ICICI Lombard'])

        self.stdout.write("Seeding Patients with Indian names and addresses...")
        # Patients for Dr. Ramesh Gupta (Bhilai / Delhi)
        p1 = Patient.objects.create(
            first_name='Aarav',
            last_name='Sharma',
            age=24,
            gender='MALE',
            phone='+91 98765 43210',
            insurance_provider=insurances['Star Health Insurance'],
            address='Quarter 12B, Street 18, Sector 6, Bhilai, Chhattisgarh',
            created_by=doc1
        )
        
        p2 = Patient.objects.create(
            first_name='Priya',
            last_name='Patel',
            age=38,
            gender='FEMALE',
            phone='+91 87654 32109',
            insurance_provider=insurances['HDFC Ergo'],
            address='Flat 403, Royal Residency, Andheri West, Mumbai, Maharashtra',
            created_by=doc1
        )

        # Patients for Dr. Sunita Sharma
        p3 = Patient.objects.create(
            first_name='Amit',
            last_name='Verma',
            age=55,
            gender='MALE',
            phone='+91 76543 21098',
            insurance_provider=insurances['Ayushman Bharat (PM-JAY)'],
            address='H-16, 2nd Floor, Dwarka Sector 10, New Delhi',
            created_by=doc2
        )

        p4 = Patient.objects.create(
            first_name='Ananya',
            last_name='Rao',
            age=62,
            gender='FEMALE',
            phone='+91 65432 10987',
            insurance_provider=insurances['ICICI Lombard'],
            address='254, 8th Main, Indiranagar, Bangalore, Karnataka',
            created_by=doc2
        )

        self.stdout.write("Seeding sample referrals...")
        # 1. Referral from Dr. Ramesh Gupta to Sector 9 Cardiology for Aarav Sharma
        ref1 = Referral.objects.create(
            patient=p1,
            doctor=doc1,
            clinic=c4,
            specialty=specs['Cardiology'],
            referral_notes='Patient Aarav Sharma, 24 years, experiencing chest heaviness and palpitations during high-intensity training. ECG reveals minor sinus arrhythmia. Refer for treadmill test and senior cardiac consultation.',
            status='PENDING'
        )

        # 2. Referral from Dr. Ramesh Gupta to Maitri Hospital for Aarav Sharma
        ref2 = Referral.objects.create(
            patient=p1,
            doctor=doc1,
            clinic=c3,
            specialty=specs['Orthopedics'],
            referral_notes='Grade 2 ankle sprain with persistent swelling. Patient has tried cold fermentation and bracing for 2 weeks without relief. Referral for physio rehabilitation program.',
            status='ACCEPTED'
        )

        # 3. Referral from Dr. Sunita Sharma to Apollo Hospital Cardiology for Amit Verma
        ref3 = Referral.objects.create(
            patient=p3,
            doctor=doc2,
            clinic=c1,
            specialty=specs['Cardiology'],
            referral_notes='Patient Amit Verma, 55 years, chronic hypertension. Presents with exertional dyspnea and family history of CAD. Referred for diagnostic angiogram and Echo.',
            status='COMPLETED'
        )

        # 4. Referral from Dr. Sunita Sharma to Medanta Neurology for Ananya Rao
        ref4 = Referral.objects.create(
            patient=p4,
            doctor=doc2,
            clinic=c2,
            specialty=specs['Neurology'],
            referral_notes='Post-stroke rehabilitation follow-up. Patient shows slight weakness on left side extremities. Referred for neuro-physiotherapy assessment.',
            status='ACCEPTED'
        )

        self.stdout.write(self.style.SUCCESS("Indian-centric dataset successfully seeded!"))

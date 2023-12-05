from django.shortcuts import render
import pymysql

# Create your views here.
def login(request):
    return render(request, 'Patient/Login.html')

def PatientSignup(request):
    return render(request, 'Patient/Register.html')

def PatientRegAction(request):
    p_name = request.POST['name']
    p_dob=request.POST['dob']
    p_address = request.POST['address']
    p_mobile = request.POST['mobile']
    p_email = request.POST['email']
    p_disease = request.POST['disease']
    p_condition=request.POST['condition']


    con = pymysql.connect(host='localhost', user='root', password='root', database='healthcare')
    cur = con.cursor()
    cur.execute("select * from patient where p_name='"+p_name+"' and Phone='"+p_mobile+"'and EmailID='"+p_email+"'");
    a = cur.fetchone()
    if a is not None:
        context = {'data': 'You Already Registered'}
        return render(request, 'Patient/Register.html', context)
    else:
        cur1 = con.cursor()
        i = cur1.execute("insert into patient values(null,'"+p_name+"','"+p_dob+"','"+p_address+"','"+p_mobile+"','"+p_email+"','"+p_disease+"','"+p_condition+"')")
        con.commit()
        if i > 0:
            context = {'data': 'Patient Registered Successfully..!!'}
            return render(request, 'Patient/Register.html', context)
        else:
            context = {'data': 'Patient Adding Failed...!!'}
            return render(request, 'Patient/Register.html', context)

def LogAction(request):
    p_mobile = request.POST['mobile']
    p_email = request.POST['email']

    con = pymysql.connect(host='localhost', user='root', password='root', database='healthcare')
    cur = con.cursor()
    cur.execute("select * from patient where  Phone='"+p_mobile+"'and EmailID='"+p_email+"'");
    a = cur.fetchone()
    if a is not None:
        request.session['p_id']=a[0]
        request.session['p_mobile']=a[4]
        request.session['p_email']=a[5]
        return render(request, 'Patient/PatientHome.html')
    else:
        context = {'data': 'Login Failed..!!'}
        return render(request, 'Patient/Login.html', context)

def patienthome(request):
    return render(request, 'Patient/PatientHome.html')

def viewdoctors(request):
    con=pymysql.connect(host="localhost",user="root",password="root",database="healthcare")
    cur=con.cursor()
    cur.execute("select * from admin a, doctor d where a.hsp_id=d.hsp_id")
    data=cur.fetchall()
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Hospital Name</th><th>Hospital Address</th><th>Contact</th><th>Doctor Name</th><th>Speciality</th><th>Appointment Timing</th>" \
            "<th>Mobile</th><th>Status</th> </tr></thead>"
    k=0
    for i in data:
        k=k+1
        strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                "<td>"+str(i[6])+"</td><td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[9])+"</td><td><a href='AppointmentAction?doctor_id="+str(i[4])+"&hsp_add="+str(i[2])+"'>Click Appointment</a></td></tr></tbody>"
    context={'data': strdata}
    return render(request, 'Patient/ViewDoctors.html', context)
def AppointmentAction(request):
    d_id=request.GET['doctor_id']
    h_add=request.GET['hsp_add']

    request.session['d_id']=d_id
    request.session['h_add']=h_add
    return render(request,'Patient/Appointment.html')

def BookAppointmentAction(request):

    did = request.POST['d_id']
    p_address=request.POST['address']
    p_problem = request.POST['problem']
    p_id = request.session['p_id']
    pid=str(p_id)


    con = pymysql.connect(host='localhost', user='root', password='root', database='healthcare')
    cur = con.cursor()
    i = cur.execute("insert into appointment values(null,'"+pid+"','"+did+"','"+p_problem+"','waiting','waiting','"+p_address+"','waiting','waiting')")
    con.commit()
    if i > 0:
        context = {'data': 'Appointment Request Sent Successfully..!!'}
        return render(request, 'Patient/ViewDoctors.html', context)
    else:
        context = {'data': 'Appointment Booking Failed...!!'}
        return render(request, 'Patient/ViewDoctors.html', context)

def AppSchedule(request):
    p_id = request.session['p_id']
    pid=str(p_id)
    con=pymysql.connect(host="localhost",user="root",password="root",database="healthcare")
    cur=con.cursor()
    cur.execute("select * from admin ad, doctor d, appointment a, patient p, billing b where a.doctor_id=d.doctor_id and d.hsp_id=ad.hsp_id and a.patient_id=p.patient_id and p.patient_id='"+pid+"' and b.patient_id = p.patient_id and b.patient_id='"+pid+"'")
    data=cur.fetchall()
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Hospital Name</th><th>Hospital Address</th><th>Doctor Name</th><th>Speciality</th><th>Appointment Timing</th>" \
            "<th>Problem</th><th>Patient Name</th><th>Appointment Date & Time</th><th>Appointment</th><th>Pay Bill</th> </tr></thead>"
    k=0
    for i in data:
        k=k+1
        status= i[31]

        if status == 'waiting':
            strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td><font color='green'>"+str(i[14])+"</font></td>" \
                    "<td> <font color='green'>Appointment Scheduled</font></td><td><a href='PayBill?b_id="+str(i[27])+"&amount="+str(i[30])+"'><font color='red'>Pay Bill</font></a></td></tr></tbody>"
        else:
            strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td><font color='green'>"+str(i[14])+"</font></td>" \
                    "<td> <font color='green'>Appointment Scheduled</font></td><td><font color='green'> Bill Paid</font></td></tr></tbody>"
    context={'data': strdata}
    return render(request, 'Patient/ViewStatus.html', context)

def PayBill(request):
    bid=request.GET['b_id']
    am=request.GET['amount']
    request.session['bid']=bid
    request.session['am']=am

    return render(request, 'Patient/PayBill.html')
def PBillAction(request):
    bid=request.POST['b_id']
    con=pymysql.connect(host="localhost",user="root",password="root",database="healthcare")
    cur=con.cursor()
    cur.execute("update billing set payment_status='Paid' where billing_id='"+bid+"'")
    con.commit()
    p_id = request.session['p_id']
    pid=str(p_id)

    cur1=con.cursor()
    cur1.execute("select * from admin ad, doctor d, appointment a, patient p, billing b where a.doctor_id=d.doctor_id and d.hsp_id=ad.hsp_id and a.patient_id=p.patient_id and p.patient_id='"+pid+"' and b.patient_id = p.patient_id and b.patient_id='"+pid+"'")
    data=cur1.fetchall()
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Hospital Name</th><th>Hospital Address</th><th>Doctor Name</th><th>Speciality</th><th>Appointment Timing</th>" \
            "<th>Problem</th><th>Patient Name</th><th>Appointment Date & Time</th><th>Appointment</th><th>Pay Bill</th> </tr></thead>"
    k=0
    for i in data:
        k=k+1
        status = i[31]

        if status == 'waiting':
            strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td><font color='green'>"+str(i[14])+"</font></td>" \
                    "<td><font color='green'>Appointment Scheduled</font></td><td><a href='PayBill?b_id="+str(i[27])+"&amount="+str(i[30])+"'><font color='red'>Pay Bill</font></a></td></tr></tbody>"
        else:
            strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td><font color='green'>"+str(i[14])+"</font></td>" \
                    "<td> <font color='green'>Appointment Scheduled</font></td><td><font color='green'> Bill Paid</font></td></tr></tbody>"
    context={'data': strdata}
    return render(request, 'Patient/ViewStatus.html', context)

def viewreport(request):
    pid=request.session['p_id']
    p_id=str(pid)
    con=pymysql.connect(host="localhost",user="root",password="root",database="healthcare")
    cur=con.cursor()
    cur.execute("select * from admin ad, doctor d, appointment a, patient p where a.doctor_id=d.doctor_id  and d.hsp_id=ad.hsp_id and a.patient_id=p.patient_id and a.patient_id='"+p_id+"'")
    data=cur.fetchall()
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Hospital Name</th><th>Hospital Address</th>" \
            "<th>Docto Name</th><th>Speciality</th><th>Problem</th><th>Prescription</th><th>Report</th><th>Feedback</th></tr></thead>"
    k=0
    for i in data:
        k=k+1
        prescription= i[15]
        status= i[17]
        bstatus = i[18]

        strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td>" \
                "<td>"+str(i[6])+"</td><td>"+str(i[7])+"</td><td>"+str(i[20])+"</td><td>"+str(i[13])+"</td><td>"+str(i[15])+"</td><th><a href='/patient/helpline?hsp_id="+str(i[0])+"'><font color='red'>FeedBack</font></a></th></tr></tbody>"
    context={'data': strdata}
    return render(request, 'Patient/ViewReport.html', context)
def helpline(request):
    hsp_id=request.GET['hsp_id']
    request.session['hsp']=hsp_id
    return render(request, 'Patient/AddHelpLine.html')
def AddhelpAction(request):
    hspid = request.POST['hsp_id']
    p_name=request.POST['name']
    p_email = request.POST['email']
    p_mobile = request.POST['mobile']
    p_remark = request.POST['remark']



    con = pymysql.connect(host='localhost', user='root', password='root', database='healthcare')
    cur1 = con.cursor()
    i = cur1.execute("insert into helpline values(null,'"+hspid+"','"+p_name+"','"+p_email+"','"+p_mobile+"','"+p_remark+"')")
    con.commit()
    if i > 0:
        context = {'data': 'Feedback Submitted Successfully..!!'}
        return render(request, 'Patient/PatientHome.html', context)
    else:
        context = {'data': 'Feedback Adding Failed...!!'}
        return render(request, 'Patient/PatientHome.html', context)




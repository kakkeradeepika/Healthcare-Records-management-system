from django.shortcuts import render
import pymysql
# Create your views here.
def index(request):
    return render(request, 'Admin/index.html')

def login(request):
    return render(request, 'Admin/login.html')

def adminaction(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username == 'Admin' and password == 'Admin':
        return render(request, 'Admin/AdminHome.html')
    else:
        context = {'data': 'Login Failed'}
        return render(request, 'Admin/login.html', context)
def adminhome(request):
    return render(request, 'Admin/AdminHome.html')
def AddHsp(request):
    return render(request, 'Admin/AddHsp.html')
def AdHSPAction(request):
    hsp = request.POST['name']
    address = request.POST['address']
    mobile = request.POST['mobile']

    con = pymysql.connect(host='localhost', user='root', password='root', database='healthcare')
    cur = con.cursor()
    cur.execute("select * from admin where hospital_name='"+hsp+"'");
    a = cur.fetchone()
    if a is not None:
        context = {'data': 'Hospital  Already Added'}
        return render(request, 'Admin/AddHsp.html', context)
    else:
        cur1 = con.cursor()
        i = cur1.execute("insert into admin values(null,'"+hsp+"','"+address+"','"+mobile+"')")
        con.commit()
        if i > 0:
            context = {'data': 'Hospital Added Successfully..!!'}
            return render(request, 'Admin/AddHsp.html', context)
        else:
            context = {'data': 'Hospital Adding Failed...!!'}
            return render(request, 'Admin/AddHsp.html', context)

def AddDoctor(request):
    con = pymysql.connect(host="localhost",user="root",password="root",database="healthcare")
    cur = con.cursor()
    cur.execute("select * from admin")
    data=cur.fetchall()
    strdata="  <select class='form-control border-0 py-3 px-4' name='hsp'  style='height: 47px;' required=''> <option selected></option>"
    for i in data:
      strdata+= "<option value='"+str(i[0])+"'>"+str(i[1])+"</option>"
    strdata+= "</select>"
    context = {'data': strdata}
    return render(request, 'Admin/AddDoctor.html', context)

def AddDoctorAction(request):
    d_hsp_id = request.POST['hsp']
    d_name=request.POST['name']
    d_speciality = request.POST['speciality']
    d_timings = request.POST['timings']
    d_mobile = request.POST['mobile']

    con = pymysql.connect(host='localhost', user='root', password='root', database='healthcare')
    cur = con.cursor()
    cur.execute("select * from doctor where hsp_id='"+d_hsp_id+"' and name='"+d_name+"'and mobile='"+d_mobile+"'");
    a = cur.fetchone()
    if a is not None:
        context = {'msg': 'Doctor Already Added'}
        return render(request, 'Admin/AddDoctor.html', context)
    else:
        cur1 = con.cursor()
        i = cur1.execute("insert into doctor values(null,'"+d_hsp_id+"','"+d_name+"','"+d_speciality+"','"+d_timings+"','"+d_mobile+"')")
        con.commit()
        if i > 0:
            context = {'msg': 'Doctor Added Successfully..!!'}
            return render(request, 'Admin/AddDoctor.html', context)
        else:
            context = {'msg': 'Doctor Adding Failed...!!'}
            return render(request, 'Admin/AddDoctor.html', context)


def BillPatient(request):
    con=pymysql.connect(host="localhost",user="root",password="root",database="healthcare")
    cur=con.cursor()
    cur.execute("select * from admin ad, doctor d, appointment a, patient p where a.doctor_id=d.doctor_id and d.hsp_id=ad.hsp_id and a.patient_id=p.patient_id")
    data=cur.fetchall()
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Hospital Name</th><th>Hospital Address</th><th>Doctor Name</th><th>Speciality</th><th>Appointment Timing</th>" \
            "<th>Problem</th><th>Patient Name</th><th>Appointment Date & Time</th><th>Appointment</th><th>Generate Bill</th> </tr></thead>"
    k=0
    for i in data:
        k=k+1
        status= i[17]
        bstatus=i[18]
        bstatus=i[18]
        if status == 'waiting' and bstatus == 'waiting':
             strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td>"+str(i[14])+"</td><td><a href='ScheduleAppointment?a_id="+str(i[10])+"'><font color='red'>Schedule Now</font></a></td><td>Loading..</td></tr></tbody>"
        elif status == 'Scheduled' and bstatus == 'waiting':
            strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td><font color='green'>"+str(i[14])+"</font></td><td> <font color='green'>Appointment Scheduled</font></td><td><a href='generateBill?d_id="+str(i[4])+"&a_id="+str(i[10])+"&p_id="+str(i[11])+"'><font color='red'>Generate Bill</font></a></td></tr></tbody>"
        elif status == 'Scheduled' and bstatus == 'Generated':
            strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td><font color='green'>"+str(i[14])+"</font></td><td> <font color='green'>Appointment Scheduled</font></td><td><font color='greeen'>Bill Generated</font></td></tr></tbody>"

    context={'data': strdata}
    return render(request, 'Admin/ViewAppointments.html', context)

def ScheduleAppointment(request):
    aid=request.GET['a_id']
    request.session['aid']=aid
    return render(request,'Admin/AssignTime.html')
def AddDateTimeAction(request):
    a_id = request.POST['aid']
    datetime=request.POST['date']


    con = pymysql.connect(host='localhost', user='root', password='root', database='healthcare')
    cur1 = con.cursor()
    i = cur1.execute("update appointment set datetime='"+datetime+"',a_status='Scheduled' where id='"+a_id+"'")
    con.commit()
    if i > 0:
        con=pymysql.connect(host="localhost",user="root",password="root",database="healthcare")
    cur=con.cursor()
    cur.execute("select * from admin ad, doctor d, appointment a, patient p where a.doctor_id=d.doctor_id and d.hsp_id=ad.hsp_id and a.patient_id=p.patient_id")
    data=cur.fetchall()
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Hospital Name</th><th>Hospital Address</th><th>Doctor Name</th><th>Speciality</th><th>Appointment Timing</th>" \
            "<th>Problem</th><th>Patient Name</th><th>Appointment Date & Time</th><th>Appointment</th><th>Generate Bill</th> </tr></thead>"
    k=0
    for i in data:
        k=k+1
        status= i[17]
        bstatus=i[18]
        if status == 'waiting' and bstatus == 'waiting':
             strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td>"+str(i[14])+"</td><td><a href='ScheduleAppointment?a_id="+str(i[10])+"'><font color='red'>Schedule Now</font></a></td><td>Loading..</td></tr></tbody>"
        elif status == 'Scheduled' and bstatus == 'waiting':
            strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td><font color='green'>"+str(i[14])+"</font></td><td> <font color='green'>Appointment Scheduled</font></td><td><a href='generateBill?d_id="+str(i[4])+"&a_id="+str(i[10])+"&p_id="+str(i[11])+"')><font color='red'>Generate Bill</font></a></td></tr></tbody>"
        elif status == 'Scheduled' and bstatus == 'Generated':
            strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td><font color='green'>"+str(i[14])+"</font></td><td> <font color='green'>Appointment Scheduled</font></td><td><font color='greeen'>Bill Generated</font></td></tr></tbody>"

        context={'data': strdata, 'msg':'Appointment Scheduled Successfully...!!'}
        return render(request, 'Admin/ViewAppointments.html', context)
    else:
        context = {'msg': 'Scheduling Failed...!!'}
        return render(request, 'Admin/ViewAppointments.html', context)

def generateBill(request):
    did = request.GET['d_id']
    aid = request.GET['a_id']
    pid = request.GET['p_id']

    request.session['d_id']=did
    request.session['a_id']=aid
    request.session['p_id']=pid

    return render(request,'Admin/GenerateBill.html')


def AddBillAction(request):
    d_id=request.POST['did']
    charge=request.POST['charges']
    pid = request.session['p_id']
    aid = request.session['a_id']

    con = pymysql.connect(host='localhost', user='root', password='root', database='healthcare')
    cur = con.cursor()
    i = cur.execute("update appointment set b_status='Generated' where id='"+aid+"'")
    i = cur.execute("insert into billing values(null,'"+pid+"','"+d_id+"','"+charge+"','waiting')")
    con.commit()
    if i > 0:
        cur.execute("select * from admin ad, doctor d, appointment a, patient p where a.doctor_id=d.doctor_id and d.hsp_id=ad.hsp_id and a.patient_id=p.patient_id")
        data=cur.fetchall()
        strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Hospital Name</th><th>Hospital Address</th><th>Doctor Name</th><th>Speciality</th><th>Appointment Timing</th>" \
            "<th>Problem</th><th>Patient Name</th><th>Appointment Date & Time</th><th>Appointment</th><th>Generate Bill</th> </tr></thead>"
        k=0
        for i in data:
            k=k+1
            status= i[17]
            bstatus=i[18]
            if status == 'waiting' and bstatus == 'waiting':
                strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td>"+str(i[14])+"</td><td><a href='ScheduleAppointment?a_id="+str(i[10])+"'><font color='red'>Schedule Now</font></a></td><td>Loading..</td></tr></tbody>"
            elif status == 'Scheduled' and bstatus == 'waiting':
                strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td><font color='green'>"+str(i[14])+"</font></td><td> <font color='green'>Appointment Scheduled</font></td><td><a href='generateBill?d_id="+str(i[4])+"&a_id="+str(i[10])+"&p_id="+str(i[11])+"')><font color='red'>Generate Bill</font></a></td></tr></tbody>"
            elif status == 'Scheduled' and bstatus == 'Generated':
                strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td><font color='green'>"+str(i[14])+"</font></td><td> <font color='green'>Appointment Scheduled</font></td><td><font color='greeen'>Bill Generated</font></td></tr></tbody>"

        context = {'data':strdata,'msg': 'Bill Generated Successfully..!!'}
        return render(request, 'Admin/ViewAppointments.html', context)
    else:
        context = {'data': 'Bill Generating Failed...!!'}
        return render(request, 'Admin/ViewAppointments.html', context)

def BillPatients(request):


    con = pymysql.connect(host='localhost', user='root', password='root', database='healthcare')
    cur = con.cursor()
    cur.execute("select * from admin ad, doctor d, appointment a, patient p,billing b where a.doctor_id=d.doctor_id and d.hsp_id=ad.hsp_id and a.patient_id=p.patient_id and d.doctor_id=b.doctor_id")
    data=cur.fetchall()
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Hospital Name</th><th>Hospital Address</th><th>Doctor Name</th><th>Speciality</th><th>Appointment Timing</th>" \
            "<th>Problem</th><th>Patient Name</th><th>Appointment Date & Time</th><th>Appointment</th><th>Bill Status</th> </tr></thead>"
    k=0
    for i in data:
        k=k+1
        status= i[17]
        bstatus=i[18]

        strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td><font color='green'>"+str(i[14])+"</font></td><td> <font color='green'>Appointment Scheduled</font></td><td><font color='green'>"+str(i[31])+"</font></td></tr></tbody>"

        context = {'data':strdata}
        return render(request, 'Admin/ViewBillPatientsStatus.html', context)




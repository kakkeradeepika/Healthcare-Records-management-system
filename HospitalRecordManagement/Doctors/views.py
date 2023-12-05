from django.shortcuts import render
import pymysql
# Create your views here.
def login(request):
    return render(request, 'Doctors/Login.html')
def LogAction(request):
    d_name = request.POST['name']
    d_mobile = request.POST['mobile']

    con = pymysql.connect(host='localhost', user='root', password='root', database='healthcare')
    cur = con.cursor()
    cur.execute("select * from doctor where  name='"+d_name+"'and mobile='"+d_mobile+"'");
    a = cur.fetchone()
    if a is not None:
        request.session['d_id']=a[0]
        request.session['hsp_id']=a[1]
        request.session['d_name']=a[2]
        request.session['d_special']=a[3]
        return render(request, 'Doctors/DoctorHome.html')
    else:
        context = {'data': 'Login Failed..!!'}
        return render(request, 'Doctors/Login.html', context)
def home(request):
    return render(request, 'Doctors/DoctorHome.html')
def dviewappoint(request):
    did=request.session['d_id']
    d_id=str(did)
    con=pymysql.connect(host="localhost",user="root",password="root",database="healthcare")
    cur=con.cursor()
    cur.execute("select * from admin ad, doctor d, appointment a, patient p, billing b where a.doctor_id=d.doctor_id and d.hsp_id=ad.hsp_id and a.patient_id=p.patient_id and b.doctor_id=d.doctor_id and d.doctor_id='"+d_id+"'")
    data=cur.fetchall()
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Hospital Name</th><th>Hospital Address</th><th>Doctor Name</th><th>Speciality</th><th>Appointment Timing</th>" \
            "<th>Problem</th><th>Patient Name</th><th>Appointment Date & Time</th><th>Appointment</th><th>Generate Bill</th> <th>Generate Report</th></tr></thead>"
    k=0
    for i in data:
        k=k+1
        prescription= i[15]
        status= i[17]
        bstatus = i[18]
        pstatus = i[31]

        if status == 'Scheduled' and bstatus == 'Generated' and pstatus == 'waiting':
            strdata+= "<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td><font color='green'>"+str(i[14])+"</font></td><td> <font color='green'>Appointment Scheduled</font></td><td><font color='green'>Bill Generated</font></td><td><font color='red'>Not Paid Bill</font></td></tr></tbody>"
        elif prescription == 'waiting' and status == 'Scheduled' and bstatus == 'Generated' and pstatus == 'Paid':
            strdata+= "<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td><font color='green'>"+str(i[14])+"</font></td><td> <font color='green'>Appointment Scheduled</font></td><td><font color='green'>Bill Generated</font></td><td><a href='GenerateReport?a_id="+str(i[10])+"&problem="+str(i[13])+"'><font color='red'>Generate Report</font></a></td></tr></tbody>"
        else:
            strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[6])+"</td>" \
                "<td>"+str(i[7])+"</td><td>"+str(i[8])+"</td><td>"+str(i[13])+"</td><td>"+str(i[20])+"</td><td><font color='green'>"+str(i[14])+"</font></td><td> <font color='green'>Appointment Scheduled</font></td><td><font color='green'>Bill Generated</font></td><td><font color='green'>Report Generated</font></td></tr></tbody>"
    context={'data': strdata}
    return render(request, 'Doctors/DViewAppointments.html', context)


def GenerateReport(request):

    aid=request.GET['a_id']
    probl=request.GET['problem']
    request.session['aid']=aid
    request.session['problem']=probl

    return render(request, 'Doctors/GenerateReport.html')


def AddReportAction(request):
    aid=request.POST['aid']
    report=request.POST['report']

    con = pymysql.connect(host='localhost', user='root', password='root', database='healthcare')
    cur = con.cursor()
    i = cur.execute("update appointment set prescription='"+report+"' where id='"+aid+"'")
    con.commit()
    context={'msg': 'Report Generated Successfully'}
    return render(request, 'Doctors/DoctorHome.html', context)


def dviewreport(request):
    did=request.session['d_id']
    d_id=str(did)
    con=pymysql.connect(host="localhost",user="root",password="root",database="healthcare")
    cur=con.cursor()
    cur.execute("select * from admin ad, doctor d, appointment a, patient p where a.doctor_id=d.doctor_id and d.doctor_id='"+d_id+"' and d.hsp_id=ad.hsp_id and a.patient_id=p.patient_id")
    data=cur.fetchall()
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Hospital Name</th><th>Hospital Address</th>" \
            "<th>Patient Name</th><th>Problem</th><th>Prescription</th><th>Report Status</th></tr></thead>"
    k=0
    for i in data:
        k=k+1
        prescription= i[15]
        status= i[17]
        bstatus = i[18]

        strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td>" \
                "<td>"+str(i[20])+"</td><td>"+str(i[13])+"</td><td>"+str(i[15])+"</td><td><font color='green'>Susccess</font></td></tr></tbody>"
    context={'data': strdata}
    return render(request, 'Doctors/DViewReports.html', context)


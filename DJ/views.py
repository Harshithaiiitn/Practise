from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from . models import *
from django.db import connection
from . forms import *
from . tables import *
from django_tables2 import RequestConfig
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.contrib.auth import authenticate, login as user_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logout_required
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None
import json
# Create your views here.


def home(request):
    return render(request,'login.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pwd']
        user = authenticate(username=username, password=password)
        if user is not None:
           user_login(request, user)
           return redirect('index') 
        else:
           return redirect('home') 
    else:
        return render(request, 'login.html')

def logout(request):
    logout(request)
    return render(request,'login.html')
  
@login_required
def homepage(request):
    return render(request,'Homepage.html/')


@login_required
def index(request):
   item  = Regulations.objects.all()
   return render(request, 'Reg.html/', {'items':item})

@login_required
def countries_view(request):
   heading_message = 'Regulations Management'
   balist=request.session['balist']
   if request.method == 'POST':
       form = RegulationForm(request.POST or None)
       if form.is_valid():
           regulations = form.cleaned_data.get('Regulations')
           request.session['reg']=regulations
           user=request.user
           if regulations:
                 for ba in balist:
                    for regulation in regulations:
                        count=BAReg.objects.filter(regulation=regulation,businessdefinition_a=ba,user=user).count()
                        if(count<1):
                            BAReg(regulation=regulation, businessdefinition_a = ba, user=user).save()
                       #BAReg(regulation=regulation, businessdefinition_a = ba, user=user).save()
                 return redirect('secondpage')
   else:
           form = RegulationForm(request.GET or None)
   return render(request,'Reg.html/', { 'form' : form,'heading' : heading_message })

@login_required
def bagroupall(request):
   heading_message = 'Group Regulations Management'
   balist=request.session['balist']
   if request.method == 'POST':
       form = RegulationForm(request.POST or None)
       if form.is_valid():
           regulations = form.cleaned_data.get('Regulations')
           request.session['reg']=regulations
           user=request.user
           if regulations:
                #for ba in balist:
                   for regulation in regulations:
                       BAReg(regulation=regulation, businessdefinition_a = "Group ("+str(len(balist))+")", user=user).save()

           return redirect('secondpage')
   else:
           form = RegulationForm(request.GET or None)
   return render(request,'Reg.html/', { 'form' : form,'heading' : heading_message })

@login_required
def selectbusiness(request):
    heading_message = 'Business Management'
    if request.method == 'POST':
       formset=CustomBusinessFormSet(request.POST or None)
       form=BusinessForm(request.POST or None)
       if  form.is_valid():
            businessactivitites=form.cleaned_data.get('BusinessActivitites')
            group=request.POST.get('groupall')
            request.session['balist']=businessactivitites
            request.session['group']=group
            if group == 'yes':
               return redirect('bagroupall')
            else:
               return redirect('countries_view')
       if  formset.is_valid():
            for form in formset:
                b_q=form.cleaned_data.get('businessdefinition_q')
                b_a=form.cleaned_data.get('businessdefinition_a')
                b_j=form.cleaned_data.get('jurisdiction')
                request.session['ba']=b_a
                BusinessActivity(businessdefinition_q = b_q, businessdefinition_a = b_a, jurisdiction = b_j).save()
            return redirect('countries_view')
    else:
           formset = CustomBusinessFormSet(request.GET or None)
           form=BusinessForm(request.GET or None)
           return render(request,'BA.html/', { 'form' : form,
           'formset' : formset,
           'heading' : heading_message
           })


def convert(parent,string):
        res ={
                'name': string,
                'parent':parent,
                'children':[]    
            }
        return res



@login_required
def secondpage(request):
        current_user=request.user
        count =BAReg.objects.filter(user=current_user).count()
        done_count=BAReg.objects.filter(user=current_user, status='done').count()
        if count == done_count:
           button_enable = True
        else:
           button_enable = False
        table = PersonTable(BAReg.objects.filter(user=current_user))
        RequestConfig(request).configure(table)
        context = {'table': table, 'flag' : button_enable}
        return render(request,'Process_1.html/',context)

@login_required
def groupallsecondpage(request):
        current_user=request.user
        # count =Group.objects.filter(user=current_user).count()
        # done_count=Group.objects.filter(user=current_user).count()
        # if count == done_count:
        #    button_enable = True
        # else:
        #    button_enable = False
        # table = PersonTable1(Group.objects.filter(user=current_user))
        # RequestConfig(request).configure(table)
         #context = {'table': table}
        return render(request,'Process_1.html/',context)
@login_required
def thirdpage(request):
        current_user=request.user
        count =ProcessReg.objects.filter(user=current_user).count()
        done_count=ProcessReg.objects.filter(user=current_user, status='done').count()
        if count == done_count:
           button_enable = True
        else:
           button_enable = False
        table = ControlTable(ProcessReg.objects.filter(user=current_user))  
        RequestConfig(request).configure(table)
        context = {'table': table, 'flag' : button_enable}
        return render(request,'Process_2.html/',context)

@login_required
def fourthpage(request):
        current_user=request.user
        count =ControlReg.objects.filter(user=current_user).count()
        done_count=ControlReg.objects.filter(user=current_user, status='done').count()
        if count == done_count:
           button_enable = True
        else:
           button_enable = False
        table = RiskTable(ControlReg.objects.filter(user=current_user))  
        RequestConfig(request).configure(table)
        context = {'table': table, 'flag' : button_enable}
        return render(request,'fourthpage.html/',context)

@login_required
def edit_item(request, pk):
    item = get_object_or_404(BAReg, id=pk) 
    heading_message = 'Process Management'
    if request.method == 'POST':
        formset = ProcessFormSet(request.POST)
        if formset.is_valid():
            BAReg.objects.filter(pk=pk).update(status='done')
            user=request.user
            title_list=[]
            for form in formset:
                 f = form.cleaned_data
                 title= f.get('title')
                 title_list.append(title)
                 description = f.get('description')
                 ProcessReg(regulation=item.regulation, businessdefinition_a = item.businessdefinition_a, businessdefinition_q = item.businessdefinition_q, jurisdiction=item.jurisdiction, 
                 process=title, description=description, user=user).save()
                 request.session['title']=title_list
            return redirect('secondpage')
    else:
        formset = ProcessFormSet(request.GET or None)
    return render(request, 'Process_2.html', {
        'formset': formset,
        'heading': heading_message,
    })
        
@login_required  
def select_control(request, pk):
    item = get_object_or_404(ProcessReg, id=pk)
    heading_message = 'Control Management'
    if request.method == 'POST':
        formset = ControlFormSet(request.POST)
        if formset.is_valid():
            ProcessReg.objects.filter(pk=pk).update(status='done')
            user=request.user
            for form in formset:
                 f = form.cleaned_data
                 control= f.get('control')
                 description = f.get('description')
                 content = f.get('content')
                 ControlReg(regulation=item.regulation, businessdefinition_a = item.businessdefinition_a, businessdefinition_q = item.businessdefinition_q, jurisdiction=item.jurisdiction, 
                 process=item.process, description=item.description, controlarea=control, controldescription=description, controlobjective=content, user=user).save()
            # print(title_list)
            return redirect('selectcontrol')
    else:
        formset = ControlFormSet(request.GET or None)

    return render(request, 'control_2.html', {
        'formset': formset,
        'heading': heading_message,
    })
@login_required
def selectcontrol(request):
        current_user=request.user
        count =ProcessReg.objects.filter(user=current_user).count()
        done_count=ProcessReg.objects.filter(user=current_user, status='done').count()
        if count == done_count:
           button_enable = True
        else:
           button_enable = False
        table = ControlTable(ProcessReg.objects.filter(user=current_user))  
        RequestConfig(request).configure(table)
        context = {'table': table, 'flag' : button_enable}
        return render(request,'control_1.html/',context)

@login_required
def selectrisk(request):
        current_user=request.user
        count =ControlReg.objects.filter(user=current_user).count()
        done_count=ControlReg.objects.filter(user=current_user, status='done').count()
        if count == done_count:
           button_enable = True
        else:
           button_enable = False
        table = RiskTable(ControlReg.objects.filter(user=current_user))  
        RequestConfig(request).configure(table)
        context = {'table': table, 'flag' : button_enable}
        return render(request,'Risk_1.html/',context)

@login_required  
def select_risk(request, pk):
    item = get_object_or_404(ControlReg, id=pk)
    heading_message = 'Risk Management'
    if request.method == 'POST':
        formset = RiskFormSet(request.POST)
        if formset.is_valid():
            ControlReg.objects.filter(pk=pk).update(status='done')
            user=request.user
            for form in formset:
                f = form.cleaned_data
                risk= f.get('risk')
                comment = f.get('comment')
                RiskReg(regulation=item.regulation, businessdefinition_a = item.businessdefinition_a, businessdefinition_q = item.businessdefinition_q, jurisdiction=item.jurisdiction, 
                process=item.process, description=item.description, controlarea=item.controlarea, controldescription=item.controldescription, 
                controlobjective=item.controlobjective, risk=risk, comment=comment, user=user).save()
            return redirect('selectrisk')
    else:
        formset = RiskFormSet(request.GET or None)

    return render(request, 'Risk_2.html', {
        'formset': formset,
        'heading': heading_message,
    })

@login_required
def showfinalmapping(request):
    current_user=request.user
    count =RiskReg.objects.filter(user=current_user).count()
    done_count=RiskReg.objects.filter(user=current_user, status='done').count()
    if count == done_count:
       button_enable = True
    else:
       button_enable = False
    table = FinalTable(RiskReg.objects.filter(user=current_user)) 
    RequestConfig(request).configure(table)
    context = {'table': table, 'flag' : button_enable}
    return render(request,'Risk_3.html/',context)

@login_required
def edit_regulation(request, pk):
    heading_message='Edit Regulation Management'
    if request.method == 'POST':
       form = RegulationForm(request.POST or None,prefix="form1")
       if form.is_valid():
           regulations = form.cleaned_data.get('Regulations')
           if regulations:
               for regulation in regulations:
                   BAReg.objects.filter(id=pk).update(regulation=regulation, edit_status='done')
           return redirect('secondpage')
    else:
           form = RegulationForm(prefix="form1")
    return render(request,'Edit_Regulation.html/', { 'form' : form,
           'heading' : heading_message
           })

@login_required
def edit_process(request, pk):
    heading_message = 'Edit Process Management'
    if request.method == 'POST':
        formset = ProcessFormSet(request.POST)        
        if formset.is_valid():
            for form in formset: 
                title=form.cleaned_data.get('title')
                description=form.cleaned_data.get('description')
                ProcessReg.objects.filter(id=pk).update(process=title, description=description, edit_status='done')
                return redirect('selectcontrol')
    else:
            
            formset = ProcessFormSet(request.GET or None)
    return render(request,'Edit_Process.html/', {'formset':formset,
    'heading': heading_message
    })

@login_required
def edit_control(request,pk):
    heading_message = 'Edit Control Management'
    if request.method == 'POST':
        formset = ControlFormSet(request.POST)        
        if formset.is_valid():
            for form in formset:
                control=form.cleaned_data.get('control')
                description=form.cleaned_data.get('description')
                content=form.cleaned_data.get('content')
                ControlReg.objects.filter(id=pk).update(controlarea=control, controlobjective=description,controldescription=content, edit_status='done')
                return redirect('selectrisk')
    else:
            formset = ControlFormSet(request.GET or None)
            return render(request,'Edit_Control.html/', {'formset':formset,
            'heading' : heading_message
            })

@login_required
def edit_risk(request,pk):
    heading_message='Edit Risk Management'
    if request.method == 'POST':
        formset = RiskFormSet(request.POST)        
        if formset.is_valid():
           for form in formset:
               risk=form.cleaned_data.get('risk')
               comment=form.cleaned_data.get('comment')
               RiskReg.objects.filter(id=pk).update(risk=risk, comment=comment, edit_status='done')
               return redirect('showfinalmapping')
    else:
            formset = RiskFormSet(request.GET or None)
            return render(request,'Edit_Risk.html/', {'formset':formset,
            'heading' : heading_message
            })

@login_required
def viewfinalmapping(request):
    ba = request.session.get('ba')
    current_user=request.user
    balist=request.session['balist']
    group=request.session['group']
    if group == 'yes':
       set=RiskReg.objects.all()
       flag=Maptable.objects.count()

       if(flag==0):
           for i in set:
               for ba in balist:  
                    RiskReg(regulation=i.regulation,businessdefinition_a=ba,process=i.process,controlarea=i.controlarea,risk=i.risk, user=request.user).save()
                    ControlReg(regulation=i.regulation,businessdefinition_a=ba,process=i.process,controlarea=i.controlarea, user=request.user).save()
                    ProcessReg(regulation=i.regulation,businessdefinition_a=ba,process=i.process, user=request.user).save()
                    BAReg(regulation=i.regulation,businessdefinition_a=ba,user=request.user).save()  
                    Maptable(regulation=i.regulation,businessdefinition_a=ba,process=i.process,controlarea=i.controlarea,risk=i.risk, user=request.user).save()
           table = FinalviewTable(Maptable.objects.filter(user=current_user)) 
           RequestConfig(request).configure(table)
           context = {'table': table}
           return render(request,'finalview.html/',context)
       else:
            for i in set:
                for ba in balist:
                    flag1=Maptable.objects.filter(regulation=i.regulation,businessdefinition_a=ba,process=i.process,controlarea=i.controlarea,risk=i.risk, user=request.user).count()
                    if(flag1<1):
                        RiskReg(regulation=i.regulation,businessdefinition_a=ba,process=i.process,controlarea=i.controlarea,risk=i.risk, user=request.user).save()
                        ControlReg(regulation=i.regulation,businessdefinition_a=ba,process=i.process,controlarea=i.controlarea, user=request.user).save()
                        ProcessReg(regulation=i.regulation,businessdefinition_a=ba,process=i.process, user=request.user).save()
                        BAReg(regulation=i.regulation,businessdefinition_a=ba,user=request.user).save()  
                        Maptable(regulation=i.regulation,businessdefinition_a=ba,process=i.process,controlarea=i.controlarea,risk=i.risk, user=request.user).save()
            table = FinalviewTable(Maptable.objects.filter(user=current_user)) 
            RequestConfig(request).configure(table)
            context = {'table': table}
            return render(request,'finalview.html/',context)            
                        


    else:
        table = FinalviewTable(Maptable.objects.filter(user=current_user)) 
        RequestConfig(request).configure(table)
        context = {'table': table}
    return render(request,'finalview.html/',context)

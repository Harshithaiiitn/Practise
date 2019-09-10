import django_tables2 as tables
from . models import *
from django_tables2.utils import A 
# from .views import edit_item
from django.urls import reverse_lazy


class CustomTemplateColumn(tables.TemplateColumn):
   def render(self, record, table, value, bound_column, **kwargs):
        if record.status == "done":
            return 'DONE'
        
        return super(CustomTemplateColumn, self).render(record, table, value, bound_column, **kwargs)

class CustomTemplateColumnEdit(tables.TemplateColumn):
   def render(self, record, table, value, bound_column, **kwargs):
        if record.edit_status == "done":
            return 'DONE'
        
        return super(CustomTemplateColumnEdit, self).render(record, table, value, bound_column, **kwargs)




class PersonTable(tables.Table):
    T1 = '<a href="edit/businessactivity/{{record.id}}/">EDIT</a>'
    T2 = '<a href="edit/{{ record.id }}">ADD</a>'
    Edit_Regulation = CustomTemplateColumnEdit(T1)
    Process   = CustomTemplateColumn(T2)
    class Meta:
        model = BAReg
        fields =['businessdefinition_a', 'regulation']
        template_name = 'django_tables2/semantic.html'

class PersonTable1(tables.Table):
            T1 = '<a href="edit/businessactivity/{{record.id}}/">EDIT</a>'
            T2 = '<a href="edit/{{ record.id }}">ADD</a>'
            Edit_Regulation = CustomTemplateColumnEdit(T1)
            Process   = CustomTemplateColumn(T2)
            class Meta:
                model = BAReg
                fields =['businessdefinition_a', 'regulation']
                template_name = 'django_tables2/semantic.html'

class ControlTable(tables.Table):
    T1 = '<a href="edit/process/{{record.id}}/">EDIT</a>'
    T2 = '<a href="/add_control/{{ record.id }}">ADD</a>'
    Edit_Process = CustomTemplateColumnEdit(T1)
    Control   = CustomTemplateColumn(T2)
    class Meta:
        model = ProcessReg
        fields =['businessdefinition_a','regulation', 'process']
        template_name = 'django_tables2/semantic.html'


class RiskTable(tables.Table):
    T1 = '<a href="edit/control/{{record.id}}/">EDIT</a>'
    T2 = '<a href="/add_risk/{{ record.id }}">ADD</a>'
    Edit_Control = CustomTemplateColumnEdit(T1)
    Risk   = CustomTemplateColumn(T2)
    class Meta:
        model = ControlReg
        fields =['businessdefinition_a','regulation', 'process', 'controlarea']
        template_name = 'django_tables2/semantic.html'

class FinalTable(tables.Table):
    T1 = '<a href="edit/risk/{{record.id}}/">EDIT</a>'
    Edit_Risk = CustomTemplateColumnEdit(T1)
    class Meta:
           model = RiskReg
           fields = ['businessdefinition_a', 'regulation', 'process', 'controlarea', 'risk']
           template_name = 'django_tables2/semantic.html'

class FinalviewTable(tables.Table):
    class Meta:
           model = Maptable
           fields = [ 'businessdefinition_a', 'regulation', 'process', 'controlarea', 'risk']
           template_name = 'django_tables2/semantic.html'
    
from django import forms
from archive.models import *


from users import config

class ArchiveForm(forms.ModelForm):

    class Meta:
        model = Archive
        fields = ['dept', 'sem', 'subject', 'exm_type', 'desc', 'attachment']
        labels = {
            "dept": "Department Name",
            "sem": "Semester",
            "subject": "Subject",
            "exm_type": "Exam Type",
            "desc": "Description",
            "attachment": "Attachment"
        }

    def __init__(self, *args, **kwargs):
        super(ArchiveForm, self).__init__(*args, **kwargs)
        self.fields['dept'].queryset = Department.objects.filter(id=config.dept_dept_id)
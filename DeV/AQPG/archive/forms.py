from django import forms
from archive.models import *

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
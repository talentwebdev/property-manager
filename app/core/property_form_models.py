class Manager(models.Model):
    
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20) 
    ...
    
    
class FormTemplate(models.Model):
    
    manager = models.ForeignKey(Manager, related_name="form_templates", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Question(models.Model):
    
    QUESTION_TYPE_TEXT = 0
    QUESTION_TYPE_PHOTO = 1
    QUESTION_TYPE_BOOL = 2
    
    QUESTION_TYPE_CHOICES = (
        (QUESTION_TYPE_TEXT, "Text question"),
        (QUESTION_TYPE_PHOTO, "Photo question"),
        (QUESTION_TYPE_BOOL, "Bool question"),
    )
    
    form = models.ForeignKey(FormTemplate, related_name="questions", on_delete=models.CASCADE)
    question = models.TextField()
    question_type = models.IntegerField(default=QUESTION_TYPE_TEXT, choices=QUESTION_TYPE_CHOICES)
    
    
class Property(models.Model):
    ...
    
    forms = models.ManToManyField(FormTemplate, related_name="properties")
    forms_ids = models.TextField(null=True, blank=True)
    
    forms_tracker = FieldTracker(fields=['forms'])
    
    def save(self):
        
        if self.forms_tracker.changed():
            # update forms_id 
            self.forms_ids = [
                str(form.pk)
                for form in self.forms
            ].join(",")
            
            # check if forms_id is equal
            is_duplicated = Property.objects.filter(forms_id=self.forms_ids).exists()
            if is_duplicated:
                raise FormsDuplicateError
            
        ...
        

class Answer(models.Model):
    
    
    property = models.ForeignKey(Property, related_name="answers", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="questions", on_delete=models.CASCADE)
    
    
    answer = models.JSONField()
    
    class Meta:
        unique_together = ('property', 'question', )
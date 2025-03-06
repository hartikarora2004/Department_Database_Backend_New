# models.py
from django.db import models
from basemodel.models import BaseModel
from usercustom.models import CustomUser
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
# Create your models here.

class Publication(BaseModel):
    class PublicationType(models.TextChoices):
        JOURNAL = 'J', 'Journal'
        CONFERENCE = 'C', 'Conference'
        BOOK = 'B', 'Book'
        BOOK_CHAPTER = 'BC', 'Book Chapter'
        PATENT = 'P', 'Patent'
        OTHER = 'O', 'Other'
    
    class PublicationStatus(models.TextChoices):
        PUBLISHED = 'P', 'Published'
        SUBMITTED = 'S', 'Submitted'
        ACCEPTED = 'A', 'Accepted'
        REJECTED = 'R', 'Rejected'
        OTHER = 'O', 'Other'
    
    class IdentifierType(models.TextChoices):
        DOI = 'DOI', 'DOI'
        ISBN = 'ISBN', 'ISBN'
        ISSN = 'ISSN', 'ISSN'
        CORPUS_ID = 'CORPUS_ID', 'CORPUS_ID'
        OTHER = 'O', 'Other'
    
    class FieldTags(models.TextChoices):
        COMPUTER_SCIENCE = 'CS', 'Computer Science'
        ARTIFICIAL_INTELLIGENCE = 'AI', 'Artificial Intelligence'
        SOFTWARE_ENGINEERING = 'SE', 'Software Engineering'
        NETWORKING = 'NET', 'Networking'

        ELECTRICAL_ENGINEERING = 'EE', 'Electrical Engineering'
        MECHANICAL_ENGINEERING = 'ME', 'Mechanical Engineering'
        CIVIL_ENGINEERING = 'CE', 'Civil Engineering'
        CHEMICAL_ENGINEERING = 'CHE', 'Chemical Engineering'
        MATERIALS_ENGINEERING = 'MATE', 'Materials Engineering'
        BIOMEDICAL_ENGINEERING = 'BME', 'Biomedical Engineering'
        AEROSPACE_ENGINEERING = 'AE', 'Aerospace Engineering'
        OTHER = 'O', 'Other'
    
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    publication_type = models.CharField(max_length=2, choices=PublicationType.choices, default=PublicationType.OTHER)
    publication_status = models.CharField(max_length=2, choices=PublicationStatus.choices, default=PublicationStatus.OTHER)
    identifier_type = models.CharField(max_length=10, choices=IdentifierType.choices, default=IdentifierType.OTHER)
    identifier = models.CharField(max_length=50, null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    authors = models.ManyToManyField(CustomUser, related_name='%(class)s_authors')
    authors_text = models.TextField(null=True, blank=True)
    accepted_date = models.DateField(null=True, blank=True)
    # select multiple tags from a text choices
    field_tags = ArrayField(models.CharField(max_length=4, choices=FieldTags.choices, default=FieldTags.OTHER), null=True, blank=True)
    # models.CharField(max_length=4, choices=FieldTags.choices, default=FieldTags.OTHER)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [models.CheckConstraint(check=~(models.Q(is_draft=True) & models.Q(is_approved=True)), name='publication draft cannot be approved'),
                       models.UniqueConstraint(fields=['draft_id', 'is_approved', 'is_deleted'], condition=models.Q(is_approved=False) & models.Q(is_deleted = False), name='Only one publication draft can be made for each object'),
                       models.UniqueConstraint(fields=['identifier', 'is_approved'], condition= models.Q(is_deleted = False), name="publication_identifier_is_unique"),
                    ]
    
    def get_ieee(self):
        return f''

class PublicationEditHistory(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='edit_history')
    editor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name= self.editor.first_name + ' ' + self.editor.last_name
        edited_date = self.edited_at.date()  # Extract only the date part
        return f"{self.publication.title} edited by {name} on {edited_date}"
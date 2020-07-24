#Entry model - including embedded documents

from djongo import models
import uuid
from django import forms



class Blastrps(models.Model):
    '''
    RPS-BLAST embedded document from rps_results.csv
    '''

    query_length = models.IntegerField()
    cdd_id = models.CharField(max_length=255)
    hit_id = models.CharField(max_length=255)
    evalue = models.FloatField()
    startQ = models.IntegerField()
    endQ = models.IntegerField()
    frame = models.IntegerField()
    description = models.TextField()
    superkingdom = models.CharField(max_length=255)
    no_rank = models.CharField(max_length=255)
    family = models.CharField(max_length=500)
    genus = models.CharField(max_length=500)



class Blastx(models.Model):
    '''
    BLASTX embedded document from blastx_results.csv
    '''

    taxonomy = models.CharField(max_length=500)
    nb_reads = models.IntegerField()
    query_length = models.IntegerField()
    accession = models.CharField(max_length=255)
    description = models.TextField()
    organism = models.CharField(max_length=255)
    percent_identity = models.FloatField()
    nb_hsps = models.IntegerField()
    query_overlap = models.IntegerField()
    hit_overlap = models.IntegerField()
    evalue = models.FloatField()
    score = models.FloatField()
    tax_id = models.IntegerField()
    algo = models.CharField(max_length=100)
    sequence = models.TextField()


class SRAMetadata(models.Model):
    '''
    Metadata embedded document from SRA_metadata.csv
    '''

    ReleaseDate = models.DateTimeField() 
    LoadDate = models.CharField(max_length=250)
    spots = models.IntegerField()
    bases = models.IntegerField() 
    spots_with_mates = models.IntegerField()
    avgLength = models.IntegerField()
    size_MB = models.IntegerField()
    download_path = models.CharField(max_length=500)
    Experiment = models.CharField(max_length=250)
    LibraryName = models.CharField(max_length=250)
    LibraryStrategy = models.CharField(max_length=250)
    LibrarySelection = models.CharField(max_length=250)
    LibrarySource = models.CharField(max_length=250)
    LibraryLayout = models.CharField(max_length=250)
    InsertSize = models.IntegerField()
    InsertDev = models.IntegerField()
    Platform = models.CharField(max_length=250)
    Model = models.CharField(max_length=250)
    SRAStudy = models.CharField(max_length=250)
    BioProject = models.CharField(max_length=250)
    ProjectID= models.CharField(max_length=250) 
    Sample = models.CharField(max_length=250)
    BioSample = models.CharField(max_length=250)
    SampleType = models.CharField(max_length=250)
    TaxID = models.CharField(max_length=250) 
    ScientificName = models.CharField(max_length=250)
    SampleName = models.CharField(max_length=250)
    Tumor = models.CharField(max_length=250)
    CenterName = models.CharField(max_length=250)
    Submission = models.CharField(max_length=250)
    Consent = models.CharField(max_length=250)
    RunHash = models.CharField(max_length=250) 
    ReadHash = models.CharField(max_length=250) 
    Cultivar= models.CharField(max_length=250)


class INVMetadata(models.Model):
    ''' 
    InViCeb embedded document from INV_metadata
    '''

    project = models.CharField(max_length=250)
    grapevine_cultivar = models.CharField(max_length=250)
    rootstock = models.CharField(max_length=250)
    plantation_year = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    substrate = models.CharField(max_length=250)
    extraction_method = models.CharField(max_length=250 )
    organ = models.CharField(max_length=250 )
    mid_sequence = models.CharField(max_length=250)
    mid_id = models.CharField(max_length=250)
    run_name = models.CharField(max_length=250)
    technology = models.CharField(max_length=250)
    run_id = models.CharField(max_length=250)
    date = models.DateTimeField()
    seq_location = models.CharField(max_length=250)
    rna = models.CharField(max_length=250)




class Entry(models.Model):
    '''
    Entry document
    '''
    blastrps = models.EmbeddedField(
        model_container=Blastrps
    )
    blastx = models.EmbeddedField(
        model_container=Blastx
    )
    sra_metadata= models.EmbeddedField(
        model_container=SRAMetadata,
        blank=True,
        null=True
    )
    inv_metadata = models.EmbeddedField( 
        model_container=INVMetadata,
        blank=True,
        null=True
    )

    query_id = models.CharField(max_length=255)
    entry_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sample = models.CharField(max_length=255)

    verified = models.BooleanField(default=False) #update many by query_id
    virus_type = models.CharField(max_length=255, blank=True,) #update many by query_id
    host_organism = models.CharField(max_length=255, blank=True,) #update many by sample
    
    objects = models.DjongoManager()

    class Meta:
        verbose_name_plural = "Entries"
    
    def __str__(self):
        ''' Convert object to string '''
        return self.query_id
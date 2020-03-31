from djongo import models

#import user from vitiVir app? 

# Create your models here.
class Blastrps(models.Model):
    '''
    RPS-BLAST embedded document from rps_results.csv
    '''

    query_length = models.IntegerField()
    cdd_id = models.CharField(max_length=255)
    hit_id = models.CharField(max_length=255)
    evalue = models.FloatField()
    startQ = models.IntegerField()
    endQ = models.IntegerField
    frame = models.IntegerField
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


class SRAMetadata(models.Model):
    '''
    Metadata embedded document from SRA_metadata.csv
    '''

    ReleaseDate = models.CharField(max_length=250) #date and time?
    LoadDate = models.CharField(max_length=250)
    spots = models.IntegerField()
    bases = models.IntegerField() #numberlong?
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
    ProjectID= models.CharField(max_length=250) #int?
    Sample = models.CharField(max_length=250)
    BioSample = models.CharField(max_length=250)
    SampleType = models.CharField(max_length=250)
    TaxID = models.CharField(max_length=250) #int?
    ScientificName = models.CharField(max_length=250)
    SampleName = models.CharField(max_length=250)
    Tumor = models.CharField(max_length=250)
    CenterName = models.CharField(max_length=250)
    Submission = models.CharField(max_length=250)
    Consent = models.CharField(max_length=250)
    RunHash = models.CharField(max_length=250) #hash?
    ReadHash = models.CharField(max_length=250) #hash?

class INVMetadata(models.Model):
    ''' InViCeb metadata '''
    pass


class Entries(models.Model):
    '''
    Entry document
    '''

    #id auto created?
    query_id = models.CharField(max_length=255)
    sample = models.CharField(max_length=255)

    blastrps = models.EmbeddedField(
        model_container=Blastrps
    )
    blastx = models.EmbeddedField(
        model_container=Blastx
    )
    sra_metadata= models.EmbeddedField(
        model_container=SRAMetadata
    )
    inv_metadata = models.EmbeddedField(
        model_container=INVMetadata
    )


    #objects = models.DjangoManager()

    def __str__(self):
        ''' Convert object to string '''
        return self.query_id
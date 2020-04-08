from rest_framework import serializers

from . import models

class BlastrpsSerializer(serializers.ModelSerializer):
    ''' Serializer for blastrps '''

    class Meta:
        model = models.Blastrps
        fields = '__all__'


class BlastxSerializer(serializers.ModelSerializer):
    ''' Serializer for blastx '''

    class Meta:
        model = models.Blastx
        fields = '__all__'


class SRAMetadataSerializer(serializers.ModelSerializer):
    ''' Serializer for SRA metadata '''

    class Meta:
        model = models.SRAMetadata
        fields = '__all__'


# class INVMetadataSerializer(serializers.ModelSerializer):
#     ''' Serializer for INV metadata '''

#     class Meta:
#         model = models.INVMetadata
#         fields = '__all__'


class EntrySerializer(serializers.ModelSerializer):
    ''' Serializer for entry objects '''
    
    blastrps = BlastrpsSerializer()
    blastx = BlastxSerializer()
    sra_metadata = SRAMetadataSerializer()
    #inv_metadata = INVMetadataSerializer(source='*')

    class Meta:
        model = models.Entry
        fields = ('entry_id','query_id','sample','blastrps','blastx','sra_metadata')#,inv_metadata 
        depth = 2


    def create(self):
        ''' Create and return a new entry ''' 

        entry = models.Entry()
        entry.save()

        return entry





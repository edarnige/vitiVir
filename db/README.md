---
## The following instructions indicate how to populate the VitiVir database with SRA data.
---


# I. Adding new data to VitiVir

Due to the complexity of an entry and the number of fields, manual entry was not included in the web interface.  However, it is possible to manually create a new entry via the Django admin page. The best way to enter data is via a series of scripts, as described here.

### I.I Process RNA-seq data through the VirAnnot pipeline
##### Getting started:
- VirAnnot can be cloned from the following repository: https://github.com/marieBvr/virAnnot.
- Setup instructions can be found in the official documentation: https://virannot-docs.readthedocs.io/en/latest/.
- Genologin cluster configuration: http://bioinfo.genotoul.fr/index.php/genologin/
- Genouest cluster configuration: https://www.genouest.org/

Files in fastq format can be downloaded from the SRA using the following command in the command line where SraAccList.txt represents a list of SRA query IDs: 
```
parallel -j 1 fastq-dump --skip-technical -F --split-files -O fastq {} :::$(cat SraAccList.txt)
```
SraAccList.txt:
```
SRR10518885
SRR10518886
SRR10518887
```
```diff
- A list of SRA samples already analyzed is found in the SRA_done.txt file.  Add any new analyzed samples to this list to avoid re-analyzing.
```

Each step of the pipeline is launched in the command line. In the VirAnnot repository, the virAnnot.py file launches the step, the map.txt file determines which samples will be analyzed, parameters.yaml contains the configuration including cluster login, and the step.yaml file indicates which step is to be executedand with what input/output. Commands used in SRA analysis (in the directory containing fastq files):
```
1. virAnnot.py -m map.txt -p parameters.yaml -s step.yaml -n ReadSoustraction_vitis
2. virAnnot.py -m map.txt -p parameters.yaml -s step.yaml -n ReadSoustraction_phiX
3. virAnnot.py -m map.txt -p parameters.yaml -s step.yaml -n Demultiplex
4. virAnnot.py -m map.txt -p parameters.yaml -s step.yaml -n DemultiplexHtml
5. virAnnot.py -m map.txt -p parameters.yaml -s step.yaml -n Assembly_idba
6. virAnnot.py -m map.txt -p parameters.yaml -s step.yaml -n Filter
7. virAnnot.py -m map.txt -p parameters.yaml -s step.yaml -n Map_idba
8. virAnnot.py -m map.txt -p parameters.yaml -s step.yaml -n Blast_RPS
9. virAnnot.py -m map.txt -p parameters.yaml -s step.yaml -n Rps2ecsv
10. virAnnot.py -m map.txt -p parameters.yaml -s step.yaml -n Rps2blast
11. virAnnot.py -m map.txt -p parameters.yaml -s step.yaml -n Blast2ecsv_nr
```
It is important to check the output after each step to detect errors. One RPS-BLASTCSVandone BLASTXCSVfor each sample will be produced at the end of the pipeline

### I.II Retrieving metadata

Now that the RPS-BLAST and BLASTX results have been generated, the corresponding SRA metadata can be retrieved using the **get\_metadata.sh** script. This creates a CSV of metadata using two NCBI API calls, one for the general metadata, and a secondspecifically to retrieve the cultivar. This requires the installation of Entrez Direct: E-utilities onthe UNIX Command Line found [here](https://www.ncbi.nlm.nih.gov/books/NBK179288/). The input for get\_metadata.sh must be a text file with each sample name on one line, for example:

SRA_list.txt
```
SRR10518885
SRR10518886
SRR10518887
```

### I.III Populating the VitiVir database
With all of the BLASTX, RPS-BLAST, and metadata CSVs located in one folder, the **pop\_SRA\_db.py** script can be executed in order to populate the VitiVir database with new entries. This script must be executed in a folder containing the new CSVs to be entered. It is wise to test the entry of new data in a test database as to be sure to not pollute the existing entries. 




### I.IV Updating VitiVirSeq BLAST database
In the blastdb/ directory, make sure you have the correct version of NCBI toolkit installed on your machine.

Since new viral sequences have likely been added, the VitiVirSeq BLAST database must also be updated. Therfore, the old database must be destroyed. All vitiVirSeq.fasta\* files must be deleted. Be careful not to delete the NCBI toolkit. Then, the **ExportSeq.js** script can be launched to extract all viralsequences in fasta format. This will generate a vitiVirSeq.fasta file from which a BLASTdatabase can be constructed using the following command:
```
./ncbi-blast-2.10.0+/bin/makeblastdb -in vitiVirSeq.fasta -parse_seqids-blastdb_version 5 -title "vitiVirSeq" -dbtype nucl
```
Remove the first few lines of the fasta file if it contains the MongoDB description in order for the above command to function.



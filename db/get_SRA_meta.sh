#!/bin/bash

########
# Create metadata csv from a list of SRA
# Eden Darnige
# July 2020
########


header=1
samples=()

#Array of samples
while IFS= read -r sample; do
    samples[${#samples[*]}]=$sample
done < SRA_done.txt

#For each sample
for sample in ${samples[@]}; do

    searchQ=$sample
    echo $sample

    #Write header once
    if [ $header -eq 1 ] 
    then
        cols=$(esearch -db sra -q $searchQ | efetch -format runinfo | sed -n 1p)
        echo $cols,Cultivar > SRA_metadata.csv
        header=0
    fi 

    #Fill in with data
    meta_data=$(esearch -db sra -q $searchQ | efetch -format runinfo | sed -e 1d | egrep -v "^$")
    (esearch -db sra -q $searchQ | efetch -format native) > temp.xml
    #Cultivar comes from a different place
    cultivar=$(xmlstarlet sel -t -v '//EXPERIMENT_PACKAGE_SET/EXPERIMENT_PACKAGE/SAMPLE/SAMPLE_ATTRIBUTES/SAMPLE_ATTRIBUTE[TAG="cultivar"]/VALUE' -nl temp.xml)
    echo $meta_data,$cultivar >> SRA_metadata.csv

    rm temp.xml;
done 
//get sequences for virseq db
let acc_length = {} //acc:seq_length to find longest contig 

//Create object with unique accessions and their longest seq from mongo entries
db.virData_app_entry.find({'blastx.sequence':{'$exists':'true'}},
    {'blastx.sequence':1, 'blastx.accession':1, 'entry_id':1, "blastx.description":1, "query_id":1}).forEach(function(entry){ 
        if(entry.blastx.accession in acc_length){//if acc exists in acc_length
          if(acc_length[entry.blastx.accession]["sequence"].length < entry.blastx.sequence.length) { //if existing is less than new
            acc_length[entry.blastx.accession] = {"sequence":entry.blastx.sequence, "entry_id":entry.entry_id.hex().toString(),
            "query_id":entry.query_id, "description":entry.blastx.description}; //overwrite old values
          }
        } else{ //otherwise create first entry with acc
          acc_length[entry.blastx.accession] = {"sequence":entry.blastx.sequence, "entry_id":entry.entry_id.hex().toString(),
          "query_id":entry.query_id, "description":entry.blastx.description};
        }
  });

  //Loop through acc_length and write fasta file
  for (var acc in acc_length) {
    print(">"+acc_length[acc]["entry_id"]+" |"+acc+"|"+acc_length[acc]["description"]+"|"+acc_length[acc]["query_id"]+
    "\n"+acc_length[acc]["sequence"]); 
  }



  //in command line: mongo test ExportSeq.js > vitiVirSeq.fasta
  //test is name of db
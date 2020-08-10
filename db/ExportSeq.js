//get sequences for virseq db
let contig_length = {} //contig:seq_length to find longest sequence for a contig 

//Create object with unique contigs and their longest seq from mongo entries
db.virData_app_entry.find({'blastx.sequence':{'$exists':'true'}},
    {'blastx.sequence':1, 'blastx.accession':1, 'entry_id':1, "blastx.description":1, "query_id":1}).forEach(function(entry){ 
        if(entry.query_id in contig_length){//if contig exists in contig_length
          if(contig_length[entry.query_id]["sequence"].length < entry.blastx.sequence.length) { //if existing is less than new
            contig_length[entry.blastx.query_id] = {"sequence":entry.blastx.sequence, "entry_id":entry.entry_id.hex().toString(),
            "query_id":entry.query_id, "accession":entry.blastx.accession, "description":entry.blastx.description}; //overwrite old values
            console.log("test",contig_length[entry.blastx.query_id])
          }
        } else{ //otherwise create first entry with contig
          contig_length[entry.query_id] = {"sequence":entry.blastx.sequence, "entry_id":entry.entry_id.hex().toString(),
          "query_id":entry.query_id, "accession":entry.blastx.accession, "description":entry.blastx.description};
        }
  });

  //Loop through contig_length and write fasta file
  for (var contig in contig_length) {
    print(">"+contig_length[contig]["entry_id"]+" |"+contig_length[contig]["accession"]+"|"+contig_length[contig]["description"]+"|"+contig_length[contig]["query_id"]+
    "\n"+contig_length[contig]["sequence"]); 
  }



  //in command line: mongo test ExportSeq.js > vitiVirSeq.fasta
  //test is name of db
//get sequences for virseq db
db.virData_app_entry.find({'blastx.sequence':{'$exists':'true'}},
    {'blastx.sequence':1, 'blastx.accession':1, 'entry_id':1, "blastx.description":1,"query_id":1}).forEach(function(entry){ //sample and blastx.accession:1?
    print(">"+entry.entry_id.hex().toString()+"|"+entry.blastx.accession+"|"+entry.blastx.description+"|"+entry.query_id+
      "\n"+entry.blastx.sequence);
  });


  //in command line: mongo test ExportSeq.js > vitiVirSeq.fasta
  //test is name of db
# helperskripts_hybr_enr

gecluster.py is a helper skript to generate aligned sequences form clustering output (e.g. as provided by MeshClust)
cluster will generate seperate multifasta files and align them with mafft (using --adjustdirection ) and 
finally also reduce redundance by selecting only one sequence per species as determined by the headers, e.g. >[species_name]_contig_227,
thus species name needs underscores followed by "contig..."

baits.txt is a text file containing sequences for RNA baits used to enrich 813 single-copy orthologs of frogs and skinks

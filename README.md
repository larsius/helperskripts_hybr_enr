# helperskripts_hybr_enr

# gecluster.py is a helper skript to generate aligned sequences form clustering output (e.g. as provided by MeshClust)
# cluster will generate seperate multifasta files and align them with mafft (using --adjustdirection ) and 
# finally also reduce redundance by selecting only one sequence per species (determined by the headers, e.g. >[species_name]_contig_227,
# thus species name needs underscores foloowed by "contig..."

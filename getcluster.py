import subprocess
import re


cluster = "out.clstr"      ## result file from meshclust
allfasta ="nanoall.fasta"  ## a file containing all sequences 
cl_min = 20                ## min and max cluster size for evaluation
cl_max = 100

###########

def singlecluster(nr,listcon):
    mycluster = "cluster_"+str(nr)+".txt"
    OUT = open(mycluster,"w")
    for ctg in listcon:
        OUT.write(ctg)
        OUT.write("\n")
    OUT.close()

def fasta2dict(fastafile):
    dict = {}
    FASTA = open(fastafile,"r")
    for line in FASTA:
        line = line.rstrip()
        line = line.rstrip(" ")
        if line.startswith(">"):
            gname = line.lstrip(">")
            dict[gname]= ""
        else:
            dict[gname] += line
    FASTA.close()
    return(dict)


#### analyse cluster output for clusters between min and max cluster size

CLST = open(cluster,"r")
name = ""
allcontigs = []
list_of_lists = []
num = 0

for line in CLST:
    line = line.rstrip()
    if line.startswith(">"):
        #oldname = name
        #name = line.lstrip(">")
        if len(allcontigs) >= cl_min and len(allcontigs) <= cl_max:
            num += 1
            singlecluster(num,allcontigs)
            list_of_lists += [allcontigs]
        allcontigs = []

    else:
        #line = line.rstrip("*.")
        contig = re.findall(r">(\w+-\w+)",line)
        allcontigs.append(contig[0])
CLST.close()


###### GET FASTA for CLUSTER and do MAFFT alignments


fasta = fasta2dict(allfasta)


for number in range(len(list_of_lists)):
    seqname = "seq_cluster_"+str(number)+".fas"
    SEQ = open(seqname,"w")
    for gene in list_of_lists[number]:
        SEQ.write(">"+gene+"\n")
        SEQ.write(fasta[gene]+"\n")
    SEQ.close()

    subprocess.call(f"mafft --adjustdirection {seqname} > ali_{seqname}" ,shell = True)
    subprocess.call(f'sed "s/_R_//" -i ali_{seqname}' ,shell = True)   ### mafft --adjustdir creates headers with _R_ when rev-comp.


    #### the following procedure keeps just one sequence per species
    myali = "ali_"+seqname
    fastacluster = {}
    FASTA = open("ali_"+seqname,"r")
    for line in FASTA:
        line = line.rstrip()
        if line.startswith(">"):
            gname = re.findall(r"(\w+)_contig",line)
            fastacluster[gname[0]]= ""
        else:
            fastacluster[gname[0]] += line
    FASTA.close()

    uniqali = "uniq_ali_"+seqname+"ta"
    SEQ = open(uniqali,"w")
    for gene in fastacluster.keys():
        SEQ.write(">"+gene+"\n")
        SEQ.write(fastacluster[gene]+"\n")
    SEQ.close()


#### sort result files ###

subprocess.call(f"mkdir cluster_lists", shell = True)
subprocess.call(f"mv cluster*.txt cluster_lists/.", shell = True)

subprocess.call(f"mkdir cluster_fas", shell = True)
subprocess.call(f"mv seq* cluster_fas/.", shell = True)

subprocess.call(f"mkdir ali", shell = True)
subprocess.call(f"mv ali* cluster_ali/.", shell = True)

subprocess.call(f"mkdir uniq_ali", shell = True)
subprocess.call(f"cp uniq* uniq_ali/.", shell = True)
subprocess.call(f"mv uniq* FastaCon/fasta_files/.", shell = True)



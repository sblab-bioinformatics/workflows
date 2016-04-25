<!-- MarkdownTOC -->

- [Processing BS and oxBS-Seq data](#processing-bs-and-oxbs-seq-data)
    - [Quality control](#quality-control)
    - [Adapter trimming](#adapter-trimming)
    - [Alignment](#alignment)
    - [Clip read overlap](#clip-read-overlap)
    - [Mark duplicates](#mark-duplicates)
    - [Methylation calling](#methylation-calling)
    - [Useful resources](#useful-resources)

<!-- /MarkdownTOC -->

## Processing BS and oxBS-Seq data

This a typical pipeline leading from raw fastq reads to methylation calling at individual CpG sites. There is no difference in data
processing between BS and oxBS reads, after all oxBS is (should be) identical to BS if no 5hmC is present. This pipeline applies to
whole genome bisulfite sequencing.

### Quality control

Run [FastQC](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/) on raw fastq files. In contrast to regular sequencing
you expect the *Per base sequence content* plot to show a close-to-zero percentage for **C** and a higher (~50%) percentage of **T**, at least
for mammalian genomes. This indicates that unmethylated cytiosines (_i.e._ the vast majority) are converted to T by bisulfite
treatment. Read quality should be comparable to standard 

### Adapter trimming

BS-Seq reads can be heavily contaminated with adapters. We use [cutadapt](http://cutadapt.readthedocs.org/en/stable/guide.html) to trim adapters. Optionally quality trimming can also be applied,
although we prefer the downstream aligner and processing to deal with it. Note that a particularly bad read quality is probably an indication that something went wrong.

For paired end reads with TruSeq adapters the typical `cutadapt` command looks like:

```
cutadapt -m 10 -O 1 -a AGATCGGAAGAGC -A AGATCGGAAGAGC -o fastq_trimmed/$out1 -p fastq_trimmed/$out2 $fq1 $fq2
```

`-m 10` discards reads shorter than 10 bp after trimming, `-O 1` trims reads even if the overlap with the adapter is just 1 bp, `cutadapt`'s default
is `-O 3`, so we are a bit more conservative.

### Alignment

We find good results with [bwameth](https://github.com/brentp/bwa-meth), a wrapper around the popular `bwa mem`. Default settings typically work fine:

```
bwameth.py -t 4 --reference $ref --prefix bwameth/${out} fastq_trimmed/$out1 fastq_trimmed/$out2
```

`$ref` is the genome sequence indexed by `bwameth/bwa`.

Worth noting that the most popular aligner for BS-Seq data is [bismark](http://www.bioinformatics.babraham.ac.uk/projects/bismark/), which wraps `bowtie1` or `bowtie2`.

With `bwameth.py` we get pretty high alignment rates, >80%. `bismark` with default settings is usually more conservative, returning ~60% alignment rate.

### Clip read overlap

*Only relevant for paired-end data*. Read pairs tend to overlap if read length is above 75-100bp:

```
R1
>>>>>>>>>>>>>>>
           <<<<<<<<<<<<<<
                         R2
```

The overalapping part should be clipped from one of the two reads to to avoid double-counting read coverage. For this we use
[bam clipOverlap](http://genome.sph.umich.edu/wiki/BamUtil:_clipOverlap):

```
bam clipOverlap --in bwameth/${out}.unclipped.bam --out bwameth/${out}.bam --stats --storeOrig XC &&
```

### Mark duplicates

As for regular genome sequencing, reads mapping to the same position are marked as PCR duplicates and ignored for methylation calling. We use [picard MarkDuplicates](https://broadinstitute.github.io/picard/command-line-overview.html) for this:

```
java -Xmx3G -jar picard.jar MarkDuplicates VALIDATION_STRINGENCY=SILENT TMP_DIR=./ I=${inBam} O=${outBam} M=${outBam}.markdup.txt
```

For standard BS-Seq libraries the duplication rate can be fairly high since the bisulfite treatment makes most of the reads unsequencable.
With PCR-Free protocol ([McInroy Plos One](http://journals.plos.org/plosone/article/metrics?id=10.1371%2Fjournal.pone.0152322)) this step might be skipped and anyway the duplication rate is fairly low for typical experiments.

### Methylation calling

We use custom scripts for extracting methylation calling from bam files. [bam2methylation.py](https://github.com/dariober/bioinformatics-cafe/tree/master/bam2methylation)
is a wrapper around `samtools mpileup`:

```
bam2methylation.py -i $bam -r $ref -A -s ' -q 10 -F2820' -mm -mq 15 -l hg19.allCpG.bed.gz > $bdg
addCGcontextToBdg.sh $bdg $ref 7 
```

Reads with bits 2820 (read unmapped, not primary alignment, read fails platform/vendor quality checks, supplementary alignment) are ignored, as well as reads
with mapping quality below 10. For convenience we might extract methylation only at CpG sites, as these are more variable and "interesting". Non CpG sites are usually
almost completely de-methylated (1%). In fact, it's useful to call methylation at non CpG sites, at least, on one chromosome to make sure methylation is low, indicating
good C to T conversion rate. Script [addCGcontextToBdg.sh](https://github.com/dariober/bioinformatics-cafe/blob/master/addCGcontextToBdg.sh) is useful to assign
the sequence context around a C. 

At the end of this step you have a table in bed-like format where each row is the position of a cytosines with the associated count of unconverted cytosines (i.e. methylated) and total cytosines.
What to do from here depends on the extact questions being asked.

### Useful resources

The [bismark](http://www.bioinformatics.babraham.ac.uk/projects/bismark/) home page has very good advice about BS-Seq data processing. See also the paper associted to [bwameth](http://arxiv.org/abs/1401.1129).

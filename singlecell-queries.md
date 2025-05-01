# Archive: #singlecell-queries

## 2025-04-03

**Sean Davis** (08:47:57):
> This falls into the category of "do my homework for me." How do people find, manage, store, use, and reuse cell type marker genes and marker gene sets?

**Jared Andrews** (09:01:56):
> Store em in a big ol GMT file and filter out sets as needed. We do it for cell markers, gene sets for GSEA or enrichment analysis, etc.

**Tim Triche** (09:04:47):
> I see someone decided to kick the “factorize vs compare to published lists” hornets nest this morning

**Sean Davis** (09:07:41) (in thread):
> I'm not really worried about the hornet nest today. Just the single hornet (or just a few hornets) representing marker gene set-adjacent management and use.

**Tim Triche** (09:08:48) (in thread):
> GMT it is, then! We find GSEA type analyses on factors to be super handy, soit’snot like I am opposed to them.

**Tim Triche** (09:09:55) (in thread):
> I just wonder a lot about the differences between cell states and fates, andI’veseen way too many arbitrarily gated flow datasets to trust academic markers

**Sean Davis** (09:10:37) (in thread):
> Do you do anything tricky to manage gene set metadata like overloading the description column or something like that?

**Tim Triche** (09:11:44) (in thread):
> msigdbr has been a handy alternative to the “great big GMT file” approach but it too has its drawbacks.

**Jared Andrews** (09:12:19) (in thread):
> Nothing quite so complex, though it is a frequent issue. We typically slap the source (publication, analysis, whatever) in the description column and keep the name specific enough to know what the biology entails. It'd be nice to have a more robust system for managing (and easily filtering) them though.

**Jared Andrews** (10:11:24) (in thread):
> We use msigdbr on top of our own lists, but the C8 collection for cell types is too broad and annoying to filter. It's still our go-to for GO/KEGG/Reactome

**Tim Triche** (10:15:34) (in thread):
> this is one of those things where a more flexible annotationhub architecture could be super helpful

**Tim Triche** (10:15:44) (in thread):
> and oddly aligned with the post-apocalypse NIH priorities

**Tim Triche** (10:16:20) (in thread):
> I don't just want***someone else's tibble***, I want a crowdsourced tibble that I can add to.  Also I don't care for the Broad's licensing terms

**Tim Triche** (10:17:38) (in thread):
> I just walked a student through EnrichmentBrowser (awesome package btw) yesterday and remembered why this process can be a drag (in her case I wanted a consensus list of genes and interactions for melphalan metabolism and clearance to map population AF diffs onto)

**Tim Triche** (10:18:53) (in thread):
> so yeah we use this process to "gate" cells (see also the Human Cell Atlas CAP, aka the Cell Annotation Platform, for relevant developments in that respect) but "gate" and "cell" are evolving terms over time and it's useful to have the resource evolve too

**Tim Triche** (10:20:25) (in thread):
> [https://celltype.info/search/cell-labels](https://celltype.info/search/cell-labels)

**Tim Triche** (10:20:30) (in thread):
> CAP not CAB, sorry.

**Tim Triche** (10:21:02) (in thread):
> so yeah we use this process to "gate" cells (see also the Human Cell Atlas CAP, aka the Cell Annotation Platform, for relevant developments in that respect) but "gate" and "cell" are evolving terms over time and it's useful to have the resource evolve too

**Tim Triche** (10:22:44) (in thread):
> I still can't believe I did this to COVID-era 1st-year grad students, but in my defense, they literally asked for it.[https://trichelab.github.io/lab_use_content/project2.html](https://trichelab.github.io/lab_use_content/project2.html)

**Tim Triche** (10:24:33) (in thread):
> my "answer key" (no right answers, I structured it for students to extend into their own projects, it's just an example)[https://trichelab.github.io/lab_use_content/project2_chunks/project2_tim.html](https://trichelab.github.io/lab_use_content/project2_chunks/project2_tim.html)

**Tim Triche** (10:25:04) (in thread):
> I did use it again yesterday with plyranges and... well, we have so much to offer students that could make their lives and science better.

**Vince Carey** (10:33:54) (in thread):
> blurting things out: any chance of connecting these concepts to celldex?  any specific role of cell ontology?  systematic approach to sharing identities of "new" cell types via PRs to the ontology?  (we could write code to merge***information***from a PR that we liked with a current cell ontology image, increasing flexibility and capturing provenance)

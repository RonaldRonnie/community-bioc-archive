# Archive: #miaverse

## 2025-03-31

**Hassan Diab** (04:23:54):
> Hello,
> 
> I want to calculate the PCA axes for a TSE object, using runPCA. I have two questions;
> 
> 1) Is CLR-transformation recommended before runPCA?
> 2) if so,  does runPCA do the CLR-transformation internally, or should I runPCA on the CLR-transformed assay?
> 
> Thanks!

**Tuomas Borman** (04:37:38) (in thread):
> Hello,
> 
> here is a table that summarizes the common options for ordination:[https://microbiome.github.io/OMA/docs/devel/pages/beta_diversity.html](https://microbiome.github.io/OMA/docs/devel/pages/beta_diversity.html)
> 1. CLR + PCA is also called as Aitchison distance which is a common option --> yes, you should apply PCA for CLR-transformed data
> 2. `runPCA`does not do any transformations, you should apply it beforehands with`transformAssay`and specify the CLR-transformed matrix with`assay.type`

**Leo Lahti** (09:03:04) (in thread):
> Yes.

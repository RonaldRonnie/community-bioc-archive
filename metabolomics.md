# Archive: #metabolomics

## 2025-04-01

**Johannes Rainer** (06:00:15):
> Resource of reproducible workflows (playbooks?) metabolomics data analysis. By@Philippine Louailand contributors.[https://rformassspectrometry.github.io/Metabonaut/](https://rformassspectrometry.github.io/Metabonaut/)
  - Attachment (rformassspectrometry.github.io): [Exploring and Analyzing LC-MS Data](https://rformassspectrometry.github.io/Metabonaut/)

**Gavin Rhys Lloyd** (06:25:09) (in thread):
> This looks very nice, great job!
> 
> If you are interested I could help you to use structToolbox ([link to vignette](https://computational-metabolomics.github.io/structToolbox/articles/data_analysis_omics_using_the_structtoolbox.html#partial-least-squares-pls-analysis-of-a-untargeted-lc-ms-based-clinical-metabolomics-dataset-)) for the multivariate (and univariate if you liked) section(s). Happy to make extra wrappers for missing steps/charts (e.g. I dont have one for limma... yet).
> 
> Or I could add a pull request to add structToolbox as an alternative example; it might depend if your plan is to showcase workflows using different tools, or not

**Gavin Rhys Lloyd** (06:25:50) (in thread):
> This looks very nice, great job!
> 
> If you are interested I could help you to use structToolbox ([link to vignette](https://computational-metabolomics.github.io/structToolbox/articles/data_analysis_omics_using_the_structtoolbox.html#partial-least-squares-pls-analysis-of-a-untargeted-lc-ms-based-clinical-metabolomics-dataset-)) for the multivariate (and univariate if you liked) section(s). Happy to make extra wrappers for missing steps/charts (e.g. I dont have one for limma... yet).
> 
> Or I could add a pull request to add structToolbox as an alternative example; it might depend if your plan is to showcase workflows using different tools, or not

**Johannes Rainer** (06:53:31) (in thread):
> hey! that's great! ideally a PR with a separate vignette:blush:- loading the data after preprocessing. we can also discuss through github issues at Metabonaut


## 2025-04-02

**Pablo** (05:54:18) (in thread):
> I have been referring to Metabonaut a lot since it's launch! Great job@Philippine Louailand others :)

**Kozo Nishida** (13:07:37):
> Does anyone know if there's a function that returns a SummarizedExperiment of a study in MetaboLights, like the following metabolomicsWorkbenchR do_query function?
> ```
> SE = do_query(
>     context = 'study',
>     input_item = 'study_id',
>     input_value = 'ST000001',
>     output_item = 'SummarizedExperiment' # or 'DatasetExperiment'
> )
> ```

**Gavin Rhys Lloyd** (13:27:48) (in thread):
> MetaboLights is mostly raw data. SummarizedExperiment is better suited to peak tables obtained after processing the raw data.
> You could try something like[https://rformassspectrometry.github.io/MsBackendMetaboLights/](https://rformassspectrometry.github.io/MsBackendMetaboLights/)combined with the xcms package to process the data into a peak table (I think xcms can output the peak table as a SummarisedExperiment).

**Gavin Rhys Lloyd** (13:30:18) (in thread):
> also there is a nice example of this in the Metabonaut repo posted recently:[https://rformassspectrometry.github.io/Metabonaut/articles/a-end-to-end-untargeted-metabolomics.html](https://rformassspectrometry.github.io/Metabonaut/articles/a-end-to-end-untargeted-metabolomics.html)


## 2025-04-03

**Kozo Nishida** (00:35:41) (in thread):
> Thank you for your reply, Gavin.
> Sorry, I didn’t explain myself clearly.
> I wasn’t referring to the raw data in MetaboLights, but rather to the ISA-TAB file format—specifically the files starting with**s_**or**m_**.
> I wanted to ask whether there is already functionality to create a`SummarizedExperiment`from those files.
> It doesn’t seem like that functionality is included in examples MsBackendMetaboLights or Metabonaut either.

**Kozo Nishida** (00:37:52) (in thread):
> And if it turns out that this functionality doesn’t exist anywhere in Bioconductor, I wanted to ask this community where it might make the most sense to add it.

**Kozo Nishida** (00:37:53) (in thread):
> And if it turns out that this functionality doesn’t exist anywhere in Bioconductor, I wanted to ask this community where it might make the most sense to add it.

**Kozo Nishida** (00:48:55) (in thread):
> Much of what I want to do is already implemented in[https://github.com/tidymass/massdataset/tree/main/R](https://github.com/tidymass/massdataset/tree/main/R), but it doesn’t support database-backed approaches.
> The massdataset package is in**tidymass**framework, and it is different from Bioconductor.
> I’d like to discuss what kind of approach would be best for the community as a whole (for reading ISA-TABs in MetaboLights).

**Kozo Nishida** (00:48:56) (in thread):
> Much of what I want to do is already implemented in[https://github.com/tidymass/massdataset/tree/main/R](https://github.com/tidymass/massdataset/tree/main/R), but it doesn’t support database-backed approaches.
> The massdataset package is in**tidymass**framework, and it is different from Bioconductor.
> I’d like to discuss what kind of approach would be best for the community as a whole (for reading ISA-TABs in MetaboLights).

**Tuomas Borman** (11:14:52) (in thread):
> Hi!
> 
> As part of a larger project, we developed a method for retrieving data tables from MetaboLights. The primary goal of the HoloFoodR package is to fetch data from the HoloFood database. However, for certain data types, the HoloFood database points to MetaboLights, so we created methods to retrieve those data tables.
> 
> Initially, we didn't plan to make the MetaboLights retrieval method directly accessible to users, but rather keep it as internal function. However, today I made it available and did some testing to ensure it works also for data outside this HoloFood project.
> 
> Here is reference page:[https://ebi-metagenomics.github.io/HoloFoodR/reference/getMetaboLights.html](https://ebi-metagenomics.github.io/HoloFoodR/reference/getMetaboLights.html)You can retrieve data specified by study identifier
> ```
> # The latest changes are not yet in Bioc
> remotes::install_github("EBI-Metagenomics/HoloFoodR")
> library(HoloFoodR)
> 
> # Get data as list
> res <- getMetaboLights("MTBLS11993")
> # Get data as SE
> se <- getMetaboLights("MTBLS3540", output = "SE")
> ```
> Is this what you are looking for?
  - Attachment (ebi-metagenomics.github.io): [Get metabolomic data from MetaboLights database — getMetaboLights](https://ebi-metagenomics.github.io/HoloFoodR/reference/getMetaboLights.html)

**Tuomas Borman** (11:14:53) (in thread):
> Hi!
> 
> As part of a larger project, we developed a method for retrieving data tables from MetaboLights. The primary goal of the HoloFoodR package is to fetch data from the HoloFood database. However, for certain data types, the HoloFood database points to MetaboLights, so we created methods to retrieve those data tables.
> 
> Initially, we didn't plan to make the MetaboLights retrieval method directly accessible to users, but rather keep it as internal function. However, today I made it available and did some testing to ensure it works also for data outside this HoloFood project.
> 
> Here is reference page:[https://ebi-metagenomics.github.io/HoloFoodR/reference/getMetaboLights.html](https://ebi-metagenomics.github.io/HoloFoodR/reference/getMetaboLights.html)You can retrieve data specified by study identifier
> ```
> # The latest changes are not yet in Bioc
> remotes::install_github("EBI-Metagenomics/HoloFoodR")
> library(HoloFoodR)
> 
> # Get data as list
> res <- getMetaboLights("MTBLS11993")
> # Get data as SE
> se <- getMetaboLights("MTBLS3540", output = "SE")
> ```
> Is this what you are looking for?
  - Attachment (ebi-metagenomics.github.io): [Get metabolomic data from MetaboLights database — getMetaboLights](https://ebi-metagenomics.github.io/HoloFoodR/reference/getMetaboLights.html)

**Kozo Nishida** (11:31:19) (in thread):
> Hi! Thank you for your reply!
> Yes that is what I'm looking for! (I think that's very likely.)[https://github.com/EBI-Metagenomics/HoloFoodR/blob/devel/R/getMetaboLights.R#L280](https://github.com/EBI-Metagenomics/HoloFoodR/blob/devel/R/getMetaboLights.R#L280)Unfortunately, I encountered the following error in my environment.
> ```
> > res <- getMetaboLights("MTBLS4381")
> curl::curl_parse_url(url, baseurl = base_url, decode = FALSE) でエラー: 
>   Failed to parse URL: Bad scheme
> ```
> But I’ll ask about it on GitHub Issues instead.[https://github.com/EBI-Metagenomics/HoloFoodR/issues](https://github.com/EBI-Metagenomics/HoloFoodR/issues)Thanks again for your reply—I really appreciate it!

**Kozo Nishida** (11:31:22) (in thread):
> Hi! Thank you for your reply!
> Yes that is what I'm looking for![https://github.com/EBI-Metagenomics/HoloFoodR/blob/devel/R/getMetaboLights.R#L280](https://github.com/EBI-Metagenomics/HoloFoodR/blob/devel/R/getMetaboLights.R#L280)Unfortunately, I encountered the following error in my environment.
> ```
> > res <- getMetaboLights("MTBLS4381")
> curl::curl_parse_url(url, baseurl = base_url, decode = FALSE) でエラー: 
>   Failed to parse URL: Bad scheme
> ```
> But I’ll ask about it on GitHub Issues instead.[https://github.com/EBI-Metagenomics/HoloFoodR/issues](https://github.com/EBI-Metagenomics/HoloFoodR/issues)Thanks again for your reply—I really appreciate it!

**Kozo Nishida** (11:31:26) (in thread):
> Hi! Thank you for your reply!
> Yes that is what I'm looking for![https://github.com/EBI-Metagenomics/HoloFoodR/blob/devel/R/getMetaboLights.R#L280](https://github.com/EBI-Metagenomics/HoloFoodR/blob/devel/R/getMetaboLights.R#L280)Unfortunately, I encountered the following error in my environment.
> ```
> > res <- getMetaboLights("MTBLS4381")
> curl::curl_parse_url(url, baseurl = base_url, decode = FALSE) でエラー: 
>   Failed to parse URL: Bad scheme
> ```
> But I’ll ask about it on GitHub Issues instead.[https://github.com/EBI-Metagenomics/HoloFoodR/issues](https://github.com/EBI-Metagenomics/HoloFoodR/issues)Thanks again for your reply—I really appreciate it!

**Kozo Nishida** (11:34:36) (in thread):
> Hi! Thank you for your reply!
> Yes that is what I'm looking for! (I think that's very likely.)[https://github.com/EBI-Metagenomics/HoloFoodR/blob/devel/R/getMetaboLights.R#L280](https://github.com/EBI-Metagenomics/HoloFoodR/blob/devel/R/getMetaboLights.R#L280)Unfortunately, I encountered the following error in my environment.
> ```
> > res <- getMetaboLights("MTBLS4381")
> curl::curl_parse_url(url, baseurl = base_url, decode = FALSE) でエラー: 
>   Failed to parse URL: Bad scheme
> ```
> But I’ll ask about it on GitHub Issues instead.[https://github.com/EBI-Metagenomics/HoloFoodR/issues](https://github.com/EBI-Metagenomics/HoloFoodR/issues)Thanks again for your reply—I really appreciate it!

**Tuomas Borman** (11:39:59) (in thread):
> Thanks, I will check it ASAP

**Tuomas Borman** (12:03:44) (in thread):
> I was able to replicate the issue. I had older version of httr2 package. I will fix this today

**Tuomas Borman** (13:04:40) (in thread):
> Not the nicest start, but now the issue is fixed:[https://github.com/EBI-Metagenomics/HoloFoodR/pull/41](https://github.com/EBI-Metagenomics/HoloFoodR/pull/41)Behavior of`httr2::url_parser()`was changed and I had not noticed that.
> 
> Thanks for letting me know@Kozo NishidaPlease tell if you still encounter in problems or have feature requests.

**Tuomas Borman** (13:04:41) (in thread):
> Not the nicest start, but now the issue is fixed:[https://github.com/EBI-Metagenomics/HoloFoodR/pull/41](https://github.com/EBI-Metagenomics/HoloFoodR/pull/41)Behavior of`httr2::url_parser()`was changed and I had not noticed that.
> 
> Thanks for letting me know@Kozo NishidaPlease tell if you still encounter in problems or have feature requests.

**Leo Lahti** (16:43:17) (in thread):
> Cool! HoloFoodR might not be the most logical place to find the metabolights functionality, so perhaps we could in the longer run consider other, metabolomics oriented packages as a home for it. Just a thought.

# Archive: #singularity

## 2025-04-01

**Alex Mahmoud** (14:01:50):
> Hi all! I got some time/energy this week, and re-started the effort to build (and automate building of) our containers as singularity containers as well. If you have an environment to test, especially restricted HPC type envs where docker is not available, I would appreciate any testing you might be able to do, so I get as many data points as possible as I refine the image and build stack!
> ```
> apptainer remote add --no-login SylabsCloud cloud.sycloud.io
> apptainer remote use SylabsCloud
> singularity pull --arch amd64[library://almahmoud/almahmoud/bioconductor:3.20](library://almahmoud/almahmoud/bioconductor:3.20)
> ```


## 2025-04-03

*12:28:47 - @Kasper D. Hansen has joined the channel*
**Kasper D. Hansen** (12:29:14):
> Shouldn't this be rolled into#containers

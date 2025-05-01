# Archive: #containers

## 2025-04-01

**Sean Davis** (10:14:53) (in thread):
> [https://github.com/Bioconductor/bioconductor_docker/issues/119](https://github.com/Bioconductor/bioconductor_docker/issues/119)
  - Attachment: [#119 Push of arm64 docker image to dockerhub failing, resulting in missing recent arm64 builds of bioconductor_docker](https://github.com/Bioconductor/bioconductor_docker/issues/119)

**Sean Davis** (10:14:56) (in thread):
> [https://github.com/Bioconductor/bioconductor_docker/issues/119](https://github.com/Bioconductor/bioconductor_docker/issues/119)
  - Attachment: [#119 Push of arm64 docker image to dockerhub failing, resulting in missing recent arm64 builds of bioconductor_docker](https://github.com/Bioconductor/bioconductor_docker/issues/119)

**Sean Davis** (10:16:34) (in thread):
> ....slack conversation to github issues.

**Sean Davis** (10:17:17) (in thread):
> ....slack conversation to github issues.

**Alex Mahmoud** (10:53:41) (in thread):
> Thank you@Sean Davis! I put in some debugging statements yesterday to get to the bottom of it, but was surprised when just adding that made more pass, and then forgot to follow up. I restarted a failed GHA job this morning, and it all passed. It seems to be a timing issue, possibly related to Dockerhub rate limiting... Good news is that it pushed both archs to both repos, so ghcr and dockerhub should be fully in sync now cc@Kasper D. Hansen


## 2025-04-02

**Alex Mahmoud** (14:45:12) (in thread):
> To close this loop, the issue was likely due to rate limiting by Dockerhub, and a retry was added on the merge/push job that takes the separate arch images and merges them into a single multi-arch tag, and wait+retry seems to have been enough for now to fix the ephemeral issue.
> TLDR, problem fixed both temporarily and systematically, and both archs should exist as expected! Thank you all for reporting and sorry it took so long for me to get to it
  - File (PNG): [image.png](https://community-bioc.slack.com/files/U34P8RS3B/F08M52J51QQ/image.png)

**Alex Mahmoud** (14:51:55) (in thread):
> To close this loop, the issue was likely due to rate limiting by Dockerhub, and a retry was added on the merge/push job that takes the separate arch images and merges them into a single multi-arch tag, and wait+retry seems to have been enough for now to fix the ephemeral issue.
> TLDR, problem fixed both temporarily and systematically, and both archs should exist as expected! Thank you all for reporting and sorry it took so long for me to get to it

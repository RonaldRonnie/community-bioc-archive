# Archive: #documentation-translation

## 2025-03-31

**Laurent Gatto** (08:34:51):
> Hi@Kozo Nishida- does the English lesson template update when we push changes to the original github repo? If not, do we have any plans on how to manage changes?

**Ouma Ronald** (12:18:52):
> Hi<!channel>. Hope you had a lovely day,  I would like to know how I can start with contributing to the`documentation-translation`.   I appreciate any steps or guidance:pray:.@Maria Doyle,@Marcel Ramos Pérez,@Izabela Mamede

**Laurent Gatto** (13:04:54) (in thread):
> Hi@Ouma Ronald- what languages could you help with? We have a couple of dedicated working groups that work on different languages (see[https://workinggroups.bioconductor.org/currently-active-working-groups-committees.html](https://workinggroups.bioconductor.org/currently-active-working-groups-committees.html)).
  - Attachment (workinggroups.bioconductor.org): [Chapter 2 Currently Active Working Groups / Committees | Bioconductor Working Groups: Guidelines and activities](https://workinggroups.bioconductor.org/currently-active-working-groups-committees.html)

**Kozo Nishida** (14:50:43) (in thread):
> Hi@Laurent GattoYes, the English lesson template will be updated when we push changes to the original GitHub repository.
> However, currently the original GitHub repository is connected to[https://github.com/swcarpentry-ja/bioc-intro](https://github.com/swcarpentry-ja/bioc-intro), not[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro).
> This is because I don't have sufficient permissions for[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro).
> If you'd like to connect the[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro)to[https://bioconductor.crowdin.com/](https://bioconductor.crowdin.com/), either I need to be granted higher permissions for[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro), or you (you are a admin user of[https://bioconductor.crowdin.com/](https://bioconductor.crowdin.com/)) will need to change the GitHub integration settings in Crowdin.

**Kozo Nishida** (14:50:44) (in thread):
> Hi@Laurent GattoYes, the English lesson template will be updated when we push changes to the original GitHub repository.
> However, currently the original GitHub repository is connected to[https://github.com/swcarpentry-ja/bioc-intro](https://github.com/swcarpentry-ja/bioc-intro), not[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro).
> This is because I don't have sufficient permissions for[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro).
> If you'd like to connect the[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro)to[https://bioconductor.crowdin.com/](https://bioconductor.crowdin.com/), either I need to be granted higher permissions for[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro), or you (you are a admin user of[https://bioconductor.crowdin.com/](https://bioconductor.crowdin.com/)) will need to change the GitHub integration settings in Crowdin.

**Kozo Nishida** (14:50:45) (in thread):
> Hi@Laurent GattoYes, the English lesson template will be updated when we push changes to the original GitHub repository.
> However, currently the original GitHub repository is connected to[https://github.com/swcarpentry-ja/bioc-intro](https://github.com/swcarpentry-ja/bioc-intro), not[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro).
> This is because I don't have sufficient permissions for[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro).
> If you'd like to connect the[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro)to[https://bioconductor.crowdin.com/](https://bioconductor.crowdin.com/), either I need to be granted higher permissions for[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro), or you (you are a admin user of[https://bioconductor.crowdin.com/](https://bioconductor.crowdin.com/)) will need to change the GitHub integration settings in Crowdin.

**Kozo Nishida** (15:04:16):
> By the way, with the rapid advancement of LLMs, some people might prefer to speed up translations using ChatGPT or Gemini instead of DeepL or Google Translate.
> There might also be preferences for managing translations with GitHub and gettext rather than using Crowdin.
> If anyone has any ideas, please feel free to share them in this channel.


## 2025-04-01

**Laurent Gatto** (06:58:32) (in thread):
> Thanks. Could you confirm that you are kozo2 on github.

**Kozo Nishida** (07:04:58) (in thread):
> [https://github.com/kozo2](https://github.com/kozo2)is me.
> It still appears that my permission for[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro)is insufficient to allow synchronization with[https://bioconductor.crowdin.com/](https://bioconductor.crowdin.com/).
  - Attachment (bioconductor.crowdin.com): [Crowdin Enterprise](https://bioconductor.crowdin.com/)

**Kozo Nishida** (07:05:00) (in thread):
> [https://github.com/kozo2](https://github.com/kozo2)is me.
> It still appears that my permission for[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro)is insufficient to allow synchronization with[https://bioconductor.crowdin.com/](https://bioconductor.crowdin.com/).
  - Attachment (bioconductor.crowdin.com): [Crowdin Enterprise](https://bioconductor.crowdin.com/)

**Laurent Gatto** (07:58:40) (in thread):
> I added you just now as a maintainer - could you try again.

**Laurent Gatto** (08:16:14) (in thread):
> I added you just now as a maintainer - could you try again.

**Kozo Nishida** (09:17:30) (in thread):
> It seems that being a maintainer doesn’t provide sufficient permissions to perform the integration.
> It looks like higher-level permissions are required, as shown by the settings on the right side of the screen.
> Would it be possible to grant me permissions higher than maintainer?
  - File (PNG): [image.png](https://community-bioc.slack.com/files/U34P8RS3B/F08LB0NGEG4/image.png)
  - File (PNG): [image.png](https://community-bioc.slack.com/files/U34P8RS3B/F08LAHNGVM0/image.png)

**Laurent Gatto** (12:33:31) (in thread):
> Could you try again.

**Laurent Gatto** (12:33:38) (in thread):
> I gave you admin rights.

**Kozo Nishida** (12:39:12) (in thread):
> Thank you. Now I can see carpentries-incubator/bioc-intro from[bioconductor.crowdin.com](http://bioconductor.crowdin.com)github integration.
> For the purpose of integration, I will add a YAML file identical to[https://github.com/swcarpentry-ja/bioc-intro/blob/main/crowdin.yml](https://github.com/swcarpentry-ja/bioc-intro/blob/main/crowdin.yml)to the main branch of[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro). I hope that's alright with you.

**Laurent Gatto** (12:40:48) (in thread):
> Thanks. Could you send a PR with that yaml file and tag me and@Charlotte Soneson, so that we see it and can also report back in the teaching meetings.

**Kozo Nishida** (12:41:02) (in thread):
> OK. I will send a PR.

**Kozo Nishida** (12:52:51) (in thread):
> I sent the PR[https://github.com/carpentries-incubator/bioc-intro/pull/144](https://github.com/carpentries-incubator/bioc-intro/pull/144)


## 2025-04-02

**Kozo Nishida** (04:40:16) (in thread):
> Hi@Laurent GattoI added[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro)`main`branch to[bioconductor.crowdin.com](http://bioconductor.crowdin.com)to sync with the Crowdin English source text.
> I believe the latest commit on GitHub is now synced with Crowdin. If it's not, please let me know.
> The synchronization is set to occur every hour.
> And, translations are pushed to the`l10n_main`branch, not the`main`branch.
> (For example,[https://github.com/carpentries-incubator/bioc-intro/tree/l10n_main/locale/fr](https://github.com/carpentries-incubator/bioc-intro/tree/l10n_main/locale/fr)is the link for French.)

**Kozo Nishida** (04:40:17) (in thread):
> Hi@Laurent GattoI added[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro)main branch to[bioconductor.crowdin.com](http://bioconductor.crowdin.com)to sync with the Crowding English source text.
> I believe the latest commit on GitHub is now synced with Crowdin. If it's not, please let me know.
> The synchronization is set to occur every hour.
> Also, translations are pushed to the`l10n_main`branch, not the`main`branch.

**Kozo Nishida** (04:40:33) (in thread):
> Hi@Laurent GattoI added[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro)`main`branch to[bioconductor.crowdin.com](http://bioconductor.crowdin.com)to sync with the Crowding English source text.
> I believe the latest commit on GitHub is now synced with Crowdin. If it's not, please let me know.
> The synchronization is set to occur every hour.
> Also, translations are pushed to the`l10n_main`branch, not the`main`branch.

**Kozo Nishida** (04:40:45) (in thread):
> Hi@Laurent GattoI added[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro)`main`branch to[bioconductor.crowdin.com](http://bioconductor.crowdin.com)to sync with the Crowdin English source text.
> I believe the latest commit on GitHub is now synced with Crowdin. If it's not, please let me know.
> The synchronization is set to occur every hour.
> Also, translations are pushed to the`l10n_main`branch, not the`main`branch.

**Kozo Nishida** (04:41:19) (in thread):
> Hi@Laurent GattoI added[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro)`main`branch to[bioconductor.crowdin.com](http://bioconductor.crowdin.com)to sync with the Crowdin English source text.
> I believe the latest commit on GitHub is now synced with Crowdin. If it's not, please let me know.
> The synchronization is set to occur every hour.
> And, translations are pushed to the`l10n_main`branch, not the`main`branch.

**Kozo Nishida** (04:41:40) (in thread):
> Hi@Laurent GattoI added[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro)`main`branch to[bioconductor.crowdin.com](http://bioconductor.crowdin.com)to sync with the Crowdin English source text.
> I believe the latest commit on GitHub is now synced with Crowdin. If it's not, please let me know.
> The synchronization is set to occur every hour.
> And, translations are pushed to the`l10n_main`branch, not the`main`branch.
> (In French case,[https://github.com/carpentries-incubator/bioc-intro/tree/l10n_main/locale/fr](https://github.com/carpentries-incubator/bioc-intro/tree/l10n_main/locale/fr))

**Kozo Nishida** (04:45:49) (in thread):
> Hi@Laurent GattoI added[https://github.com/carpentries-incubator/bioc-intro](https://github.com/carpentries-incubator/bioc-intro)`main`branch to[bioconductor.crowdin.com](http://bioconductor.crowdin.com)to sync with the Crowdin English source text.
> I believe the latest commit on GitHub is now synced with Crowdin. If it's not, please let me know.
> The synchronization is set to occur every hour.
> And, translations are pushed to the`l10n_main`branch, not the`main`branch.
> (For example,[https://github.com/carpentries-incubator/bioc-intro/tree/l10n_main/locale/fr](https://github.com/carpentries-incubator/bioc-intro/tree/l10n_main/locale/fr)is the link for French.)

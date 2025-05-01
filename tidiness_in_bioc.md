# Archive: #tidiness_in_bioc

## 2025-04-01

**stefano mangiola** (08:20:48):
> If someone would like to lead a tidyomics workshop at the Galaxy Bioconductor Community Conference (GBCC), e.g. about bulk RNA/singlecell/spatial multiomics, please submit today.
> 
> I would have proposed it, but apparently, only one abstract per person can be submitted (@Maria Doyle?), and I believe the abstract form is now inaccessible to me. There will be plenty of tidyomics members who can support you at the event.
> 
> Don't feel you need a lot of experience.

**stefano mangiola** (08:21:11) (in thread):
> If someone would like to lead a tidyomics workshop at the Galaxy Bioconductor Community Conference (GBCC), e.g. about bulk RNA/singlecell/spatial multiomics, please submit today.
> 
> I would have proposed it, but apparently, only one abstract per person can be submitted (@Maria Doyle?), and I believe the abstract form is now inaccessible to me. There will be plenty of tidyomics members who can support you.
> 
> Don't feel you need a lot of experience.

**stefano mangiola** (08:21:32) (in thread):
> If someone would like to lead a tidyomics workshop at the Galaxy Bioconductor Community Conference (GBCC), e.g. about bulk RNA/singlecell/spatial multiomics, please submit today.
> 
> I would have proposed it, but apparently, only one abstract per person can be submitted (@Maria Doyle?), and I believe the abstract form is now inaccessible to me. There will be plenty of tidyomics members who can support you at the event.
> 
> Don't feel you need a lot of experience.

**Michael Love** (08:48:38):
> ~~~Justin and I are planning a long workshop to briefly demo tidyomics in general (tidySE, plyranges) and then get into some of plyxp’s unique aspects like group_by summarize.~~~~~~I think there is plenty of space for another workshop from tidyomics. E.g. if you have a particular domain / dataset of interest. I’m happy to help craft workshop material with anyone.~~~

**stefano mangiola** (08:52:13):
> Amazing! The issue is that the deadline is today, hopefully we can find someone from the community. I have already submitted an abstract for cellNexus:disappointed:

**Michael Love** (08:52:38):
> they extended to next week

**Michael Love** (08:52:58):
> “we will be extending the deadline by one week due to requests received”

**Michael Love** (08:53:15):
> Stefano you will be in person?:raised_hands:

**Jenny Drnevich** (10:08:06):
> The abstract deadlines are for 10 min talks and posters only. We sent out a survey for the longer 45 min workshops for what people wanted to see and who was interested in teaching a workshop. The "deadline" was March 21, but it looks like it's still open:[https://forms.gle/i34Ag8SHMtBAmpPh7](https://forms.gle/i34Ag8SHMtBAmpPh7). We haven't made any decisions yet, but there were already a few more than the number of slots. However, the submissions were heavily Galaxy-biased (this is how they do workshops) so Bioc ones might get more preference (can't promise anything).
  - Attachment (Google Docs): [Expression of interest for GBCC2025 training topics](https://forms.gle/i34Ag8SHMtBAmpPh7)

**Jenny Drnevich** (10:10:45):
> Galaxy usually pushes "posters", even those selected for a talk are encouraged to also do a poster. They often have people with laptops giving demos at the poster sessions. Just another avenue for getting your tidyomics stuff out...

**Jenny Drnevich** (10:11:01) (in thread):
> Galaxy usually pushes "posters", even those selected for a talk are encouraged to also do a poster. They often have people with laptops giving demos at the poster sessions. Just another avenue for getting your tidyomics stuff out...

**Jenny Drnevich** (10:12:58):
> @Michael LoveI don't see Justin's or your name on the survey for leading a training session...

**Michael Love** (10:32:31):
> We were going to submit yesterday but then with the extension we are honing the submission

**Michael Love** (10:32:37) (in thread):
> We were going to submit yesterday but then with the extension we are honing the submission

**Michael Love** (10:33:26):
> I got tripped up with the registration bc that means I have to submit a complete expense request and wait for approval, but then i realized there is a way to not pay by card right now

**Michael Love** (10:34:33):
> oh i see. well maybe we will go for a talk then

**Michael Love** (10:35:50):
> this is what made me think abstracts would be considered for workshops
  - File (PNG): [Screenshot 2025-04-01 at 10.35.37 AM.png](https://community-bioc.slack.com/files/U34P8RS3B/F08LBEQ4V1S/screenshot_2025-04-01_at_10.35.37___am.png)

**Michael Love** (10:37:20):
> i think we will just go for a talk this year

**Jenny Drnevich** (10:37:22):
> That's CSHL's boilerplate abstract text. We haven't had a lot of luck getting them to change their standard text, like including you don't need to pay a down payment to register.

**Jenny Drnevich** (10:39:02):
> [conference planning jointly between Galaxy, BioC and CSHL has been a lot more complicated this year as each one has a different standard way of doing things!]

**Michael Love** (10:39:58):
> understand and thank you for organizing!

**Michael Love** (10:40:14) (in thread):
> ~~~Justin and I are planning a long workshop to briefly demo tidyomics in general (tidySE, plyranges) and then get into some of plyxp’s unique aspects like group_by summarize.~~~~~~I think there is plenty of space for another workshop from tidyomics. E.g. if you have a particular domain / dataset of interest. I’m happy to help craft workshop material with anyone.~~~

**Jenny Drnevich** (10:41:28) (in thread):
> What page was this on?

**Michael Love** (10:42:33) (in thread):
> scientific program

**stefano mangiola** (19:25:03) (in thread):
> Yes! Looking forward to meet you all!


## 2025-04-03

**Kozo Nishida** (11:17:59):
> I'm planning to visualize data using`tidyplots`for each`rowData`group in`SummarizedExperiment`.
> The x-axis represents each`colData`group, and the y-axis corresponds to the`assays`values.
> In this case, do you think it’s best to convert`SummarizedExperiment`into a`tibble`using`tidySummarizedExperiment`?
> I’d appreciate your thoughts—such as whether it might be better to use a different package that doesn’t require converting`SummarizedExperiment`into a`tibble`.

**stefano mangiola** (19:16:51) (in thread):
> `tidySummarizedExperiment`can be piped directly into ggplot. If you are interested in specific features/genes, you can do
> 
> se |> filter(...) |> ggplot(...)

**stefano mangiola** (19:17:20) (in thread):
> `tidySummarizedExperiment`can be piped directly into ggplot. If you are interested in specific features/genes, you can do
> 
> se |> filter(...) |> ggplot(...)

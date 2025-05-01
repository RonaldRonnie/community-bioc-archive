# Archive: #developers-forum

## 2025-03-31

**Shian Su** (19:57:36):
> So I vibe-coded my way into a working minimap2 interface for R, thoughts on whether this is a viable project?[https://github.com/Shians/minimap2-ai-r](https://github.com/Shians/minimap2-ai-r)

**Shian Su** (19:57:38) (in thread):
> So I vibe-coded my way into a working minimap2 interface for R, thoughts on whether this is a viable project?[https://github.com/Shians/minimap2-ai-r](https://github.com/Shians/minimap2-ai-r)

**Shian Su** (19:58:23):
> I need to decide if I want to pay for Cursor since I'm now out of free tokens.:cry:

**Kasper D. Hansen** (20:02:34):
> I don't know. I could see the appeal for teaching for example. I have always aligned in a separate process.

**Kasper D. Hansen** (20:02:46):
> I would look into whether people are using Rbowtie

**Kasper D. Hansen** (20:03:06):
> That seems to me to have a similar potential usecase

**Kasper D. Hansen** (20:03:56):
> ... so basically you should ignore my comment since I am clearly not the target audience, but you should look into Rbowtie

**Dirk Eddelbuettel** (20:21:32) (in thread):
> Micro-comment from glancing at your DESCRIPTION: You do not need SytemRequirements: C++11 (unless you plan compilation on ancient R versions) because C++11 has been the minimum for several years and it is already C++14 with R 4.4.* (and maybe even R 4.3.*).

**Shian Su** (20:22:13):
> Thanks for pointing me to Rbowtie, they actually have a very interesting approach of compiling the binary and using`system.file`to find the binary and`system`to call it. That's actually 1000x simpler than me trying to work out how to use minimap2's C interface (with heavy AI assistance). How does one smuggle a binary from the src area out into inst?

**Shian Su** (20:24:06) (in thread):
> Thanks Dirk, the majority of this code is AI generated as an experiment over the weekend. I appreciate experienced eyes checking over it for obvious issues. My goal was simply to make it generate alignments identical to the output of the CLI tool.

**Dirk Eddelbuettel** (20:25:49) (in thread):
> I always have to look it up but WRE under R 4.4.3 says
> > **C++ standards**: From version 4.0.0 R required and defaulted to
> C++11; from R 4.1.0 in defaulted to C++14 and from R 4.3.0 to C++17
> (where available).  For maximal portability a package should either
> specify a standard (*note Using C++ code::) or be tested under all of
> C++11, C++14 and C++17.

**Shian Su** (20:27:01) (in thread):
> Is it preferable to specify C++17 or remove it entirely?

**Dirk Eddelbuettel** (20:27:36) (in thread):
> As for the 'can I smuggle a binary in': leads to the usual problem of 'will it run everywhere' etc but I have an example for that too---time-series seasonal adjustement (eg in package`seasonal`) uses a binary provided by the US Commerce Department (so free for everybody) but shipped as a binary.  We created a wrapper`x13binary`that`seasonal`depends upon.  You could borrow that model.  Both are on CRAN, and we have an RJournal paper on the approach.

**Dirk Eddelbuettel** (20:28:41) (in thread):
> > Is it preferable to specify C++17 or remove it entirely?
> The recommendation (and by now check from`R CMD check`) is to remove entirely**unless you need a feature that only C++11 had**so just leaving it 'open' and 'relaxed' is best.  The compiler knows what to do.

**Dirk Eddelbuettel** (20:28:57) (in thread):
> As for the 'can I smuggle a binary in': leads to the usual problem of 'will it run everywhere' etc but I have an example for that too---time-series seasonal adjustement (eg in package`seasonal`) uses a binary provided by the US Commerce Department (so free for everybody) but shipped as a binary.  We created a wrapper`x13binary`that`seasonal`depends upon.  You could borrow that model.

**Dirk Eddelbuettel** (20:29:18) (in thread):
> As for the 'can I smuggle a binary in': leads to the usual problem of 'will it run everywhere' etc but I have an example for that too---time-series seasonal adjustement (eg in package`seasonal`) uses a binary provided by the US Commerce Department (so free for everybody) but shipped as a binary.  We created a wrapper`x13binary`that`seasonal`depends upon.  You could borrow that model.  Both are on CRAN, and we have an RJournal paper on the approach.

**Shian Su** (20:29:49) (in thread):
> I have the full source code, so I'd be compiling the binary on the target machine, the only smuggling is from src where it'd normally be built into inst, and I'm not sure if there's a standard way to do that or I just do some`../../inst/bin`shenanigans in the Makefile.

**Dirk Eddelbuettel** (20:30:13) (in thread):
> No a local binary, made at install time, is fine. You control the path!  Function`system.file(..., package="mypackage")`is your friend.

**Shian Su** (20:30:36) (in thread):
> I have the full source code, so I'd be compiling the binary on the target machine, the only smuggling is from src where it'd normally be built into inst, and I'm not sure if there's a standard way to do that or I just do some`../../inst/bin`shenanigans in the Makefile.

**Dirk Eddelbuettel** (20:30:54) (in thread):
> No a local binary, made at install time, is fine. You control the path!  Function`system.file(..., package="mypackage")`is your friend.

**Dirk Eddelbuettel** (20:32:01) (in thread):
> (For seasonal we decided to decouple as`x13binary`is released less often. So the binary, made at install or build time, lives there.`seasonal`calls it.  Same thing otherwise.)

**Dirk Eddelbuettel** (20:32:09) (in thread):
> (For seasonal we decided to decouple as`x13binary`is released less often. So the binary, made at install or build time, lives there.`seasonal`calls it.  Same thing otherwise.)

**Shian Su** (20:37:16):
> In terms of use-case, the first motivation is for FLAMES which currently has to grab minimap2 via basilisk to make the pipeline installation more user friendly in terms of installation. The second motivation is I want to one day get into some real-time long-read processing using R, whereby reads streaming off a Nanopore sequencer can be processed in real time to compute statistics and make decisions. This is step 1 towards that because through the C interface I can keep the built index in memory as batches of new reads stream in, essential for real-time processing.

**Shian Su** (20:38:44) (in thread):
> Thanks,`cp bin/minimap2 ../../inst/bin`it is then, very straightforward.

**Dirk Eddelbuettel** (20:39:49) (in thread):
> "In theory, yes. In practice there will be hickups."  Just kidding.

**Shian Su** (21:28:57) (in thread):
> So far it seems to be working, it’d be cool to turn this intoanear-zero maintenance package that just rebuilds with each release of minimap2 via GitHub action.


## 2025-04-02

**Tim Triche** (12:21:19) (in thread):
> hey@Peter(Yizhou) Huangthis could be helpful for you

*12:21:23 - @Peter(Yizhou) Huang has joined the channel*
**Tim Triche** (12:22:16) (in thread):
> this is pretty slick! vibe coding for the win

**Peter(Yizhou) Huang** (13:46:01) (in thread):
> I guess it would be super handy in bam-slicing case, when we sliced target regions from genomic BAMs -> covert to fastq -> aligned against transcript reference using minimap2 all together in R environment.

**Tim Triche** (13:53:11) (in thread):
> :100:

**Shian Su** (18:17:22) (in thread):
> This was my first experience with agentic models that did multi-file edits with controllable context. I decided to try problems at 3 levels of difficulty.
> 
> The first was just simple implementation of an S4 class along with unit tests, it had errors in the unit test because the coding LLM is still bad at maths and couldn’t correctly calculate the number of rows in the matrix that it declared. Easy fix and the rest was perfectly functional. Iteratively asking it to implement more methods and calculate internal invariants was fun, particularly invariants because those need to be updated on any mutating method and it’s easy to miss when coding manually.
> 
> The second attempt was to do something I had almost zero understanding of. I wanted a web app todo list with a hierarchical task structure, dependencies and automation. It produced a surprisingly decent initial product, but the second it broke and I didn’t have the technical skills to debug it became an unrecoverable mess. LLMs at this stage is not capable of effective debugging of its own code.
> 
> So the third attempt was this. I know that it’s absolutely possible in principle because we already have things like Rsamtools. I know that it shouldn’t be overly complex because the code in the Python bindings look quite simple. I had no idea how to actually build C code into a shared library to call with Rcpp. The biggest time sink was actually getting it all to compile on my ARM Mac. Minimap2 makes heavy use of SSEinstructions from x86 and it took a lot of trial and error with the Makevars to get it to work. But it was great to have the LLM set up 95% of the code for me to focus on the hard problems. It also required that I had already wasted sufficient portions of my life dealing with compiler errors to resolve the issues that came up.
> 
> Overall 8 out of 10:robot_face:. Would vibe code again.

**Shian Su** (18:19:58) (in thread):
> I’m not going to sign up to Cursor, since I already have a GitHub copilot subscription and VS Code already has these features in their preview release.

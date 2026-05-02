# GitHub 2026 可靠性危机：故障、AI agents 与开发者信任

- BestBlogs URL: https://www.bestblogs.dev/video/297a3b9
- Extraction: DOM text from BestBlogs page
- Extracted chars: 10646
- Original publisher URL: https://www.youtube.com/watch?v=d53Zk28esmU

---

VIDEO
84
GitHub is having some major issues right now…

Fireship 梳理 GitHub 在 2026 年 4 月的可靠性危机，包括 outages、merge queue 事故、安全事件、Mitchell Hashimoto 离开，以及 agentic AI development workflows 对基础设施造成的压力。

Fireship
关注
·
昨天
·
8 个章节
·
查看原文 →
GitHub 2026 可靠性危机：故障、AI agents 与开发者信任
章节导览
8 个章节
CH.1
GitHub's Growing Reliability Crisis
00:00
CH.2
The Rise of the 'Facebook for Code'
00:51
CH.3
The 2026 Uptime Crisis
01:54
CH.4
A Week of Disastrous Failures
02:18
CH.5
Mitchell Hashimoto's Breakup with GitHub
03:05
CH.6
AI Agents and Infrastructure Strain
03:51
CH.7
Exploring GitHub Alternatives
04:44
CH.8
High Impact Careers and Conclusion
05:05
📝 实时字幕
跟随播放
全部字幕
00:00
1

it's 10 p.m Do you know where your children are i don't know where mine are because I'm too busy

00:04
1

working on pushing commit final final v2 actual fix to GitHub Unfortunately if you're one of the 100 million plus

00:10
1

developers who use GitHub you may have encountered a message like this recently or maybe all of your pull requests

00:16
1

just disappeared completely or maybe the search returns nothing or your continuous integration actions just hang in the void GitHub

00:23
1

is easily the most important website in software engineering But more and more developers are yelling at it and in

00:28
1

some cases literally crying like it's a broken vending machine that ate their last dollar Well finally yesterday things hit

00:34
1

the point of no return after legendary developer Mitchell Hashimoto did the unthinkable He packed up his open- source project

00:41
1

Ghosty and is leaving GitHub for good in search of greener pastures Um and this fall I'm going to take

00:46
1

my talents to South Beach In today's video we'll find out what the hell happened to GitHub and why It

00:51
1

is April 30th 2026 and you're watching the code report In 2008 GitHub was built with Ruby on Rails as

00:58
1

an online platform to manage your software source code with a relatively new technology called Git which is the version

01:04
1

control system built by Linus Torvalds in 2005 to manage the source code of Linux The pitch was simple It

01:10
1

take the command line nightmare your senior engineer keeps yelling about it Give it a web UI make it like

01:15
1

Facebook for code and suddenly every developer on Earth has a public coding profile It worked so well that by

01:21
1

2018 Microsoft bought it for $7.5 billion Today it hosts over $420 million failed side projects and effectively is the

01:30
1

public record of software If it isn't on GitHub it might as well not exist Developers use it to store

01:35
1

code track bugs through issues propose changes through pull requests run tests and deployment through GitHub actions while also functioning

01:43
1

as a social network and resume for developers All duct taped to a Git server which is exactly why it

01:49
1

breaking is such a problem and the main reason developers are big mad at GitHub right now is uptime or

01:54
1

lack thereof But let's check the actual receipts According to thirdparty monitoring GitHub uptime in 2025 dipped below 90% and

02:02
1

April 2026 is tracking around an abysmal 86% For context AWSS3 promises 11 9 and GitHub is currently operating at

02:12
1

just 1 n However the official GitHub status page would beg to differ and reports uptime well above 99% for

02:18
1

all services Regardless the previous week on GitHub was a disaster On April 23rd the Merge Q quietly unmerged 292

02:23
1

pull requests across 658 repos In other words the platform whose entire job is to not lose your code just

02:34
1

lost your code Damn it's gone Then on April 27th GitHub's elastic search subsystem was hit by a botnet that

02:41
1

took down GitHub search for hours And then on April 28th GitHub was forced to publish two blog posts the

02:46
1

same morning One was the CTO apologizing for reliability while the other was about a critical remote code execution vulnerability

02:54
1

where Git push could literally execute code on GitHub servers A few big projects like Zigg have already migrated away

03:00
1

from GitHub but then shit really hit the fan when Mitchell Hashimoto dropped this blog post He's the creator of

03:05
1

tools like Vagrant and Terraform which are part of his company Hashi Corp which was taken public and made him

03:10
1

extremely rich Despite having enough money to own his own private jet he still bangs out code daily building a

03:16
1

terminal emulator called Ghosty He joined GitHub in 2008 as user number 1,299 and is logged in almost every single

03:23
1

day for 18 years But on April 28th he wrote a breakup letter while literally crying Speaking of GitHub he

03:29
1

said quote "I want to ship software and it doesn't want me to ship software." That line hits hard and

03:35
1

he says he kept a journal for a month and put an X next to every day a GitHub outage

03:40
1

blocked his work and almost every day got an X at this point He's had enough and his 50,000 star

03:45
1

GitHub project Ghosty is leaving the platform for good That's a massive vibe shift but who can we get blamed

03:51
1

for this well it's easy to point the finger at Microsoft because it's literally their sole responsibility to make this

03:56
1

website work But I actually know people who work at GitHub and believe they're trying The key to success is

04:03
1

developers developers developers developers developers developers developers developers developers When they acquired GitHub back in 2018 it actually got better

04:13
1

in the years that followed with features like actions code spaces etc But now in the AI coding era the

04:19
1

initification is real A GitHub CTO admits in writing that since 2025 agentic development workflows have accelerated sharply which translated

04:28
1

into English means that AI agents are hammering GitHub like it's a free buffet A GitHub isn't just a host

04:33
1

for developers anymore It's a host for their replacement In the same way Bill Gates saved the world from CO

04:38
1

19 I have faith Microsoft will turn the GitHub ship around But if they don't there are alternatives out there

04:44
1

You've got the reliable but boring GitLab you've got the German nonprofit Codeberg and you've got the minimal Source Hut

04:50
1

which has zero AI features whatsoever and many other viable platforms ready to reap the benefits of GitHub's downfall That

04:56
1

that means the good news is that if you make the mistake of choosing to become a programmer as a

05:00
1

career there will always be a home for your code But did you realize you have 80,000 hours in your

05:05
1

career 40 hours per week 50 weeks per year for 40 years That's a lot of time to make a

05:10
1

positive impact on the world And 80,000 hours the sponsor of today's video can help you do that If you're

05:16
1

young you've probably heard advice like "Follow your passion do what you love and take the initiative." But these cliches

05:22
1

are not based on evidence or data Unlike the work of 80,000 hours which is a nonprofit that for the

05:28
1

last 10 years has been researching the question of how do you find a fulfilling career that does good too

05:34
1

their website has tons of collected research on high impact careers along with job boards podcasts and a lot more

05:41
1

It's an incredible resource for anyone looking to start a high impact career or make a switch mid-career Join the

05:46
1

newsletter today to get a free copy of their in-depth career guide sent to your inbox It could be the

05:51
1

catalyst that changes your direction in life that this has been the code report Thanks for watching and I will

05:56
1

see you in the next one

点击任意行跳转 · 悬停可向 AI 提问

内容简介
GitHub's 2026 Meltdown: Reliability Crisis and the AI Surge

GitHub, the platform that has served as the bedrock of software engineering since its inception in 2008, is currently navigating its most turbulent period to date. As of April 2026, the developer community is reporting record levels of frustration due to a series of outages, data losses, and security vulnerabilities that have shaken the industry's trust in Microsoft's $7.5 billion acquisition.

The Reliability Gap

While GitHub's official status page remains optimistic, reporting uptimes above 99%, third-party monitoring tools paint a far grimmer picture. In April 2026, the platform's actual uptime dipped to an estimated 86%. To put this in perspective, standard cloud services like AWS S3 aim for "11 nines" of durability, whereas GitHub is struggling to maintain even one.

Recent failures include:

Data Loss: On April 23rd, the Merge Queue system accidentally unmerged 292 pull requests across over 600 repositories.
Infrastructure Attacks: A botnet attack targeted GitHub's Elastic Search subsystem, disabling search functionality for hours.
Security Risks: A critical remote code execution (RCE) vulnerability was discovered where a simple git push could potentially execute malicious code on GitHub's own servers.
The Hashimoto Departure

Perhaps the most symbolic blow to the platform was the departure of Mitchell Hashimoto. As the creator of Vagrant and Terraform and a GitHub user since 2008, Hashimoto represents the core demographic of the platform. After documenting a month of daily outages that blocked his work on the Ghosty terminal emulator, Hashimoto officially moved his 50,000-star project off the platform, stating, "I want to ship software and it [GitHub] doesn't want me to ship software."

The AI Factor: "Initification"

The root cause of these stability issues appears to be the transition into the AI coding era. GitHub's CTO has acknowledged that the rise of agentic development workflows—where AI agents autonomously interact with repositories—has placed unprecedented strain on their infrastructure. Essentially, AI agents are hammering the platform's servers at a frequency and scale that human developers never could, leading to what some are calling the "initification" of the service.

Looking for Alternatives

As the "vibe shift" continues, many developers are looking toward alternative platforms:

GitLab: The primary established competitor, known for being feature-rich if slightly more complex.
Codeberg: A German non-profit alternative gaining traction among open-source purists.
Source Hut: A minimal, AI-free platform focused on speed and simplicity.

While Microsoft has a history of turning around struggling products, the current state of GitHub serves as a reminder that even the most essential tools in the software ecosystem are not invincible.

00:00 / 00:00
1x

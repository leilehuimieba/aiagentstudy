# Claude Code 非技术用户完整指南

- BestBlogs URL: https://www.bestblogs.dev/video/367df0d
- Extraction: DOM text from BestBlogs page
- Extracted chars: 52404
- Original publisher URL: https://www.youtube.com/watch?v=bqJzIWAEn40

---

VIDEO
86
The Ultimate Non-Technical Guide to Claude Code

Futurepedia 面向非技术用户系统演示 Claude Code，覆盖桌面应用、Plan Mode、迭代 prompting、claude.md 上下文、MCP connectors、GitHub、Vercel 部署、skills、安全审查和简单应用项目。

Futurepedia
关注
·
昨天
·
14 个章节
·
查看原文 →
Claude Code 非技术用户完整指南
章节导览
14 个章节
CH.1
What is Claude Code?
00:21
CH.2
Interface Options
01:11
CH.3
Pricing and Usage
02:22
CH.4
First Build: Cube Tacto
03:24
CH.5
Iteration Process
07:30
CH.6
Context Management
10:55
CH.7
Model Selection
13:46
CH.8
Parallel Building
15:12
CH.9
MCPs and Connectors
21:02
CH.10
Building Morsel
24:40
CH.11
GitHub Integration
30:05
CH.12
Skills and Security
34:26
CH.13
Deployment with Vercel
36:52
CH.14
Mobile App Experience
39:43
📝 实时字幕
跟随播放
全部字幕
00:00
1

i made this video to be the most comprehensive non-technical guide to Claude Code in existence to do that I'll

00:07
1

go step by step creating six different projects and explaining every concept along the way we'll build a website a

00:14
1

game a Chrome extension an automation that connects external tools and a mobile app with AI vision all without touching

00:21
1

a single line of code we'll start at the beginning what is cloud code cloud code is an agentic coding

00:30
1

tool that handles entire development workflows through natural language you tell it what you want a website a game a

00:37
1

mobile app a dashboard a web scraper then it makes a plan generates the code tests it debugs it and

00:44
1

delivers it if you've used Lovable Base 44 or built something right inside Chat GBT or Claude you already know

00:50
1

how this feels you describe what you want it builds it cloud code works the same way the difference is

00:55
1

where it runs cloud code works directly on your computer it can create files edit them and build things locally

01:02
1

this gives you much more power and control and cheaper cost at scale there are three main ways to use

01:11
1

Cloud Code the first is the desktop app you download it like any other app and inside there are three

01:16
1

tabs on the left a chat tab which is the regular cloud experience a co-work tab which I've done a

01:22
1

full video on and then the code tab that's where we'll be working you type what you want it starts

01:27
1

building it's really as easy as that to get started i'll show that in just a second the second option

01:32
1

is the terminal the textbased interface that Cloud Code is actually running through under the hood regardless of which option

01:38
1

use some people prefer to work here directly especially if they have a technical background the third is an

01:44
1

IDE which stands for integrated development environment it looks intimidating but the main advantage is as Cloud builds every file

01:51
1

it creates shows up in a panel on the side so you can see exactly what's being made and edits

01:57
1

that happen it just requires a bit more setup to get going but it is a great middle ground if

02:01
1

you want to move there after mastering everything in this video i'm showing you all three because if you watch

02:06
1

other tutorials they may be working from the terminal or an IDE so now you'll know what you're looking at

02:11
1

but for this video we're staying in the desktop app the latest update that just came out the other day

02:16
1

added a lot it is the fastest way to get building and most people won't need the added layers the

02:22
1

other options have to use Claude Code you need a paid Claude subscription the free plan doesn't include it if

02:30
1

you're just getting started the Pro at $20 a month is what I'd recommend you may already have it see

02:34
1

how things go then upgrade if needed if you're doing heavy frequent builds you'll eventually want to move to the

02:40
1

$100 a month max plan that gives you significantly more usage but for learning experimenting and building personal tools Pro

02:47
1

is plenty one thing to know is usage resets every 5 hours so if you hit a limit mid- project

02:55
1

you're not locked out for long and there also is a weekly cap and that can get confusing sometimes you

03:00
1

can always check under settings and then usage to see where you're at along the way we'll get into the

03:07
1

different modes memory files slash commands MCPs setting up GitHub and deploying what you build to the web i will

03:15
1

cover a lot of ground but none of this is super complicated i'll walk through each piece as it comes

03:20
1

up before any of that I want to show you how easy it is to just get started so let's

03:24
1

build something i'm on the code tab now each project you create needs a folder to live in on your

03:31
1

computer this is where Claude will work create files and make edits this button lets you select an existing folder

03:38
1

or create a new one i have a folder called Cloud Code projects for this video and I'll create a

03:42
1

new subfolder for each build this one is called Cube Tacto i wanted to start with something fun there are

03:48
1

more practical builds coming later here's my prompt create a playable browser game that combines a 3x3 Rubik's cube with

03:55
1

tic-tac-toe on each turn the active player first places their mark on an empty sticker on the cube after placing

04:01
1

their mark that player must make exactly one standard move of the cube and victory is checked after the rotation

04:07
1

is completed not after placing the mark so just the idea and a few rules that's it but before sending

04:12
1

I'll switch the mode to plan mode instead of jumping straight into building Cloud will first map out the plan

04:18
1

for how it's going to implement everything it will ask clarifying questions if it needs them and I can review

04:24
1

the whole plan before anything gets built for any initial prompt I always go to plan mode first i'll send

04:30
1

it trust the workspace which is just the folder I gave it to work in and then Claude starts planning

04:35
1

and it usually will come back with a few questions this first one is about which types of moves to

04:40
1

allow i actually don't want any of the options it suggested so I'll type what I want in the other

04:44
1

box then for the draw condition I'll go with the recommendation same with the type of markings for the X's

04:50
1

and O's then that's all it needed couple minutes later the full plan is ready it's got the text stack

04:56
1

bio layout geometry move types animations everything you can read through whatever you want clarity on if something doesn't look

05:04
1

right you can tell Claude in the prompt box or add notes right onto the plan and it will revise

05:08
1

just fine-tune whatever you want before it starts building once you're happy with it click accept and allow edits and

05:14
1

it will get to work and over on the right there's different panels and view options the preview panel is

05:20
1

open and it's still showing the plan you can resize open and close what you want i don't need the

05:25
1

plan anymore and near the start of a build it will ask for various permissions there is a setting to

05:29
1

skip these but especially when you're new you'll typically be here anyways and can just approve what comes up most

05:35
1

of the requests happen right at the beginning then it runs on its own and you can go do something

05:40
1

else i usually have it going on one monitor while I work on another i will cut out the wait

05:44
1

times throughout the video planning takes a couple minutes and building can take 5 to 15 minutes depending on the

05:50
1

complexity even more if it's really complex so I'll come back when it's done so just from that one prompt

05:55
1

and answering a few questions it had it built the full working prototype before I test it let me show

06:00
1

you what actually happened after I approved the plan it updated to-dos created a file and used a tool then

06:07
1

it updated the to-dos worked on the game logic created another file then it ran two commands created a file

06:13
1

edited a file used five tools you can open these up to see further details on each step so I

06:19
1

kept going editing files using tools and when I open this you can see it actually used the preview on

06:24
1

its own placed a mark then tested a move verified that it worked correctly then went back to clean up

06:30
1

the debug code so it not only created the plan and built the whole game using tools and creating files

06:36
1

along the way but it also tested the game out for itself if something wasn't working it would change the

06:42
1

plan and go back into the code to see what went wrong then fix it then test again until it

06:46
1

was working properly all before sending it to me if this is your first time using it that's pretty mind-blowing

06:52
1

you get used to it fast and start getting annoyed if everything doesn't go perfectly but I think it's good

06:57
1

to just stop and appreciate what's happening every once in a while this was unthinkable not too long ago all

07:02
1

right let me test it myself let's load it right in the preview window i can place a mark click

07:08
1

a button to rotate and drag it around to see different angles i'll play through a few moves to get

07:15
1

a winner really quick and perfect all the core functionality working from one simple prompt there are definitely things I

07:22
1

want to change but the foundation is solid now we iterate this is a big part of the process figure

07:30
1

out what works or doesn't work functionally what you like or dislike aesthetically and then refine it until it's exactly

07:36
1

what you want we do this all through prompting for most changes a simple follow-up prompt is all it takes

07:41
1

the biggest recommendation I'll give is go one change at a time if you throw a bunch of requests in

07:46
1

at once it's less likely to get everything right the changes can interact with each other in unexpected ways one

07:52
1

at a time means if something breaks you know what caused it so here's the first change I want to

07:56
1

make i can't tell which layer is going to rotate before pressing a button when hovering over one of the

08:01
1

buttons add a glow to the corresponding layer as well as arrows to indicate which direction it will rotate that

08:06
1

should do the trick and as you can see I'm no longer on plan mode i have it on accept

08:11
1

edit you can switch back to plan mode at any time if you need it to really think through a

08:16
1

big change or new feature but most of the time I'll just be prompting from here i described the problem

08:21
1

described what I wanted and that's it about a minute later it's done i will open the preview place a

08:26
1

mark then hover over a button and that is a lot more clear what's going to happen i want a

08:34
1

big change now this isn't very fun when I'm playing both sides so I'll say add an option for an

08:39
1

AI opponent after player one's turn player two is an AI that automatically makes a move i'll just send it

08:45
1

like that then again it took around 1 minute to make the change and it looks like it added a

08:50
1

box up top to check to switch to the AI version and that is working perfectly so this is really

08:57
1

cool but turns out this is way too easy now that I'm actually playing it so I need to change

09:01
1

the gameplay logic i'll make it so that after you make a mark it's the opponent that makes the rotation

09:06
1

and that rotation has to include the sticker you made the mark on i'm going to send that then I

09:11
1

actually have more changes I know I'll want to make instead of making you sit through that back and forth

09:15
1

I'll just do all that then come back and summarize it all right I'll just do a quick run through

09:19
1

of these changes the new gameplay logic was much more fun i made it so you can still rotate the

09:25
1

cube after the game is over then I had it add a red line through the winning move then I

09:29
1

didn't like that you could see the hidden arrows and asked it to olude them naturally same thing with the

09:34
1

red line then it was really hard to win so I asked it to add three levels of difficulty then

09:40
1

medium was still too hard i had it make that slightly easier but that was it just continuing the same

09:45
1

process we've covered and you can see it was a simple prompt every time and now honestly the game is

09:50
1

really fun to play medium is still pretty hard but I did win a couple times i haven't spent the

09:56
1

time to win on hard mode yet i don't know if I'd even be able to but overall this turned

10:00
1

out awesome and that was the point of this first build you really can just jump in describe what you

10:05
1

want and build something real and fun so already you'll be able to build a custom dashboard a personal tool

10:11
1

replace a paid subscription we will get into a lot more features and ways to have more control but with

10:16
1

just plan mode prompt iterate you can build out stuff that would have seemed impossible a couple years ago and

10:22
1

hopefully that makes this seem less intimidating if this is your first time seeing it if you want to use

10:27
1

claude code for marketing work we've got a free guide for you it has four workflows and 12 prompts you

10:32
1

can copy paste to go from idea to finished product in a single session things like building a lead magnet

10:38
1

or testing a positioning angle the same day you think of it you can even launch a campaign without writing

10:43
1

a single line of code if you don't know exactly what to build after watching this video this has real

10:48
1

world use cases that are easy to get started with that's free just click the link in the description one

10:55
1

more thing to cover before we move to the next project context management and memory so after a few back

11:00
1

and forths there's a lot of history in this chat and Cloud uses all of that as context but the

11:05
1

context window is limited you can hover over it at any time to see how full it is but as

11:09
1

you approach that limit Claude can compact the conversations it reviews the history and tries to preserve the most important

11:16
1

information so it's not carrying everything forward the problem is it's not a perfect process details get dropped nuance can

11:23
1

get lost and over time the quality of Claude's understanding can drift the better move is to start a fresh

11:29
1

session the downside is Claude won't have any of that conversation history it will only know what's in your project

11:34
1

folder so there are two steps that make that handoff smooth the first step is creating a claude.md file that's

11:43
1

a permanent reference document that holds everything Claude needs to know about a project long term the rules the tech

11:49
1

stack the architecture API references or any preferences you want it to follow consistently to create it hit forward slash

11:57
1

that pulls up a list of commands and skills there's a lot in here batch for making large scale changes

12:03
1

in parallel compact for summarizing conversation history there's debug and a lot more each one has a short description it

12:10
1

is worth browsing through so you know what's available you won't use most of them but a few will come

12:14
1

up regularly the one we want is called init just type it and send then claude knows what to do

12:19
1

it will go through your project folder and generate the claude.md file automatically and as you keep building you can

12:25
1

ask it to update the file whenever something significant changes i'll pull up the folder so you can see what's

12:30
1

in there now so here's all the files Claude has created so far there's useful information in these but not

12:36
1

everything it would need in a fresh session that's what the CloudMD is for just finished and you can see

12:40
1

the new file has just popped in i'll open it up and right at the top it says "This file

12:45
1

provides guidance to Claude Code when working with code in this repository." Then there's a full breakdown of the project

12:50
1

everything it would need as a starting point but there's one thing it won't capture where you left off it

12:56
1

won't know which feature you were in the middle of or what decisions you just made and what's still on

13:00
1

the list so before starting a new session send this prompt summarize everything important about this project the architecture decisions

13:07
1

we made current state and what's left to do so I can paste it into a new session then start

13:12
1

a fresh session point it to the same folder and paste that answer in claude reads that claude.mmd file automatically

13:19
1

at the start of every new session so it will have all the permanent context then your summary tells it

13:24
1

where you left off those two things give it everything it needs to keep building without missing a beat so

13:29
1

one project down and that was really easy but right now it only lives on my computer later in the

13:34
1

video I'll deploy it so anyone can access it online i'll even link it in the description so you can

13:39
1

actually play it yourself and I will only use free tools to do that one more thing to understand before

13:46
1

we get building again which model to use and how that affects your token usage claude Code gives you three

13:52
1

main models to choose from haiku Sonnet and Opus the number at the end will change over time and at

13:57
1

some point the name might change too they have varying levels of capability but more capability means more tokens so

14:04
1

you want to match the model to the task now Haiku is fast and really light on tokens but it's

14:11
1

not powerful enough for serious building sonnet is strong and it's capable enough for a lot of work and it's

14:16
1

significantly more token efficient than Opus it's a good choice for iterative edits once a project is already built out

14:21
1

opus is the most powerful and what I'd recommend for the initial plan and the first build of any project

14:27
1

it reasons better through complex problems and makes fewer mistakes up front and that saves you time in the long

14:32
1

run i use it for most things but I'm on the highest plan so I have that flexibility the general

14:37
1

rule is to plan and build with Opus iterate with Sonnet if you're on the max plan and not watching

14:42
1

your limits closely you can just run Opus throughout and not think about it you will also see settings for

14:46
1

low medium high and max these control how many tokens Claude allocates to complete a task just adjust that to

14:53
1

the task as well then again you can monitor your usage under settings then usage it's got that rolling 5-hour

15:00
1

window that resets plus a weekly cap on top of that if you're on pro and using Opus heavily you

15:05
1

can eat through your limit faster than you'd expect builds take time so I cut those out of a video

15:12
1

but generally the initial build takes 5 to 15 minutes depending on complexity sometimes more instead of sitting there watching

15:19
1

it work you can run multiple sessions at the same time and build different projects in parallel i wouldn't start

15:26
1

here get comfortable with the basics first but once you are this is a powerful way to work so I'm

15:30
1

going to run three in parallel a link in bio page a product landing page and a Chrome extension all

15:36
1

using just what I've covered so far a prompt plan mode and iterations then some smaller features I'll show along

15:42
1

the way i'll create a new session for the link in bio i want something that looks unique and futuristic

15:48
1

so it's got an AI neural network visual concept and there's a few more details in here i have the

15:53
1

folder selected i'm on plan mode i'll send it off now I'll start a new session for the Chrome extension

16:00
1

select a folder it's already on plan mode up top I can already see my other session needs input so

16:06
1

i'll send this prompt really quick trust the workspace then jump over and it has some questions to answer before

16:12
1

it finishes the plan those are all easy ones so back to the extension it's already proposed a plan with

16:18
1

no questions i'll let it start building now one more session for the landing page i already have an image

16:24
1

of the product sitting in this folder that's an easy way to give Claude the assets you want it to

16:29
1

use drop images logos or whatever directly into this project folder rather than the chat this one will be a

16:34
1

simple prompt build a landing page for this product there is an image in the folder named futurefuel-can.png you can

16:41
1

use that on the site switch to plan mode and send it off now I have three projects building at

16:47
1

once i wouldn't recommend doing this right off the bat but I wanted to show the feature and it seemed

16:57
1

like an easy way to show some more simple things you can build and get ideas from the next two

17:02
1

builds will be more complex to track what's happening across sessions this panel shows the status of each a yellow

17:07
1

dot means it needs your input so the link in bio comes back with a plan but it guessed on

17:12
1

the URLs and got a few wrong i'll click revise plan drop in the correct links and approve and the

17:17
1

landing page needs me to answer some questions i jump through those all done the link and bio plan is

17:20
1

updated approve that probably felt a little chaotic it kind is but now everything's running and it's just a

17:27
1

matter of checking in as each one finishes the Chrome extension is already done i think a lot of people

17:32
1

will be surprised at how easy building a browser extension is i know I was when I first tried and

17:36
1

Claude has all the steps listed out for me in case I didn't know what to do let me just

17:41
1

explain what this is supposed to do first it fixes a very minor annoyance for me but when I open

17:46
1

up a YouTube transcript I have to click toggle off timestamps then scroll to highlight everything copy it and then

17:52
1

when I paste it somewhere it still retains all of those line breaks i want just a button that strips

17:58
1

all of that and gives me clean text so let's see if it worked claude created a folder with the

18:02
1

Chrome extension files then I just open Chrome extensions switch to developer mode hit load unpacked i need to select

18:11
1

the whole folder that has all the files in it and it's installed and again Cloud had all those instructions

18:17
1

listed out if I needed them now I'll go back to YouTube to test it open the transcript and I

18:24
1

guess it didn't oh wait there it is down at the bottom i asked for it up top but I

18:28
1

will test it out paste and there we go the functionality is there just in the wrong spot so here's

18:35
1

a tip I haven't mentioned yet anytime you have an error or a change that's easier to show than describe

18:40
1

take a screenshot and drop it in the chat cloud can see whatever you upload so I screenshotted that just

18:46
1

tell it the button is in the wrong place and ask it to move it next to the other transcript

18:50
1

buttons and while that's running I'll check the other sessions the landing page needs me to approve the plan i'll

18:57
1

do that and then the link in bio looks ready i'll close the plan then open the preview panel the

19:04
1

preview looks great honestly that is perfect on the first try i guess the only thing I'd want to add

19:09
1

is my profile picture in the center so I will drop the image file into the project folder and ask

19:14
1

it to pull that in that should be the only change and the Chrome extension fix is done all I

19:20
1

do is refresh the extension in Chrome reload the page to test and now it's in the right spot perfect

19:27
1

back to the link in bio the profile picture still isn't showing just screenshot ask it to fix it and

19:34
1

I guess a quick note the preview panel gave an error the latest update has been slightly buggy for me

19:39
1

if that happens just click open file up top and select the HTML file manually then it should load fine

19:45
1

and there it is really nice animations this looks great but I'm realizing this probably wouldn't work well on mobile

19:52
1

the buttons would be small and hard to hit so there's a toggle in the top right to switch between

19:57
1

web and mobile views and Claude actually built a separate mobile layout already without being asked and it looks awesome

20:03
1

another one done then we just had that one more the landing page my guess is this will be good

20:08
1

on the first try a landing page is pretty easy and yep looks great it wrote all the copy just

20:13
1

from the product image there's features ingredients benefits testimonials a buy now button priced a 12-pack at $39 seems a

20:23
1

little steep but maybe it's an awesome product so that was three builds to show some variety and cover a

20:29
1

few easy but useful tips along the way uploading your own assets debugging with screenshots and testing a Chrome extension

20:36
1

built from scratch all with that same basic process we've got two more builds to go the first will show

20:42
1

how to connect cloud code to tools you're already using through MCPS the second will show how to wire in

20:48
1

an AI model through the API for tech generation image analysis vision just whatever you need built directly into your

20:55
1

project then we'll learn how to push it all to GitHub then deploy it for the world

21:02
1

this next build uses something called MCPs it's a way to connect cloud code or any AI agent to external

21:09
1

tools and services you can think of MCPs like a USBC for software a universal connection protocol that lets different

21:16
1

tools plug into each other you can build custom MCPs for anything but Claude has a huge library already built

21:23
1

in they call them connectors you can find these under customize this is also where skills and plugins are which

21:29
1

i'll cover later you can click connect your apps right here to browse the list or I'll usually click it

21:34
1

over here where it says connectors and that will show all of the ones I already have connected and the

21:40
1

settings for them as well then the full list is under the plus button then browse connectors the available options

21:46
1

are huge there's all the common stuff like Google Calendar Google Drive Gmail notion Canva and tons more for this

21:53
1

build I'm going to use Granola which I use for meeting notes then a sauna where we manage team projects

21:59
1

and tasks and while we're here one I would recommend connecting regardless of what you're building is called context 7

22:06
1

it pulls in up-to-date documentation for over 50 frameworks like React Expo Tailwind Forcell and more these tools change and

22:14
1

claude may have been trained on older versions or pull in outdated info from the web context 7 makes sure

22:20
1

it's always working from current documentation definitely worth connecting then it will just always be there another example if you're

22:26
1

building out something that needs to take payments there's a Stripe MCP that makes that process much smoother there's tons

22:32
1

of useful options in here once a connector is added you can manage exactly what it's allowed to do block

22:37
1

certain actions require approval or allow automatically now my Granola and ASA are connected and ready so here's the prompt

22:44
1

for this build i'm asking it to build a conbon style interface where it pulls in my meeting notes from

22:48
1

Granola and extracts all the action items then it adds each of those to the board it will also pull

22:54
1

in a list of teammates from ASA and I can drag them onto whichever task needs to be assigned to

22:58
1

them then when I'm finished assigning I can click a button to push that all to ASA so plan mode

23:04
1

new folder send so I'm just going to skip through the planning and approval since we've already covered all of

23:14
1

that then I'll show there were a couple of errors along the way so I screenshotted those and fixed them

23:19
1

the push to a sauna button needed a fix then I needed a project selector just standard iteration now here

23:34
1

is the finished prototype so it read through the recent meetings that I gave it access to and it pulled

23:40
1

out every action item all my teammates from ASA are listed at the top it pulled those in on its

23:45
1

own then I select the project from the drop down now I can just drag people onto the tasks to

23:50
1

assign them so I'll assign a couple to me then I'll use SGE for another person to assign them to

23:55
1

so I'll push that then it says they're queued up i can say push it should be done so we'll

24:02
1

go check asauna and here are all four of the tasks properly assigned all right now I'm not going to

24:08
1

go through and make every part of this function perfectly and fine-tune all the aesthetics and all of that i

24:12
1

just wanted to show how connectors work so you can utilize them for yourself and I deliberately picked something other

24:17
1

than a standard Gmail or Google Calendar demo i wanted to show a less obvious use case to help give

24:22
1

more ideas once you start connecting the tools you already use daily the possibilities open up fast hopefully this gives

24:28
1

you a lot of ideas there are so many ways to streamline and optimize or automate workflows with internal tools

24:34
1

like this this last build does a big thing the others haven't it connects an AI model through the API

24:40
1

that will be able to analyze images and give personal recommendations based on data and once you know how to

24:49
1

do this you can utilize any functionality in LLM as that's just the ones that apply to this demo i'm

24:55
1

going to build this in a way where I can use it on mobile that feels like a mobile app

25:00
1

and before I build it I think it's worth explaining why you'd want a personal use mobile app in the

25:04
1

first place most of the time I use these for one of a few reasons either there's an existing app

25:08
1

that almost does what I want but not quite or maybe I don't want to pay for another subscription or

25:13
1

sometimes I'll download an app and then it's asking for just a ton of data I'd rather not hand over

25:18
1

and sometimes an app just doesn't exist at all so building it yourself solves any one of those and it's

25:23
1

more achievable than it sounds when you build it this way and this will be a mobile responsive web app

25:27
1

not a true native mobile app i'll cover the difference and what's involved in going further after this build you

25:32
1

can do it either way but it's kind of overkill for a personal use app but for what I'm building

25:37
1

in this one Cal AI recently sold to My Fitness Pal for a lot of money i'm going to build

25:41
1

the same core functionality from scratch create a mobile responsive web app where I can take a picture of my

25:46
1

food and it will estimate the calories and macros and log them and track them over time use Claude as

25:51
1

the model to analyze the images add a feature where you can click and get personalized advice based on your

25:56
1

logs select folder plan mode and send it off it comes back with a few questions the first is about

26:01
1

the tech stack i want this middle option because I will be deploying this through Verscell later that way I'll

26:07
1

be able to open it on the web on my phone if you're ever unsure which option to pick just

26:12
1

take a screenshot drop it into Claude and ask for clarification a lot of times I'll actually have a Claude

26:17
1

chat open in a separate window so I can ask questions throughout the build without having to fill up the

26:22
1

context in here i'll often do that before I even start a project too sometimes before diving into plan mode

26:27
1

I'll tell Claude my idea and have it ask me a bunch of questions and fine-tune a lot of that

26:32
1

before I even start my initial prompt that triggers that plan but I know what I want in this case

26:36
1

and the other questions are straightforward functionality choices then a minute or so later the plan is ready and this

26:41
1

one is more involved than the previous builds it needs to store data analyze images with an AI model generate

26:48
1

personalized advice and access the camera and Claude handles it all so I will accept the plan now to actually

26:53
1

test the AI functionality I need to add my API key and an API key is a unique string of

27:01
1

characters essentially a digital ID badge that tells a service you're authorized to use it and it tracks your usage

27:06
1

for billing and I'll use cloud as the AI model but your cloud API key is separate from your cloud

27:12
1

subscription you fund it independently through the anthropic console then it draws from that balance each time the app makes

27:18
1

a call for personal use a few dollars goes a long way and this does work the same with other

27:24
1

models like ChatCBT or Gemini 2 to get one go to the console add funds then go to API keys

27:29
1

and create a new key give it a name so you can track what it's being used for then copy

27:36
1

the API key when it appears you won't be able to see this again and this is what you'll add

27:40
1

to your project and this does need to be done properly so the key doesn't get leaked anywhere anyone that

27:44
1

has this key will be able to use whatever funds you loaded so don't paste your API key directly into

27:49
1

the cloud chat those chats travel through the web and depending on your settings they may be used for model

27:54
1

training i'd recommend turning that off but either way the safer habit is to add the keys manually these types

27:59
1

of variables are added to av.local file env is for environment variables and local means it only exists on your

28:05
1

machine and you don't need to go here but in your file structure it's in.git ignore that means if you

28:13
1

push this project to GitHub this file never goes with it you can always ask Claude for these best practices

28:19
1

too it's familiar with all this stuff like always it'll walk you through step by step and I'll actually ask

28:24
1

it to create that.local for me and once Claude creates the file I can click right here to open it

28:28
1

directly in the panel on the right and this is now me interacting with my local file system not Claude

28:35
1

i replace the placeholder with my actual key then save it and now it's done safely i'll tell Claude the

28:41
1

key is added and ask it to test i'll open the app in the browser this time because I want

28:47
1

to show that the address bar says localhost that means that even though I'm in a browser this is only

28:52
1

accessible on my machine right now not the web yet but there is an error the API isn't detected so

28:58
1

I'll just tell Claude what happened claude figured out the issue and fixed it test again another error looks like

29:05
1

the image is too large i sent just a screenshot of the error so Claude built in automatic resizing to

29:12
1

handle that going forward test again and the analysis runs the calorie and macro estimates look accurate i can submit

29:18
1

the entry view the log history check the goals tab and pull up personalized advice that doesn't have much data

29:26
1

to go off yet but it's all working so that's a working prototype but I don't like the look of

29:33
1

this at all and I want to change a bunch of things so I'll just iterate on this really quick

29:38
1

off camera and come back when it's done so here it is i like the look of this much more

29:42
1

and it's called morsel it's all functioning it was probably unnecessary for me to build this out and make it

29:47
1

look nice just for a demo but I think this looks pretty good

29:52
1

so I will run the init command that will generate the cloud.md file before moving on now all the project

29:59
1

context is saved next I'll go through all the steps to actually deploy something the process will be set up

30:05
1

git then connect to GitHub and push all the code there then we'll connect GitHub to versel to deploy a

30:12
1

live site and Claude is going to do a big portion of this but there are some manual steps along

30:18
1

the way too we need to connect a GitHub account github is a cloud platform for posting code once your

30:23
1

project is there you can access it from any device share it with others or deploy it to the web

30:32
1

it's also good for version control you'll always have a saved snapshot of your project and can roll back to

30:37
1

any previous state if something goes wrong but to make this work we also need Git installed locally on a

30:42
1

newer Mac it's usually already there windows users will have slightly different steps but since we're asking claude it will

30:47
1

give you the right instructions for your specific setup automatically just start with this prompt check if I have Git

30:54
1

installed if not install it for me and mine is already installed because it came with my Mac out of

30:59
1

the box if yours isn't Cloud will walk you through it windows users may get a PowerShell permissions prompt just

31:04
1

follow what it says once that's confirmed ask it to connect to GitHub so it can push code on your

31:10
1

behalf and to walk you through anything that needs manual input it will tell me the four-step process we're going

31:15
1

to go through to do that and installing Homebrew is the first step of that process i'll tell it to

31:22
1

start the Homebrew installation process then it comes back and tells me I need to copy and paste a command

31:27
1

into the terminal so this is where we need to actually interact with the terminal ourselves i could do a

31:33
1

spotlight search for terminal and it looks like this this is the command line interface you interact only through text

31:39
1

commands i know scary stuff but we're only running a couple of commands and Cloud makes it easy and instead

31:45
1

of opening the terminal separately you can use the same panel button and open it right there then it's just

31:51
1

copy paste then hit enter then it does ask me to input my password so this is the password to

31:57
1

my computer and when you type this it won't actually do anything as you're typing the cursor won't move there'll

32:04
1

be no hidden characters it looks like just nothing is happening so it might feel like you're doing something wrong

32:09
1

but that's just the way it hides passwords so just type your full password and hit enter then just wait

32:14
1

a minute and when that input field reappears it's all done then tell Claude that homebrew is installed and ask

32:20
1

what next now it popped up asking if it can run a terminal command itself to install the GitHub CLI

32:27
1

i will allow then it installs it the last part it needs is me to run one more terminal command

32:34
1

to authenticate to actually connect my GitHub account so for this step you do need a GitHub account if you

32:41
1

don't have one it's free set it up like any account then once you're ready copy the command Claude gave

32:47
1

paste it into the terminal and hit enter then it will ask a few questions and Claude actually told me

32:53
1

exactly what to answer for each of these questions already i use it on github.com preferred protocol is https then

32:58
1

authenticate by logging in with a web browser now it gives me a code to copy so copy that then

33:06
1

hit enter to open up the link it gave and continue with my account paste the code then authorize GitHub

33:12
1

then it sends a code to that email i'll enter that here and we are all set github is officially

33:19
1

connected so back in cloud code I'll say all done now it's verifying it works it did so it says

33:25
1

it can now push code create and clone repos and open PRs on my behalf perfect now let's use it

33:32
1

i'll go back to the cube tactoe project and say create a new GitHub repository for this project and push

33:39
1

all the current code then couple of approvals and it's done with a direct link to the repo it just

33:44
1

created i'll open that and this is the repository on GitHub with all the files that have been created so

33:50
1

far that probably felt like a lot if you're new to all of this that's exactly why I walked through

33:56
1

every step the good news is you only do this once from here for any new project it's just a

34:01
1

prompt you just say create a new repo and push the code and it handles it all and I could

34:06
1

had made a video that skips the tedious parts like this but I'd rather make sure you're actually set up

34:10
1

in the best way this stuff is important if you want to use cloud code seriously so I'm trying to

34:15
1

cover all of it but now that all the code is on GitHub it's actually really easy to deploy but

34:19
1

first a quick detour i want to cover skills skills are reusable workflows you can build into Claude they're like

34:26
1

recipe cards for repeatable tasks there are skills built in by default there's ones you can find from other people

34:33
1

and ones you create yourself you find them under customize same place we went for connectors and there's a library

34:38
1

of pre-built skills covering a wide range of tasks and if you want more there are community databases on GitHub

34:45
1

but you can also build your own if there's ever a multi-step process you go through regularly just do it

34:51
1

once with Claude then ask it to package that up as a skill and from that point on it gets

34:56
1

triggered automatically whenever you ask for that task and that saves you all the prompting and back and forth time

35:01
1

now plugins are in here too it's a similar concept but broader they cover an entire role or workflow rather

35:07
1

than just a single task and same deal you can find community-built ones on GitHub the skill I want to

35:13
1

show right now is a security review this one's built in by default and this project is simple enough that

35:20
1

i'm not expecting anything to get flagged but it's always worth running before you make something public i can just

35:24
1

say run a security check and it will trigger the skill they are also under slash commands if you want

35:30
1

but you don't need to use those my wording will trigger that skill automatically and with that Cloud will run

35:34
1

through the full codebase and look for vulnerabilities and the result for this one no high or medium severity issues

35:40
1

identified there's a full analysis listed and just a clean conclusion at the bottom no exploitable vulnerabilities for this project

35:46
1

that makes sense i didn't use API keys there's no user data being collected but the habit of doing this

35:54
1

is important if you are including any of those things API keys user data taking payments it is much more

36:00
1

serious to spend time on security and make sure this is all perfect the morsel app for example does have

36:05
1

my API key in it i kept that repo private and it's only for personal use but if I were

36:10
1

sharing that with anyone I'd want to go deeper on this and be sure it's probably enough of an explanation

36:15
1

for this video but as your builds get more complex definitely pay attention to security and privacy but one more

36:19
1

thing I ask before going live is there anything else I should be aware of before making this live for

36:25
1

other people to access it will find nonsecurity issues you might have missed oh in this case it flags that

36:30
1

the game won't load on older browsers easy fix if I want it covers the mobile touch functionality which I

36:36
1

didn't test yet actually like how that would work on a touchcreen it thinks it'll work but that's something I

36:42
1

should verify and then there's other little things like that you can't restart Midame that's a good point those are

36:46
1

all easy fixes but things I didn't notice on my own so this can be really helpful moving on to

36:52
1

the deployment i'll be using Versel which is one of the most common platforms for this and it's really easy

36:59
1

to set up and free for the amount I'll be using it there are paid levels if you're scaling things

37:03
1

up but just connecting a repo for personal use is free i'll create a new account to show this from

37:08
1

scratch i'll create it with this GitHub account then it will take you to this page and right in this

37:12
1

box where it says import git repository I'll click the button continue with GitHub click install and it will connect

37:19
1

forcell to my GitHub account i'll select all repositories and install then that box populates with the repositories I have

37:26
1

on GitHub i will click import on cube tactoe then I don't need to change anything on this page just

37:33
1

hit deploy and that's it the game is live on the web i will come down to dashboard first and

37:39
1

this has everything you'd need for more complex projects integrations storage logs and the cool thing is anytime I make

37:44
1

a change and push it to GitHub through cloud code Verscell will automatically detect that and redeploy with the newest

37:50
1

update no extra steps then right here is the domain this is live and playable at i will leave this

37:56
1

in the description in case anyone else wants to play it i thought it was really fun to play so

38:02
1

I will probably make some other changes to the game and tweak it a bit it might look a little

38:06
1

different by the time I post this video

38:10
1

deploying Morsel is a bit more involved but the approach is the same so push the code to GitHub connect

38:17
1

the repo to Verscell just like before and it'll deploy but it won't be functioning yet there will be errors

38:23
1

you can copy logs or screenshot them and ask Claude to fix things it'll just work through them i'll walk

38:29
1

through a couple things that were flagged in this project because they'll be common ones versell doesn't have access to

38:34
1

your API key like I mentioned that M.LO file never gets pushed to GitHub which is exactly what you want

38:40
1

for security but it means you need to add those environment variables manually in Verscell storage is another piece since

38:45
1

morsel needs to save food logs and photos there's a storage tab in Verscell where I set up Neon for

38:52
1

the database and blob for file storage you create them connect them and then they're ready neon holds the data

38:58
1

blob holds the photos and then that API key in the environment variables handles the AI analysis that ties it

39:05
1

all together so as always ask Cloud for the steps and screenshot when you hit something unexpected these types of

39:11
1

things will vary from project to project so I won't spend a lot of time walking through every step here

39:17
1

just know that for more complex projects there will be other steps and bugs along the way this will take

39:21
1

some trial and error always but especially when you're getting started there's no way to cover every single thing that

39:27
1

might come up in a video but that's part of the process get comfortable working through issues and learning new

39:33
1

things along the way and this one was still pretty easy even with how much is actually going on in

39:38
1

this project i'll show one last part now that this is set up actually using this on my phone this

39:43
1

is a mobile responsive web app not a native app but you can make it feel like one so you

39:50
1

open up the site on your phone's browser tap the share button and then add to home screen now it

39:56
1

sits on your home screen like any other app the logs I saved on my computer are already there and

40:03
1

I can use the phone's camera to log new meals too got one of these seaweed things sitting next to

40:08
1

me so the camera part worked and it logged it this is pretty amazing to be able to build something

40:12
1

like this in under an hour if I wanted to build this as a true native mobile app it is

40:20
1

a lot more steps and they're different than the ones we went through so it would have added a huge

40:25
1

amount to this already long video and most people watching won't need that yet once you've mastered everything in this

40:29
1

video you can start experimenting there ask Claude for the steps and work through it now I could just keep

40:35
1

going deep dive into every step and make this a 5hour video but I don't think that's what actually gets

40:40
1

you building everything in this video is more than enough to start and get through all the common obstacles after

40:45
1

you've gone through a couple each next one just feels easier and usually the very first project is the hardest

40:50
1

and we just went through six so hopefully this video gets you going if you build something using what I

40:55
1

covered I would love to see it or if there's a specific part of this you want me to go

41:00
1

deeper on you know a full video on true mobile apps or more specific into skills or MCPS just anything

41:04
1

let me know in the comments

点击任意行跳转 · 悬停可向 AI 提问

内容简介
The Ultimate Non-Technical Guide to Claude Code

Claude Code is transforming the way we think about software development by allowing anyone to build applications using natural language. Unlike standard AI chatbots that merely provide advice or code snippets, Claude Code acts as an agentic tool that runs directly on your local machine, creating and editing files to deliver functional prototypes.

Getting Started with Claude Code

To use Claude Code, you need a paid subscription (Pro or Max). While there are multiple interfaces available—including the Terminal and integrated development environments (IDEs)—the Desktop App is the most accessible entry point for non-technical users. It offers a streamlined 'Code' tab where projects are organized into local folders.

The Core Workflow: Plan, Build, Iterate

The secret to success with Claude Code lies in its Plan Mode. Instead of rushing into code generation, Plan Mode allows the AI to map out the architecture and ask clarifying questions. Once the plan is approved, the iteration process begins. The speaker emphasizes making one change at a time to avoid complexity errors and ensure a solid foundation.

Advanced Features and Context Management

As projects grow, managing the 'memory' of the AI becomes crucial. Using the /init command, users can generate a claude.md file. This document acts as a permanent reference for the project's tech stack and rules, allowing you to start fresh sessions without losing critical progress.

Model Selection Strategy
Opus: Best for initial planning and complex first builds.
Sonnet: Ideal for iterative edits and everyday tasks due to its token efficiency.
Haiku: Best for fast, light tasks that don't require heavy reasoning.
Connectivity and Deployment

One of the most powerful aspects of Claude Code is the Model Context Protocol (MCP). This allows the AI to connect to external tools like Asana for task management or Stripe for payments.

To share your creations with the world, the guide walks through a professional deployment pipeline:

GitHub: Host your code online for version control.
Security Reviews: Use built-in skills to scan for vulnerabilities.
Vercel: Connect your GitHub repository to host your site live on the web for free.
From Web to Mobile

While building a 'native' app (the kind you download from an App Store) is complex, Claude Code makes it easy to build mobile-responsive web apps. By using the 'Add to Home Screen' feature on a smartphone, these projects look and feel like true native applications, complete with camera access and local storage capabilities.

00:00 / 00:00
1x

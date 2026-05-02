# 一次登录打通所有 MCP：WorkOS 的 Cross-App Access 方案 | BestBlogs.dev

- BestBlogs URL: https://www.bestblogs.dev/video/adebf6b
- Extraction: DOM text from BestBlogs page
- Extracted chars: 27692

---

VIDEO
92
⭐ 精选内容
One Login to Rule Them All: Cross-App Access for MCP — Garrett Galow， WorkOS

Garrett Galow 解释了 Cross-App Access 和 ID-JAG 如何让身份提供商在 AI 客户端与 MCP 服务器之间建立安全信任桥，减少重复授权。

⭐ 推荐理由WorkOS 的 Garrett Galow 精准定义 MCP 生态的核心痛点：每接入一个服务就多一个 OAuth 授权页，对用户造成“授权疲劳”，对企业则缺少集中式访问管理、撤销控制和生命周期管理。Cross-App Access 通过 ID-JAG（Identity JWT Authorization Grant）让身份提供商成为 AI 客户端与 MCP 服务器间的信任桥，一次 SSO 后自动完成后续授权流程。目前最清晰的 MCP 身份架构方案，附具体实现指引。

展开
AI Engineer
关注
·
04-28
·
7 个章节
·
查看原文 →
一次登录打通所有 MCP：WorkOS 的 Cross-App Access 方案
章节导览
7 个章节
CH.1
Introduction and Personal Background
00:14
CH.2
The Problem: Consent Screen Fatigue
01:23
CH.3
IT Management and Security Risks
03:51
CH.4
Cross-App Access (XAA) and Live Demo
06:39
CH.5
How It Works: The ID-JAG Protocol
09:29
CH.6
Implementation and Setup for Admins/Devs
13:10
CH.7
Q&A: Scopes, Entra Support, and DCR
17:05
📝 实时字幕
跟随播放
全部字幕
00:14

all right good morning everybody thank you for coming to this talk hopefully your morning was eventful i caught a

00:21

little bit of the keynote i wasn't able to catch all of it but it was pretty good um my

00:25

name is Garrett Galo today I'm going to be talking about one login to rule them all uh or crossop

00:30

access for MCP in case you haven't heard about that uh quick intro about myself uh I run product at

00:37

work OS i've been building enterprise developer platforms for the past almost 15 years uh originally at Microsoft Azure then

00:44

at Cloudflare for a long time and now at work OS if you haven't heard of work OS before we

00:52

make your app and also your agents enterprise ready uh we power off for the likes of Enthropic Cursor OpenAI

00:59

so if you've ever logged into Cursor for example whether that was with username password or like an enterprise IDP

01:05

you've used work OS um today I'm going to be talking about uh MCP and signin through things like anthropic

01:14

and cursor um but first uh if you've used MCP at all extensively you know that it means consent screens

01:23

on top of consent screens on top of consent screens who here uses MCP servers on the regular okay most

01:29

of you um if you haven't kind of experienced this before uh here is uh cursor which I have set

01:36

up uh and if you want to use MCP servers with cursor you know you add them in you have

01:41

the little config file and then in each one of these if you want to use it you have to

01:45

connect it'll pop up this window you have this nice little consent screen that you're not going to read you're

01:51

just going to say okay and you're going to get redirected back and you need to do this for every

01:56

single tool which is frankly pretty annoying and sometimes you have to do this again you don't really know why

02:03

sometimes you have to do this again sometimes it seems to forget that you've already done this um yeah and

02:09

so this is like a thing you have to do uh every time you want to use uh these MCP

02:14

servers and uh that's not fun but it's in a company with a lot of developers it's not just you

02:21

know one person's inconvenience uh as a user you might log into a half dozen or a dozen MCP servers

02:27

um but when you combine that together across your team you basically have dozens and dozens of people spending all

02:33

this time managing all these consent screens clicking these buttons uh without really caring why they have to do this

02:40

now this is a relic of a lot of the technology that MCP decides to use it uses OOTH as

02:44

an underlying uh authentication layer and so uh the way O was kind of invented around was this thing of

02:50

like you don't tr you know these two systems don't trust each other so you have to like provide this

02:53

consent to say yes cursor can have access to my Figma account yes cursor can have access to my notion

02:58

account um but the reality is that's not really how uh you know things operate today that's not how companies

03:06

operate um you know we have a thing called single sign on most people are using it if you have

03:12

a company you're logging in through something like an octa or Microsoft intra one of these systems um and that

03:18

sort of you know that idea of like one login sign into all those applications worked great but MCP breaks

03:24

this model right it sort of assumes that uh you know none of these apps know anything about each other

03:29

there's no way to know that you're the same person that you know you should have access to these systems

03:33

and so you have to go through these flows over and over and over and over again now that is

03:38

really annoying um and maybe that unto itself is a problem worth solving but you know humans will tolerate a

03:44

lot of annoyances if they get value out of it the real problem comes in um for the IT team

03:51

like the people managing all these applications uh MCP is not doesn't work the way that they want it to

03:57

work you know it can't really tell like what MCP servers you may or may not be using you're connecting

04:03

to these arbitrary things you're not necessarily going through that IDP to connect to them um which is problematic they

04:11

basically can't determine uh you know which AI agents you can actually use right uh in theory you can take

04:18

any arbitrary MCP client you know that might be a cursor but you could be using u sort of like

04:23

a deepseeek or some of these other tools that maybe your IT team doesn't want you to use and um

04:29

you're granting access to these sensitive systems right you know you have lots of data and things like Figma or

04:34

notion that you know it maybe doesn't want any you know any AI agent to get access to the other

04:41

thing is actual access and security um I don't know how many people heard about the npm Axios package getting

04:48

popped about a week ago uh unfortunately I was uh hit by that i'm still not exactly sure what npm

04:56

package thing I use that had that dependency but uh you know our IT team you know became aware of

05:02

that problem they were able to detect that you know my machine had been compromised they were able to cut

05:07

off network access to my machine they could invalidate my octa sessions across all the applications so they could help

05:12

secure uh you know my my account and our company data but you know in my local machine I had

05:19

MCP servers connected I had like API keys that I was using for certain things like that's the real we

05:24

had to go through and do all this you know I was looking through my laptop seeing like what did

05:27

I connected to what services might I have some sort of other credential not driven from the IDP that you

05:33

know is at risk of being leaked how do we go revoke that how do we ensure that you know

05:38

my system safe uh MCB today using OOTH you know if something happens like that or you know you leave

05:46

a company and it might revoke your you know single sign on through your IDP to those applications you still

05:51

have these access tokens these refresh tokens even in most cases that give you standing access to these services that

05:57

means you might have access for uh days or weeks or even months um you know many companies don't use

06:03

things like skim which allows you to revoke that access fully but you know and so that means that uh

06:09

you have this like lasting access problem that it doesn't have any visibility over and then again every time someone's

06:15

on boarding to the team they have to go through this whole thing where uh it might be able to

06:19

like automatically set up the MCP servers you're using in something like cursor or claude um but you still need

06:25

to go through all this authentication um and manage all these connections yourself so um obviously this isn't great so

06:33

what are we doing about it right what's the solution to this the solution solution is cross app access

06:39

otherwise known as XAA XA is basically a way in which the identity provider can act as a standin a trust

06:48

provider between applications so let's say the example of I have cursor that's my MCP client uh Figma is the

06:56

MCP server I want to connect to and then octa is the IDP that we use at our company for

07:01

logging into things so both cursor and figma already have this trust relationship ship with octa right to lo into

07:10

cursor I go through octa to lo I go through octa so both of these applications know about you know

07:15

work osc.com they know about me as a person that has access to these applications what cross app access does

07:22

it helps bridge the gap between cursor and figma but providing a way for cursor to talk to Figma they

07:27

can both depend on that trust reliance on octa and they can get credentials issued without manual or human intervention

07:36

So let me show you a little bit what that looks like so I'm going to flip over to uh

07:41

my terminal and make it bigger and more visible so uh here on the left on this tab I have

07:49

just like regular cloud code set up and you know if I check my MCP servers uh you know I've

07:55

connected the Figma server here obviously it needs authentication i could go through that you know it's going to present

08:01

a consent screen um that's kind of the standard flow uh in this window over here uh we have a

08:08

version of cloud code that is xa compatible basically implemented xa here so um the first thing I do just

08:15

kind of show uh since this is sort of like a a beta implementation of this um I can basically

08:23

say like I have configured inside of cloud code um this connection to my octa environment and the first thing I'm going to do here is I'm going to log in

08:35

and so this is doing an octa in i'm going to log into my Octa environment

08:44

you know this is the thing you need to do one time in order to uh if you were

08:49

setting up Claude for the first time you'd be logging into Octa okay that's all done now um

08:56

and then now if I start up Claude and I look at my MCP servers we'll notice here that Figma

09:04

is automatically connected let me try and make that a little bit bigger and so I didn't have to do

09:10

I didn't have to click anything i didn't have to see a consent screen uh Figma's automatically connected and now

09:16

you know whether it's Figma or a list of MCP servers I can do all of that i know that

09:21

kind of seems like magic i didn't actually have to click anything did I actually do anything promise I did

09:25

let me kind of talk a little bit about what's actually happening behind the scenes the whole point of this

09:29

is you don't have to do anything right so it doesn't it appears as like it's sort of automatic but

09:35

uh here's how it works so in this uh situation we basically have four systems the client which in that

09:41

case was cloud code I was using the identity provider which is octa the resource authorization server uh which is

09:48

in this case managed by Figma but we're separating it from the resource server which is the Figma API um

09:54

if you're not familiar in MCP you'll have the resource server which like your MCP server it will call out

09:58

to a separate place to do authorization and issue tokens so in the case the first thing I did I

10:04

did that octa login right so the user goes through SSO to the IDP and that issues back an ID

10:11

token and refresh token so in this case Claude holds on to those tokens and it's able to use that

10:17

in the next step to uh to ask for what's called a uh ID Jag token so ID JAG is

10:25

uh happens to be the name of the spec that that all this technology is built off of stands for

10:30

identity JWT authorization grant it's a very big mouthful effectively it just means a token issued by an IDP that

10:39

can be used across services to uh manage access so the client goes back to the IDP says "Hey I

10:46

have this refresh token for Garrett would you please give me this ID Jag token that will work with Figma?"

10:52

Uh Octo basically knows about Claude knows about Figma it can check hey is Garrett a member of both of

10:58

these applications uh am I allowed to do this says "Am I allowed to issue tokens for Claude on behalf

11:04

of Figma?" The answer is yes octa will send back this ID Jag token to cla code then Claude sends

11:12

that to Figma in this case Figma's authorization server says "Hey I have this ID Jack token for Garrett from

11:18

the works Octa instance could you please validate this and provide me back a token?" Figma because it has this

11:25

relationship with Octa goes through verifies the ID Jag once that's verified and correct it is then able to issue

11:32

this access token back to cloud code and at that point uh step four here is the regular MCP offflow

11:38

so it just starts talking to the MCP server it's using a regular O access token it's not a new

11:44

type of credential and then you know now I can talk to the MCP server figma will issue responses and

11:49

we're off to the races uh a few things that are important here uh steps two and three here are

11:56

totally invisible to the user right once I've logged into the IDP which I don't have to do that very

12:01

often you know that can be you know once a day it's kind of up to the IT you know

12:06

your company's policies maybe that's once a day maybe that's once a week once you've done that login you don't

12:10

have to do that again steps two and three are done behind the scenes uh and then step four is

12:15

just the regular access token request that you're doing to the MCP server the other thing around this is uh

12:22

in the case of this access token that's being issued uh that could be very short-lived so most applications issue

12:29

access tokens around five minutes um and so what happens is that token will expire after five minutes but you

12:37

don't need the human to do anything you can basically rerun this ID Jagra flow plus the exchange and get

12:43

a new access token as needed and so as long as your SSO session is active you can keep getting

12:48

these ID Jack tokens and exchanging them for access tokens and so you actually have a better security posture where

12:52

if something happens and you know my access is removed for some reason or my session is locked with octa

12:59

once that access token expires I won't beble to get back in I won't be able to reconnect to that

13:03

MCP server and so I want to go a little bit through um you know what does this look like

13:10

on the setup side like what does your IT admin need to do if you're running MCP client what do

13:14

you need to do if you're running MCP server what do you need to do on the IT side it's

13:18

actually pretty straightforward Right uh you're already going to have a like cloud code or cursor octa application created you're

13:25

already going to have the fig Figma SSO application created right those will be existing things that your company already

13:30

has inside of a system like octa there's this new kind of manage connections portal where you basically come in

13:35

and say hey which app do I want to grant the ability to request access to this other app so

13:40

in this case we're saying cursor can request access to Figma uh and that policy means that when if cursor

13:48

comes knocking and says hey octa can I have an id jag token for figma part of its request is

13:54

which system does it want access to octa can verify that and say yes actually uh cursor is allowed to

14:00

request this access out of Figma and we'll issue that token so that's all all you really have to do

14:05

on the IT side once you've done that everything else is as normal like you know the user must belong

14:10

to both applications you're kind of doing the same kind of management policy as you normally do on the MCP

14:17

client so this would be your cloud code your cursor or if you're building kind of your own MCP client

14:23

there's a handful of things you need to do one you need to have an SSO connection that's XA compatible

14:29

so you know in general if you're supporting SSO in your application or your client that's kind of the standard

14:33

fair um XA support is relatively new so C uh Octa does support it but with some caveats um they're

14:41

working through those we're working with other industry partners like Microsoft that have them support this as well but you

14:46

need that and that customer's uh IDP connection would need to be XA compatible enabled uh your client requests IDJ

14:54

token from the ID uh identity provider you get that token back you need to make that exchange request to

15:00

the MCP server so you need to uh support uh that token flow and then once that's done number four

15:06

is your standard just talk to an MCP server so nothing new there uh we've built support as someone who

15:12

you know we provide authentication services for for our customers we've built support for one two and three here so

15:17

we can handle if you're building an MCP client we can handle all of that flow um we're actually the

15:22

way in which you know cursor and enthropic are doing this because they use us for their SSO connections on

15:29

the MCP server side which is probably more relevant to most folks is like you might be you know your

15:34

company might have an MCP server you want customers to use there's also some stuff you need to do to

15:38

support it on your So the first is there's this new um JWT bearer type that you need to support

15:45

um so this is basically like announcing that you now support uh this ID Jag flow and that you'll accept

15:50

these kinds of tokens then obviously like MCP clients are going to send you those tokens you need to accept

15:56

them uh and then you need to verify them so there's a step where you go to the uh identity

16:01

provider the octa URL and say like hey is this a valid token it's basically it's kind of assigned JWT

16:06

kind of like how you'd validate JWT in any other context you're doing the same thing here and then last

16:13

uh which should be kind of the normal thing is issue the access token right so you validated everything now

16:17

you want to give them an access token

16:22

if you'd like to learn more about how this works I you know kind of treated this as like a

16:26

highle overview obviously like there's a whole spec defining ID Jag and the specifics around how it should work uh

16:32

that's an exercise I leave to you the reader if you want to go explore the spec um I will

16:36

say like Claude is very good at explaining the spec so that might be an easier way to get introduced

16:40

to it without having to go read you know uh IETF nomenclature um but here we have a blog post

16:46

kind of outlining all the details around IDAG how does it work um a lot more of the technical aspects

16:51

of it if you're interested um so yeah you can check that out to learn more and with that uh

16:57

happy to answer any questions people have yeah so this might uh this might solve the authentication problem but does

17:05

it also solve the authorization problem let's say for Figma you've got like different token scopes does that also solve

17:12

the authorization bit as well yeah uh so just I'm going to repeat question so people on the recordings can

17:17

hear it question is this solves authentication not authorization does this do anything to to help with that um by

17:23

default no uh so this is p kind of just around the authentication bit um this is still you know

17:29

you logging into Figma uh as yourself you know so you're getting the permissions that you have uh with Figma

17:36

um one of the things we're kind of talking about is like okay how do you extend this to be

17:39

able to um define like scoped access so maybe uh you know octa saying yes I'm I will grant this

17:46

crop cross app access but there's caveats alongside like the permissions I'm going to grant that's not something that's like

17:52

part of the spec today um but obviously like something that's important that we need to consider ask the same

17:59

question for a second b um how does the uh MCP client know which app to go for inside Octa

18:11

the question how does the MCP client know the app it's requesting access for in Octa uh the answer is

18:18

basically like an audience URL so you would use um in this case it's like you know mcp.figma.com figma.com you

18:24

know is the the Figma's MCP server that audience will be known inside of Octa and so uh your cursor

18:33

will request to your Octants and say "Hey here's the audience I'm looking for." Um that's configured inside of Octa

18:39

to say like the Figma app covers this audience and then that's how it's checking the access request so use

18:47

that to hack scopes um no I don't think you'd use it to hex scopes because it's it's just audience

18:53

which is kind of like a standard OS parlance so um yeah that's the thing that like uh cursor knows

19:01

the audience that it's trying to get based on the MCP server octa is configured to know for this app

19:06

that's the audience that it controls and then obviously you know Figma knows its own audience and is and is

19:10

checking uh you know the validity of the JWT with with Octa

19:17

cool yep do you support Azure um intra yeah yeah yeah it's intra supported uh Microsoft doesn't hasn't yet added

19:29

XAA support inside of intra um that's something we're working with them on if you have connections push uh because

19:37

we want to get this adopted more broadly um yeah kind of more generally uh today with Octa this is

19:44

supported for OIDC based connections um but they're they're going to support this for sample based connections as well um

19:50

kind of the spec defines that you whatever you send to the IDP it's either a refresh token ID token

19:56

or a sample assertion so kind of just something that proves that you have an you know the user has

20:00

a session in your app um that's the only part that's cares about the type of SSL connection you have

20:06

but yeah right now it's just octto hopefully that will be more soon okay so so there is no intro

20:11

at no they don't support it yet so can I follow up with this sure so with Microsoft I ran

20:21

into various client protocol fragmentation okay um there was a resource parameter problem where cloud code sends the resource entra

20:32

validates but it has to match the scope um the way codeex does it is completely different wake log desktop

20:41

does it is not the same either sorry this is to what part of the flow is this or what

20:49

when cursor claude is talking to uh Microsoft here is that for like single sign on or is that for

20:56

single sign on okay so there's an RFC 9728 when does the initial discovery Yeah the resource the resource in

21:09

the scope have to match otherwise

21:14

yes and different protocols need a set of different yeah I would have to maybe we can I can talk

21:22

to you after we run this one it's a little in the weeds yeah I mean uh if this is

21:27

like a OIDC based connection then yeah the scopes that the client is requesting need to match what the server

21:34

will allow and if there's a mismatch there there's kind of different ways you can handle it but like you

21:39

should grant obviously scopes that weren't you know allowed um so that might be we can talk about it can

21:45

see uh that's the issue where doesn't support VCR set up proxy that now needs to be aware of which

21:54

client is coming in to tweak a few headers before sending it across i wonder if like yeah uh the

22:03

question was intro doesn't support DCR so that creates issues yeah that's um kind of I think a general problem

22:09

in the wild is you know which clients and which servers support all the you know as the MCP spec

22:14

develops um so I would say like most clients and servers support DCR at this point but obviously not everyone

22:21

does and there's not a lot you can really do if uh you know one doesn't support it you have

22:26

to like you know go reg you know in case of it's not DCR you have to go pre-register that

22:30

client um you know CIMD is like the new standard that kind of supersedes uh DCR it's um uh command

22:38

or I actually forgot what the CI stands for it's metadata it's like a metadata document that defines clients up

22:44

front so you don't have to create the clients every time um but that one has even less broad support

22:49

in the ecosystem because it's you know it's like three months old um but it is like a better experience

22:53

so yeah there's still a little bit of um catchup in the ecosystem to you know uh supporting like the

22:59

latest spec cool yeah

23:05

great well thanks everyone for your time have a great rest of the conference

点击任意行跳转 · 悬停可向 AI 提问

内容简介
One Login to Rule Them All: Cross-App Access for MCP

In the rapidly evolving world of AI engineers, the Model Context Protocol (MCP) has become a standard for connecting AI agents to various data sources. However, as Garrett Galow (Head of Product at WorkOS) explains, the current implementation has a major friction point: Consent Fatigue.

The Problem: Friction and Security Gaps

Currently, MCP relies on standard OAuth flows. This means every time a developer wants to connect an AI client (like Cursor or Claude) to a server (like Figma or Notion), they are met with a series of repetitive consent screens.

For an individual, this is annoying; for an enterprise, it's a management nightmare.

Lack of Visibility: IT teams cannot see which arbitrary MCP servers users are connecting to.
Persistence Risks: Standard OAuth tokens can live for days or weeks. If a machine is compromised or an employee leaves, revoking access across dozens of disconnected MCP servers is nearly impossible.
The Solution: Cross-App Access (XAA)

Cross-App Access (XAA) introduces a model where the Identity Provider (IDP), such as Okta, acts as a bridge of trust between the client and the server.

How XAA Works (The ID-JAG Protocol)

The technical backbone of this solution is the Identity JWT Authorization Grant (ID-JAG). The flow works as follows:

Single SSO Login: The user logs into their IDP (e.g., Okta) once.
Silent Token Exchange: Behind the scenes, the client requests an ID-JAG token from the IDP for a specific 'audience' (the MCP server).
Automatic Connection: The MCP server validates this token with the IDP and issues an access token.

This process is entirely invisible to the user, eliminating consent screens while ensuring that access is tied to a central, revocable SSO session.

Security and Implementation

By moving to XAA, companies gain a better security posture. Access tokens can be short-lived (e.g., 5 minutes). Because the renewal process is automatic as long as the SSO session is active, the moment an IT admin kills a session in Okta, the user’s access to all connected MCP tools is revoked almost instantly.

Current Support
WorkOS: Fully supports the ID-JAG flow for clients like Cursor and Anthropic.
Okta: Currently the primary IDP supporting XAA.
Microsoft Entra: Support is not yet native, though industry efforts are underway to expand adoption.

As the AI ecosystem matures, moving away from 'relic' authentication methods toward centralized, enterprise-ready identity management is essential for scaling AI agents in the workplace.

00:00 / 00:00
1x
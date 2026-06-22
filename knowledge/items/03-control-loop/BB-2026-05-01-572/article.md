# AI agents expose the security checks you never actually wrote

- BestBlogs URL: https://www.bestblogs.dev/article/aa9f535e
- Original publisher URL: https://stackoverflow.blog/2026/06/15/ai-agents-expose-the-security-checks-you-never-actually-wrote/
- Source: BestBlogs / Stack Overflow Blog
- Publish time: 2026-06-15 22:58:54
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 3; page/content captured from BestBlogs resource APIs
- Extracted chars: 7803

---

Earlier in June, attackers took control of more than twenty thousand Instagram accounts, including the dormant Obama-era White House account, without writing an exploit or guessing a single password. They opened a chat with Meta's AI support assistant, asked it to attach an email address they controlled to an account they did not own, and requested a password reset to that address. Meta later confirmed what the logs already showed: the assistant behaved exactly as designed, while a separate part of the system was supposed to verify that the email belonged to the account, and that check never ran.

  Calling this an AI mistake misses what happened. The assistant carried out a valid sequence of permitted operations for whoever was talking to it. What would have stopped the attack was a person: a support worker who saw a stranger rerouting a celebrity's recovery email, sensed something was wrong, and refused.

  A large share of real-world authorization was never written as software at all. Instead, it lived in the discretion of whoever stood between a request and the system, and everything behind them was built assuming that discretion would always be there. Put an agent in that seat and discretion vanishes, while nothing and nobody downstream notices. The agent does not bypass your security model, i justt exposes the part of it that was a person.

  A confused deputy with a chat window

  Security has a precise term for what Meta hit: the confused deputy. A process holding real privileges is talked by a less-privileged party into using those privileges on its behalf. No clear? It's the night guard who unlocks the vault for anyone who calls and says the boss sent them: he's got the keys, they've just got a good story. The canonical 1988 case was a compiler that could write to a protected billing file. A user who could not write there asked the compiler to do it for them, and it complied, because it had the authority and never asked whose request it was serving.

  An LLM agent is one of these by construction. Its interface is natural language, which carries no notion of who is authorized to do what, and the model's whole job is to turn a plausible-sounding sentence into a tool call. A direct API request at least brings the caller's identity along with it. A sentence does not, so unless that identity is reattached before the call fires, the agent acts on its own authority and the requester's permissions never enter the picture.

  Agents also cannot reliably separate instructions from data. Everything in the context window reads as potential instruction: the user's message, a retrieved document, the body of an email the agent was asked to summarize. A support bot that resets a password because a convincing chat told it to will just as readily follow a command hidden inside a file it was handed to process. The VPN trick that defeated Meta's geolocation check is the crude version of this. The sophisticated versions, where the malicious instruction is smuggled in through content the agent ingests, are already being documented as the dominant class of agent attack.

  The blast radius is about to multiply

  The Instagram bot could reset passwords, and that's a serious reach, but a bounded one. The agents shipping now are not bounded that way. In the same week Meta disabled the support tool, it launched its Business Agent, which books appointments, qualifies leads, closes sales, takes payments, and connects to systems like Shopify and Zendesk to act on a company's behalf. Run the same confused-deputy logic through a payment API and a CRM and the failure is no longer a stolen account. It is a refund sent to the wrong party, an order rerouted, a price overridden, a customer record edited, each one a legitimate operation the agent was authorized to perform for whoever asked.

  The market is outrunning the security model. Gartner has projected that 40% of enterprise applications will include task-specific AI agents by the end of 2026, up from under 5% at the start of it. Most of those deployments will inherit the same assumption Meta's did, which is that whatever sits at the far end of a privileged action has judgment.

  Why a better model does not fix this

  A more capable model behind the same workflow would have handed over the same accounts with better grammar, which is exactly why the model cannot be the place authorization lives, being the part an attacker controls. The decision to allow an action has to be made outside it, by a policy layer that checks who is actually behind the session before anything runs. Meta's assistant never established that the person it was talking to owned the account before it rebound their recovery email.

  In a couple lines of code, what shipped looked something like this. The agent could call the function, and being able to call it was the whole authorization:

  def add_recovery_email(account, new_email):
    account.recovery_email = new_email      # nothing here ties to the caller
    send_reset_link(new_email)

  The fix is not a smarter model or a better prompt. It is the principal check that was missing, decided outside anything the chat can influence:

  pythondef add_recovery_email(account, new_email, principal):
    if not principal.owns(account):         # who is actually asking, verified
        raise Unauthorized("session not authenticated as the account owner")
    account.recovery_email = new_email
    send_reset_link(new_email)

  
   

   The attacker controlled the conversation, but principal comes from the authenticated session, not the chat, so no sequence of convincing messages can satisfy that line.
  

  Agents should hold scoped, short-lived authority instead of standing access. A token minted to summarize a customer's open tickets should be useless for refunding their last order. That is least privilege, but it has to be enforced per action and per resource, not granted once when the session opens and trusted from then on, because an agent will be talked into reaching for everything its credentials permit.

  Anything irreversible needs a gate the agent cannot drive through. A confirmation the model can satisfy by generating the right words is not a control, just fluff. Payments, deletions, permission changes, and account recovery belong behind a human approval or a hard policy rule, classified by how much damage they can do rather than waved through on the same path as a routine lookup.

  Every action an agent takes should carry its provenance, meaning the principal, the session, and the prompt that produced it, so you can audit what happened and revoke it when something is exploited. Considering that the Instagram attack ran for roughly six weeks, the distance between a contained incident and twenty thousand stolen accounts is often just whether anyone could see, close to real time, that one privileged action was firing again and again for accounts with nothing in common.

  Putting the judgment into code

  None of this is a reason to keep agents away from real systems. They are worth building, and what went wrong at Meta was an ordinary engineering gap, not some property of AI we have to fear. Every fix here is something teams already know how to do: scope the credentials, verify the principal, gate the actions you cannot undo, and keep a record of what ran.

  One habit ties them together. Before you connect an agent to anything that matters, ask what the person in that loop used to check. That judgment was real work, and now it has to exist as code, because the agent will not improvise it for you. Do that, and obedience stops being the liability. An agent that does exactly what it is allowed to do is precisely what you want, as long as you have done the work of deciding what it is allowed to do.

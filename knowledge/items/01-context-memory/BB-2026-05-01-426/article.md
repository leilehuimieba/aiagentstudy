# The permalink problem in AI chat

- BestBlogs URL: https://www.bestblogs.dev/article/c495b41d
- Original publisher URL: https://uxdesign.cc/the-permalink-problem-in-ai-chat-1f1579ec991c?source=rss----138adf9c44c---4
- Source: BestBlogs / UX Collective
- Publish time: 2026-05-25 19:10:58
- Capture route: article discovered from logged-in Chrome/OpenCLI profile `qmvqcrb8` latest article feed page 5; page/content captured from BestBlogs resource APIs
- Extracted chars: 19441

---

Editor’s note: I wrote this article from firsthand experience as a founder and engineer.

         Disclosure: I co-founded AI Toolbox — a Chrome extension that adds per-message bookmarking and full-text search to major AI chat products.

        

       

       
        
         
          
           
            Press enter or click to view image in full size
            
             
            

           

           
            Engelbart’s 1968 NLS could already jump to any individual text element by structural address. Fifty-eight years later, AI chat cannot.
            

            Credit: Frame from “A Research Center for Augmenting Human Intellect”, 9 December 1968. Public domain via the Doug Engelbart Institute archive.
           
          
         

        

       

       
        
         A real review left on the public listing of one of the three major AI chat products this spring:

         
          “I had the perfect answer it gave me yesterday about my tax setup and now it’s just gone. Scrolled forever, can’t find it, and there’s no way to bookmark anything. Lost an hour of work basically.”

         

         It is one of dozens like it. Another from the same week, on a different product:

         
          “Why is there no way to save one message?? I asked it to draft something important, came back later, and the whole thread had gotten so long I couldn’t tell which version was the good one.”

         

         The most valuable text a knowledge worker reads in a workweek, the response to a question they could not have answered on their own, is the only text in 2026 that has no URL. AI chat inherited a messaging-app architecture in which the conversation is the addressable unit and the individual message is an ephemeral transcript line. That decision is not load-bearing. It is downstream of how fast the products shipped, not of how the underlying work actually behaves.

         This is the fifth post in a series I have been writing about design failures shared across the three major AI chat products. The earlier four covered the chat box as default UI, the forgotten conversation problem, the death of the empty state, and the missing undo. All four are downstream of one architectural choice. This one is the choice.

        

       

      

      
       
      

      
       
        
         The valuable text in a workweek has no URL

         In 2026, almost every other category of text a knowledge worker touches is addressable. A tweet has had a URL since Twitter shipped permalinks in 2006. A Slack message has had a “Copy link” affordance since 2014. A Notion block has had a per-block URL since the 2018 rewrite. A Google Docs comment has had a deep link for over a decade. A Linear comment, a Figma frame, a Jira ticket field. Even the cell in a VisiCalc spreadsheet was structurally addressable in 1979. The pattern is older than the web.

         Tim Berners-Lee’s 1998 W3C note on URIs is unusually direct about why this matters: “Cool URIs don’t change. The reason they should not change is simple: so that other people can link to them.” A resource that other people, or your future self, cannot link to is a resource that does not persist in the network of knowledge work. It is alive only inside the application that produced it, and only until the application decides otherwise.

         The AI response in your chat history fails this test on every count. It has no stable URL. You cannot link to it. You cannot send a coworker just the one paragraph that mattered. You cannot bookmark it in your browser. You cannot save it to a read-it-later service. You cannot embed it in a Notion page. You can copy and paste the text, but you have just severed it from its conversation, its model version, its timestamp, and its provenance.

        

       

      

      
       
      

      
       
        
         What other tools made first-class

         The design vocabulary for treating the message as a first-class object is everywhere except in AI chat. Worth listing concretely, because the absence becomes obvious when the comparison is on the page.

        

       

       
        
         
          
           
            Press enter or click to view image in full size
            
             
            

           

           
            Five collaboration tools ship per-unit Copy Link. AI chat ships a Share dialog scoped to the whole conversation, with nothing per message.
            

            Credit: Screenshots by author, composited side by side.
           
          
         

        

       

       
        
         Slack, Notion, Linear, Figma, GitHub, Google Docs, Twitter, Reddit, and Hacker News all converged on the same primitive: the smallest unit of meaningful content in the product has a URL, and the user interface exposes a one-click affordance to copy it. The reasons differ slightly across products. Slack needs it so a teammate can land on the exact message that started the thread. Notion needs it so a block of decision-making can be embedded across pages. Linear needs it so a code review comment can be pasted into a Slack thread without losing context. The underlying property is the same: the unit of value is the unit of address.

         Spreadsheets formalized this earliest. VisiCalc, Lotus 1–2–3, and Excel all treated the cell as an addressable element, and the language of A1 references became the bridge between the cell as visual surface and the cell as durable identity. Bret Victor’s “Magic Ink” reads as a long argument for exactly this: a designed information system makes its interior structure inspectable, addressable, and reachable, rather than collapsing into a single opaque transcript.

         The AI message has no A1 reference. It has no Copy Link menu item. The hover state of an LLM response in May 2026 offers regenerate, copy, thumbs up, thumbs down. That is the affordance vocabulary of a feedback collection form, not of a knowledge artifact.

        

       

      

      
       
      

      
       
        
         The eighty-year lineage that already solved this

         The HCI tradition picked up the addressability problem in 1945 and never let go. Vannevar Bush’s “As We May Think” in the Atlantic that year described the memex as a machine whose central operation was the trail: a named, persistent association between specific items that the user could return to and share. Bush did not describe a search box. He described addressing.

         Twenty years later, Ted Nelson’s 1965 ACM paper coined the term hypertext and introduced what he initially called zippered lists and later called transclusion: every chunk of content has an identity that another document can reference, and the reference is honored at read time. Nelson’s Literary Machines, first published in 1981, treats addressability as the precondition for hypertext, not as a separate feature.

         Three years after Nelson’s first paper, Doug Engelbart sat in front of an audience of computer scientists at the Fall Joint Computer Conference and ran the demonstration that became known as the Mother of All Demos. NLS, his On-Line System, could already jump to any text element by structural address. The mouse and the hyperlink were both there. The point of the demo was that any piece of text in any document was reachable.

         Tim Berners-Lee built the early web on the same foundation. The URI was not a marketing afterthought. It was the primitive that made the entire architecture compose.

         Closer to the present, Andy Matuschak’s evergreen notes treat every individual note as a stable address that other notes can transclude. Maggie Appleton’s Language Model Sketchbook sketches what AI interactions could look like if the unit of address were the idea instead of the chat. Amelia Wattenberger’s 2023 essay on why chatbots are not the future of interfaces frames the same point from a different direction: surfacing structure is the work, the chat is the avoidance of the work.

         Eighty years of writing on this question, by the people who designed the substrate the AI products are running on top of. The AI products did not lose that argument. They did not have it.

        

       

      

      
       
      

      
       
        
         What the industry shipped instead

         It would be unfair to claim the products ignored sharing entirely. They did ship something. Worth describing what, because the gap between what shipped and what addressability requires is the diagnostic.

         
          
           Get Adi Leviim’s stories in your inbox

          

          
           Join Medium for free to get updates from this writer.

          

          
            
            
             
              
             

            
 
           
           
            
             Subscribe
            

           

           
            Subscribe
           

          

          
            
            
              
              
               
               
             
            
 
            
             Remember me for faster sign in

            
 
           
          

          

         

         ChatGPT lets you share a conversation. Clicking the share button creates a snapshot at a URL on the form chatgpt.com/share/[id]. The snapshot is the whole conversation up to that moment, not the message you wanted to share. The share UX got simpler in 2026: clicking the icon now copies the link directly and shows a snackbar reading “Anyone with this link can see this conversation.” The product iterated on share friction without ever introducing per-message scope as an option. Pinning, which arrived in early 2025, pins the entire conversation in the sidebar. The OpenAI developer community has had an open feature request for per-message bookmarks accumulating upvotes since 2023, with no native shipping in sight.

         Claude offers the same primitive at the same scope. The share menu produces a chat-level link. Projects, added in 2024, organize entire conversations into flat workspaces with shared instructions and files. There is no per-message URL, no per-message save, no per-message label.

         Gemini is the partial counterexample, and it is worth being honest about it. In 2024 Google shipped a share affordance under each response that creates a URL on the form g.co/gemini/share/[id] pointing at just that response. Two caveats neutralize most of what looks like first-class support. The share URL is a snapshot at a different domain, not a permalink to the message inside the user's own conversation. And the link expires automatically after about six months. The original message in the original conversation history continues to have no addressable URL. What Gemini shipped is closer to a screenshot-as-a-service than to addressability.

         All three products converged on the same misreading of the problem. The user does not want to make a public snapshot. The user wants a URL that points back to a specific message in their own history, that survives, that they can bookmark in their own browser, paste into their own notes, return to in a week. The shipped feature solves the rare case (showing a stranger an output) and ignores the common case (returning to your own work).

        

       

       
        
         
          
           
            Press enter or click to view image in full size
            
             
            

           

           
            All three products ship a share affordance. Only one operates per message, and even that one points away from the message’s home.
            

            Credit: Screenshots by author, composited side by side.
           
          
         

        

       

      

      
       
      

      
       
        
         What users do when the primitive is missing

         When a tool is missing the primitive a user needs, the user does not stop. They build the workaround. Two workarounds are visible everywhere.

         
          “Would pay for this if I could just star individual responses and get back to them in one tap. Right now my only option is copy-pasting everything into Notes.”

         

         The Notes reflex. Cmd+A inside the response, Cmd+C, alt-tab to Apple Notes or Obsidian or Notion, Cmd+V, save. The user has just manually re-implemented per-message addressability outside the product. The address is now a note in a different application.

         
          “Long chats are unusable for going back to. I know the answer I want is in here somewhere around the middle but I have to scroll past hundreds of messages every time.”

         

         The scroll-and-pray reflex. Open the conversation, scroll, hope the eye recognizes the shape of the paragraph. There is no addressable destination to navigate to. The user is performing a linear scan because the structural one is unavailable.

        

       

       
        
         
          
           
            Press enter or click to view image in full size
            
             
            

           

           When per-message bookmarking is added as a third-party retrofit, two thirds of paid users immediately start using it, with a heavy power-law tail. The shape of the curve is what missing primitives produce when the workaround finally arrives. Credit: Chart by author. Data drawn from anonymized aggregate usage across paid users in May 2026.
          
         

        

       

       
        
         Across roughly twenty thousand paid users of a Chrome extension I co-built, sixty-three percent have created at least one per-message bookmark, the average active bookmarker holds fourteen bookmarks, and the top eight percent of users hold sixty percent of all bookmarks. Seventy-four percent of users who upgrade to a paid tier cite saving individual messages, by bookmark or by label, as the reason. Per-message saving is the third most requested feature in support tickets, after bulk export and folder organization. A 23 percent higher adoption rate among users of one of the three products, the one whose typical output is longer and more deliberative, is the strongest signal in the data: the more the product pushes users toward producing real artifacts, the more the missing primitive hurts.

         When three of every four paying users tell you that the reason they are paying is to make individual messages first-class, the absence of that primitive in the native product is the design failure. Not a missing feature. A primitive omission that the user is willing to pay a third party to fix.

        

       

      

      
       
      

      
       
        
         What first-class messages would look like

         A messaging-app architecture treats the conversation as the addressable unit. A knowledge-work architecture would treat the message as the addressable unit. Concretely, that means a small list of properties that the three major products do not currently ship.

         Every message would have a stable URL that points to its position in the user’s own conversation history. Not a separate snapshot domain. Not an expiring link. A regular URL on the product’s own host that, when revisited a year later, returns to that message in that conversation. The Slack pattern, scaled to AI chat.

         Every message would expose a Copy Link affordance in the response menu, alongside the existing copy, regenerate, and reaction controls. One click. The vocabulary every other collaboration product converged on years ago.

         Every message would be a bookmark target, a label target, and a search hit. Searches would return addressable hits rather than “the conversation contains this.” Bookmarks would survive conversation rename and archive. Labels would aggregate across conversations into a cross-history view, the way Linear labels aggregate across projects.

         Cross-conversation linking would follow as the natural consequence. The model itself could begin to cite prior responses by URL, the way Andy Matuschak’s evergreen notes link to one another, the way a research paper cites a section of another paper. The forgotten conversation problem I wrote about earlier in this series would shrink dramatically the day the message had a URL, because the user would have somewhere to write the URL down.

        

       

       
        
         
          
           
            Press enter or click to view image in full size
            
             
            

           

           
            The five surfaces I have written about in this series share one architectural root. Correct the root and four of the five lose most of their gravity. 
             
Credit: Diagram by author.
           
          
         

        

       

       
        
         The chat box, the empty state, the missing undo, the forgotten conversation, the missing permalink. Five surfaces, one decision. Treat the conversation as the addressable unit and you inherit all five problems. Treat the message as the addressable unit and four of the five lose most of their gravity. The order of the work is not five separate fixes. The order of the work is the architectural correction, and the surface fixes fall out of it.

        

       

      

      
       
      

      
       
        
         Key takeaways

         
          The most valuable text a knowledge worker reads in a workweek is the only text in 2026 that has no URL. Every adjacent collaboration tool, from Slack to Notion to Figma to Linear to Twitter, treats the smallest unit of meaningful content as addressable.

          AI chat inherited a messaging-app architecture in which the conversation is the addressable unit and the message is an ephemeral transcript line. That decision is downstream of shipping speed, not of how the work actually behaves.

          Eighty years of HCI lineage from Bush, Nelson, Engelbart, Berners-Lee, and Matuschak treats addressability as the primitive that makes computers augment thought. The AI products did not lose that argument. They did not have it.

          What the products shipped (conversation-level share, expiring snapshots at separate domains, per-conversation pinning) solves the rare case of showing a stranger an output and ignores the common case of returning to your own work.

          The five design failures I have written about in this series, including this one, share an architectural root. Treat the message as the addressable unit, and four of the five lose most of their gravity. The fix is one decision, not five.

         

        

       

      

      
       
      

      
       
        
         Follow me on Medium for more essays on AI UX and the design reality of building for global audiences.

        

       

      

      
       
      

      
       
        
         About the author: Adi Leviim is a full-stack engineer and product builder with 7+ years of experience shipping commercial software to global audiences. He writes about AI UX, the design reality of building for millions of users, and the gap between AI demos and production AI. Follow him on Medium for essays at the intersection of engineering and design.

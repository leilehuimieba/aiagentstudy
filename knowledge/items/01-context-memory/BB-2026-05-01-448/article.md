# I Spent May Evaluating Different Engines for OCR

- BestBlogs URL: https://www.bestblogs.dev/article/aba895ac
- Original publisher URL: https://towardsdatascience.com/i-spent-may-evaluating-different-engines-for-ocr/
- Source: BestBlogs / Towards Data Science
- Publish time: 2026-06-04 00:30:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 1; page/content captured from BestBlogs resource APIs
- Extracted chars: 19430

---

Not all documents were supposed to be read by a machine. Old hotel invoices, bank statements, payslips, loan applications, medical bills, customs forms, court filings, work orders.

  Most companies use free tools alongside paid APIs to try to convert these documents, and if you want structured output, APIs like Textract Structured run you up to around $65 per 1k pages.

  In the last few years, though, a lot of new options have appeared: smaller open-source vision models specialized for OCR, general vision-language models, and document parsing tools like LlamaParse — changing what’s possible and the cost thereof.

  
   
   Rough timeline—we see more OCR solutions after 2024 | Image by author
  
  So it felt like a good time to do my own experiment to test some of these against documents of varying difficulty.

  I scouted 93 docs that could act as a proxy for what companies use OCR for — handwritten notes, tables, financial legacy docs, scanned invoices, receipts, charts, old newspapers, tax forms — then ran them all through 14 different engines.

  The idea was to see how they handled two things: text recovery and the ability to preserve useful table structure.

  The main question I wanted answered: do you really need to pay $65 for 1k structured pages, or can you slice that down to a fraction? And does the specialized models win over the general ones?

  When doing experiments like this you always find quite a few strange things, which I’ll cover too. But to answer that main question I’ll take you through what OCR is (skip if not new), the economics, the test, some of the results, and what else this showed me.

  Note: I did not test full field extraction, since that is harder to compare cleanly across fourteen engines.

  TL;DR

  There is no single best OCR engine. OCR is a routing problem.

  For clean high-volume documents, Tesseract is still hard to beat because it is free and fast. For mixed production documents, Gemini Flash was the best all-rounder in this test. For tables, Mistral OCR looked like the cheaper structured option.

  The smaller specialist models looked good inside their comfort zone, but failed harder at documents they hadn’t seen. So, for high-stakes or messy documents, it makes sense to escalate to a larger model.

  The main takeaway is economic: don’t pay for expensive structured OCR when the document does not need it. Classify your docs, test engines on your own data, and route based on cost, accuracy, structure, and failure tolerance.

  Benchmarks are useful for discovery, but they will not tell you what works on your documents.

  Explain the OCR space to me

  OCR (Optical Character Recognition) is how a machine turns a picture into machine readable text. Simple in principle, and for easier docs mostly solved, but harder when things become more human. 

  Just to give you a quick overview, older OCR found text on a page, sliced it into characters, and matched each one against a library of known shapes. Tesseract has done this since the 1980s. 

  Modern OCR however (including newer versions of Tesseract) usually uses a neural network that looks at the whole page at once and outputs the document as text. So, if your document is a clean PDF or a high-quality scan in a standard font, OCR is mostly a solved problem. 

  It stops being solved the moment things get messier: photographed receipts, handwritten notes, weird graphs and charts, dense financial tables, or scanned tax forms and loan applications.

  Companies need this done well for obvious reasons, as it’s something every downstream system acts on. The better OCR gets, the more paperwork becomes something a system can reason over instead of something a human has to read by hand. 

  There is also the fact that if we feed AI systems badly parsed docs, everything after it will be hard to trust. 

  I’m all about economics, so this space caught my eye once I saw how much money is being poured into it. The Intelligent Document Processing (IDP) market is projected to grow to somewhere between $20 billion and $90 billion by the early 2030s, depending on which analyst you ask. 

  Probably driven by companies paying $15–25 per invoice in manual handling costs.

  And because I stay close to the tech world, I’ve watched a wave of specialized small OCR models ship over the past year (mostly Chinese), now being used by developers everywhere. 

  
   
   Some of the OCR specialized models released last year | Image by author
  
  Which raises the question I wanted to test: can the small open-source models actually do the work the expensive APIs charge for or should we actually look towards the general vision models to handle OCR too?

  Skip the next section if you want to understand what this experiment showed. I have to go through the test setup first.

  The docs, the engines, and the metrics

  This experiment comes down to three questions: what engines we used, what docs we tested with, and how we decided who won.

  For the engines, I wanted a lineup that covered all the choices I talked about, this meant: old and new, open and closed, local and cloud, specialized and general.

  Tesseract became the classical choice. It runs locally and is very fast. Then I added two document-parsing pipelines: Docling and Marker. Docling is slower but runs on CPU, Marker is open-weight but needing a GPU to run fast, which shows up later in the price.

  Then for the new wave of specialized open OCR models: GLM-OCR, PaddleOCR-VL, DeepSeek-OCR, and MinerU 2.5 (a borderline case, really a pipeline with a VLM inside). I picked them off OpenDataLab’s OmniDocBench leaderboard, where they ranked first, second, fourth, and fifth.

  I hosted them on Modal and served the applicable ones with vLLM, batching to speed things up. I counted the scale-up time when measuring latency later.

  I also added one closed purpose-built model, Mistral OCR, which I’d heard good things about.

  On the open side, I used Qwen3-VL (8B, from Alibaba), also hosted on Modal with the rest of the smaller models. I should flag that I gave it a plain transcription prompt rather than the optimized serving setup it was designed for, so I may not have given it a fair shot.

  On the closed side, for the general models, I picked Gemini Flash 3.1 Lite (currently first on the IDP Leaderboard, the western counterpart built on OmniDocBench v1.5) and Claude Sonnet 4.6, at sixth.

  For the cloud document services: LlamaParse and AWS Textract, in both its text and structured forms. Structured Textract can do far more than I asked of it. I only tested its text accuracy across the board and its table extraction against eight of the other engines.

  Let’s turn to the documents. I picked seventeen document types that were either easy, medium, or hard. Ninety-three files in all. 

  Easy was the stuff OCR mostly solved years ago: clean invoices and receipts. Medium came largely from the OmniAI OCR Benchmark dataset: bank statements, medical notes, photographed receipts, shipping documents, tax forms.

  Hard was chosen when things turned more difficult: charts, forms, handwritten notes, weirdly scanned financial tables, legal papers, newspapers, and old legacy reports. 

  
   Some docs were really quite difficult, such as the legacy scanned docs you see below, and this was just because I was curious if some could actually do it well.

  

  
   
   
    Messy legacy reports we ran through an LLM judge sourced from the Industry Documents library  under fair-use license— every engine did badly according to the judge (except Gemini Flash) maybe some bias carried through there.
   
  
  Some of these images came with gold ground truth and some didn’t, and the ground truth I did have wasn’t always consistent, some files labeled correctly, some not, which is why we should briefly cover the metrics too. 

  Since every engine emits different markup, the usual scoring didn’t quite fit. One might pick Precision and Recall for a case like this. 

  Precision looks at how many of the OCR output’s words actually match in the GT while Recall measures how many times each GT word was captured.

  Precision would punish engines that emit markdown structure the GT doesn’t contain, furthermore the GT sometimes skipped labels entirely which would punish the engine unfairly. Recall would measure the words but punish the frequency. 

  So, I added on a third metric called Coverage. I just wanted to measure how much of the ground truth shows up somewhere in the engine’s output. It isn’t perfect, but it tells me whether an engine caught most of what mattered, without penalizing it for gaps that were the ground truth’s fault rather than the engine’s.

  For the documents with no gold ground truth at all, I fell back on an LLM judge, with Gemini 3 Pro as the base model and anyone who’s used one knows this is fickle business.

  What this experiment showed

  We mapped every document against the Coverage metric to build a scatter chart, and tracked latency on a separate chart. The thing a generalized chart can’t tell you though is that the engines failed in different ways.

  The bubble graph showed that most engines fall somewhere in the middle top, with two outliers on both sides of it.

  
   
   All images have been created from the result of the experiment
  
  Gemini Flash and Textract Text did very well across the board with some edge cases. The specialized models all fell below the general models and specialized APIs. Sonnet performed the highest but also with a steeper price tag.

  This may not have been a surprise as the test set was highly unusual. Some of the specialized models may not have seen many of them. Furthermore, this test was on English documents and most of these smaller models have Chinese origin. 

  When we also mapped latency, some of the models turned out to be very slow, but again most wound up somewhere in the middle. 

  
   
  
  The outliers here were: Tesseract, Claude Sonnet 4.6, and Docling. Tesseract was incredibly fast compared to all other engines. It should be your go-to for easier documents. 

  These graphs generalise across all the documents, but I did separate the results based on the type and difficulty level.

  To start with the easy docs. On invoices, every engine did well, Tesseract especially. Receipts knocked everyone down a little.

  
   
  
  The one outlier was Docling, which struggled across a lot of the categories, even the easy ones.

  When I looked into the Docling failures I found things like Ifjointreturn instead of “joint return,” and worse, strings like City,wrostffielfouaveaoreignadresalcomletacesb. DeepSeek also missed key details here like invoice number and date, which is why its number sits low.

  The same pattern holds in the medium category, though that’s where PaddleOCR started degrading on specific types: bank statements, shipping, tax forms. Tax forms were hard for everyone, but PaddleOCR and Docling wound up at the bottom. 

  Textract was the best engine on a lot of the medium types, along with Claude Sonnet 4.6 and Mistral OCR.

  On the harder types, Gemini Flash started rising, beating Textract on forms and handwritten notes, matching it elsewhere. It did remarkably well everywhere. Tesseract and Docling failed hard on handwritten, and forms were tough for them too. 

  Almost all the specialized models didn’t pull through on these harder docs except on financial tables, where they held about even.

  For the docs with no ground truth (newspapers, legal, reports, some scanned legacy documents) we used an LLM judge. These are genuinely hard, so it’s no surprise almost everyone failed on the reports and newspapers. 

  Except Gemini Flash that did reasonably well everywhere. Mistral OCR also did well for newspapers. Gemini Flash won everywhere with the judge, though we used Gemini Pro as the judge so take that with a grain of salt (but I did double check myself).

  Before rounding off: I also ran 8 engines against Textract Structured to see how they did on financial tables, extracting an HTML table. I used Textract Structured’s output as the ground truth for TEDS (Tree Edit Distance Similarity) and scored Claude Sonnet 4.6, LlamaParse, Mistral OCR, Gemini Flash, Marker, MinerU, DeepSeek-OCR, and Docling against it. 

  
   
  
  Mistral OCR, and LlamaParse, and Sonnet did very well while being much cheaper. I also ran it through an LLM judge, and the winners were the same three (even before Textract Structured) though I’d want to build that test better before I fully trust it.

  
   
  
  Now, let’s talk about what it costs to scale this up, and what would make sense where.

  When does what make sense

  Let’s run through what it costs to scale up with these engines, and then based on these docs what you would chose where. 

  First, the cost of using these engines vary wildly, as you saw before. Sometimes it helps to see the cost not just for one document, but thousands up to a million. 

  
   
  
  We’re self-hosting on Modal, so these costs come from actual usage there. You can run locally, but my computer wouldn’t allow it and I didn’t want to try it. 

  If you were to just use one engine that handles both easy and hard documents, I would think you wound up with a bigger bill than necessary. Using Textract Structured for any documents that are not needed would hand you a bill of $6.5k per 100k docs. 

  I do wonder how many companies go the easy way here and pick the expensive options for easy as well as hard docs and leave a lot of money on the table. 

  The key idea to take with you here is that there’s no single best engine for every use case, it depends on document type, privacy, table structure, failure tolerance, cost, and so on.

  For the docs we have here, Gemini Flash 3.1-Lite is a clear winner. This one was correct from looking at the leaderboards. Mistral OCR did well on structured tables while staying cheap. Claude Sonnet 4.6 did very well too, but it’s very slow and expensive comparatively. 

  Docling is so very slow on my laptop. I’m sure there are ways to speed it up, but it also failed in ways that make it inherently unstable (still a small test though). 

  The specialized OCR models were a bit of a headache, especially on English docs; I saw output errors in Chinese that I’ll cover in a bit, so I wonder if that’s part of it. 

  Textract is a stable choice, but structured buys you almost no additional text accuracy so if you’re paying that steep markup for structured output, make sure you actually use it. I’m guessing it’s a pretty good business model for them.

  So, in general for this very small test: for clean, high-volume print, just use Tesseract. For general heterogeneous production, go Gemini Flash. For a cost-floor with table structure, test Mistral OCR. For high-stakes docs, route to Sonnet or a larger model.

  Since everyone did well in different ways you’ll have to contact me for specifics but if you need to go private it may be worth it to look at fine-tuning a model on your docs. Or, use a small specialized model and escalate on failures. 

  Let me just quickly talk about some things that stood out after doing this experiment.

  Other stuff I should mention

  A handful of things surfaced from this that are worth pulling out on their own. 

  First, if you want to understand how a model or engine will do on your docs, the only way is to test on those docs, you can’t rely on benchmarks to tell you. This was the number one insight this showed. OCR usefulness depends on your own document mix, layouts, languages, scans, tables, handwriting, and failure tolerance. 

  Do not pay for structure if you don’t need it. I wonder how many are using certain APIs or models for a reason they can’t justify. Map the cost to understand what you are losing by not using the correct engine for the documents.

  The specialist models, as mentioned before, have sharp boundaries. This is obvious, they can be excellent inside their training distribution but fail outside of it. This is where the general models will win. 

  If you want to fine-tune it may help, but only if the stream is stable as it will also fail if it is constantly introduced new document classes.

  Lastly, the failure modes told us more than the averages. 

  PaddleOCR had repetition loops, column-merging, fallback into Chinese textbook template text like 书名:___ repeated hundreds of times. While Docling has character errors, word-merging, and column misalignment all stacking together.

  DeepSeek OCR has chart blindness and empty outputs on some docs. Tesseract did fine on clean docs (as mentioned) but failed on photo/handwriting altogether outputting garbage. 

  Caveats to consider

  Before we round up, let me cover how this test is ultimately imperfect by naming the issues in the GT, the metrics used, and the sample size.

  I covered this in one of the section above, but the ground truth differs between documents depending on the dataset where they were found. In general tokenization artifacts can make correct OCR look worse than it is.

  Most engines have different formats, some return plain text, some markdown, some HTML/rich markdown and it’s hard to generalize across all.

  We are using Coverage, and then also some other metrics, but these aren’t perfect. Coverage won’t charge the engine if it outputs too much text or the structure of it is off. Though I did find that for the engines that failed, they did so at the start or mid-way through rather than at the end.

  This means it’s useful for ranking but not a perfect way to score.

  LLM judges are not neutral truth: I’ve covered this in the past, but they are biased and very prompt sensitive. 

  Then I just need to say that this test is interesting but not that big, the sample size is way too small to use this as a factual study. But, I don’t fully trust these metrics nor the judge so it was the only way for me to be able to double check the results on my own without this turning into a year long project.

  So, this test is useful for direction and getting a sense of what works, but for getting a sense of your use case, you need to run it through with your specific docs. 

  Lastly, latency and reproducibility is unstable. Serverless cold starts make timing noisy, and API models can silently change over time, so exact reproduction is hard.

  
  Like always with these articles, it takes quite a bit to do an experiment like this but I don’t just do it for content, I do it because I’m genuinely curious. 

  What it looks like though is that OCR seems to be a routing problem, and perhaps an evaluation problem. Classify your docs and run them through several engines, then try to build a decent router and validator in your pipeline to escalate failures and then log the costs. 

  If you need to get the full results from this experiment or you want me to run it through your docs, get in touch. 

  You can follow my writing on Medium, my website or connect with me via LinkedIn. 

  ❤ 

  All datasets used in this benchmark are publicly available and sourced from HuggingFace. Licenses include MIT, CC-BY-4.0, and fair-use frameworks (UCSF Industry Documents Library) covering research, scholarship, and education. No source documents are reproduced — datasets were used solely as evaluation inputs to measure OCR engine performance.

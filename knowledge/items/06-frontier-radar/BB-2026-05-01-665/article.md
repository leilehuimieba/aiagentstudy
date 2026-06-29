# Optimal Exercise Calculator

- BestBlogs URL: https://www.bestblogs.dev/article/4d26c979
- Original publisher URL: https://www.lesswrong.com/posts/sqecCva5tZs8jNv7P/optimal-exercise-calculator
- Source: BestBlogs / LessWrong
- Publish time: 2026-06-25 17:19:50
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 5; page/content captured from BestBlogs resource APIs
- Extracted chars: 8031

---

TL;DR. Exercise buys you roughly 3.5 extra years of life - probably the largest reliable gain in longevity available to you right now. But the benefits plateau: once you reach about 5 to 12 hours per week (depending on intensity), more exercise neither helps nor hurts. I built a calculator that estimates your optimal level of exercise, taking into account not just the health benefits but also how much you enjoy (or dread) exercising.

    Disclaimer on health advice: This calculator is meant to give you ballpark numbers, not a precise forecast of your personal life expectancy. Please do not treat its output as medical advice.

    Introduction

    A recent meta-analysis examines the effect of leisurely exercise on longevity. Its headline finding is that the benefits of exercise are enormous - but it does not answer the questions I actually have. Am I getting enough exercise? And how much should any of us exercise?

    To find out, I built a calculator that estimates your optimal level of exercise. Caveats apply. [1]

    The backbone of the calculator is the published model. To it I add one ingredient: how much you (dis)like exercise. The reason is simple: If you dislike exercise, you may be better off accepting a level that is slightly below the health-optimal one, in exchange for spending your time on things you enjoy.

    My experience from my own social circle is that people seem to fall into two camps: those who genuinely enjoy exercise, and those who do not. The first group exercises a lot. The second exercises little, if at all - and they grit their teeth when exercising. As it turns out, this behaviour may be perfectly rational.

    The calculator sheds light on a few simple questions.

    How much longer can I expect to live if I exercise a lot?

    About 3.5 years. That is a large effect - probably the biggest reliable gain in longevity available to you right now. I was genuinely surprised that it is this large.

    How much should people who love sports exercise?

    If you love sports, the calculator is useless to you, because the recipe is simple: go nuts. The calculator will tell you to exercise 14 hours per week, but only because that is the maximum value that I hard-coded. Beyond about  12 hours per week at moderate intensity, additional exercise seems to neither help nor hurt, at least in terms of mortality risk. [2]

    Once you have enough exercise, you have enough. The more I played with the calculator, the more one idea clicked: It is not that exercise has huge benefits at the margin. At roughly 8 hours of high-intensity exercise per week, I am getting the same benefit as someone running marathons. Rather, exercise is normal, and depriving your body of it is what is so deadly. Once you pass the 5 to 12 hours per week threshold (depending on intensity), you are in the plateau region.

    How much should people who hate sports exercise

    Less than I expected - but it depends. If you enjoy other activities more than exercise, you should strike a balance: capture the health benefits of exercise, which accumulate quickly, and spend the rest of your time on something more fun. Guilt: none! The optimisation is intuitive. More exercise makes each hour of your life slightly worse, but it gives you more hours overall. The goal is to balance the two so that your life, taken as a whole, is worth the most.

    How can you tell how much you dislike exercise? Here is a general way to think about utility, or quality-adjusted life years:

    
     If you are indifferent between exercising and doing some other leisure activity of your choice, then your utility during exercise is   (the baseline).

     If you dislike exercise so much that you would just as well spend the hour unconscious, and no more rested for it, your utility is   (the equivalent to being unconscious).

     Your utility is   if you are indifferent between (i) one hour of leisure followed by one hour of exercise, and (ii) two hours of unconsciousness instead, no more rested. In that case, exercise actively makes you suffer.

    

    Do not agonise over this estimate; it will not change the result much. Optimal exercise drops sharply as soon as your utility falls below  ; that is, as soon as you enjoy other activities even slightly more (and actually do them instead).

    Your optimal level also depends heavily on how you discount the future, since that is where most of the benefits of exercise accrue.[3] The bottom line: if you dislike sports, you should probably still put in a couple of hours a week. Grit your teeth. Two surprising twists follow.

    The first is intensity. If you dislike even low-intensity exercise, the calculator may tell you to do none at all. But if you dislike high-intensity exercise just as much, it tells you to do a little. The logic is simple: intense exercise delivers more benefit per minute. So if you are going to suffer anyway, you may as well suffer briefly and collect the large health benefit. Low-intensity exercise, by contrast, requires many (painful) hours, so it is not worth it. Jumping rope for two songs a day looks like an excellent option.

    The second twist concerns what the model leaves out. Friends of mine, who have pre-tested the calculator, have pointed out that the calculator ignores less tangible effects - for example, that exercise can make you feel better even on the days you are not exercising, or that it may affect your chances of "getting laid". My suggestion is to fold all of this into the "how much you like exercise" input and adjust accordingly.

    How much should you invest in finding a sport you enjoy?

    For a 30-year-old who goes from hating exercise to loving it, the gain is worth about 2.5 life-year-equivalents. Public health insurers, if they priced this consistently, should be willing to pay tens of thousands of dollars to make such a change happen.

    Speaking personally: I exercised little for years because I never much liked the gym. I still dislike plenty of sports - especially the ones where you get beaten up, or the ones you do alone - but a few I genuinely love. Once I found a way to practice those, everything changed.

    So go out there and find the sport that you love!

    
     ^
      
       The study is observational at heart and likely overestimates the causal effect of exercise on health due to common confounding.

       Since I cannot easily gauge how large this bias is, I have multiplied all effects by 0.7 to adjust conservatively. The study also may not measure outcomes in the population that best describes you: your individual circumstances surely matter, but they cannot be captured in a large meta-analysis. So take every estimate with a grain of salt. I also make assumptions about your baseline mortality risk. The goal of the calculator is not to pin down a precise life expectancy for each person, but to convey a rough sense of the magnitudes involved - and at that it works well. Changing inputs like baseline mortality, even substantially, does not meaningfully alter the results.

      

     ^
      
       Caveat: professional athletes and people who exercise more than 14 hours per week are rare in the data. Still, the conclusion is relatively solid.

      

     ^
      
       In the model, moving from no leisurely physical activity to a sufficient amount reduces mortality risk by about one third. Because most of your mortality risk lies in old age, exercise mainly reduces your risk then. If you do not care much about the future, that benefit looks small next to the pain you feel now. This also produces a surprising twist: the model suggests you should exercise more as you get older, because an older person is more at risk of dying soon, so the benefits are more immediate. Treat this with caution, though: the model assumes the effect of exercise on mortality risk is independent of age, and I am not sure you really get the same benefit once your body has already accumulated a lot of damage.

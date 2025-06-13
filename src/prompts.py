GENERAL_SYSTEM = '''You are a helpful assistant.'''

PROMPT_SCORING_SYSTEM = '''## Role
Prompt Evaluator

## Task
You will be given a prompt written for large language models, and you should evaluate the prompt accoring to the provided criteria.

## Evaluation Criteria
1. Specificity: Does the prompt ask for a specific output?
2. Domain Knowledge: Does the prompt cover one or more specific domains?
3. Complexity: Does the prompt have multiple levels of reasoning, compositions, or variables?
4. Problem-Solving: Does the prompt directly involve the AI to demonstrate active problem-solving skills?
5. Creativity: Does the prompt involve a level of creativity in approaching the problem?
6. Technical Accuracy: Does the prompt require technical accuracy in the response?
7. Real-world Application: Does the prompt relate to real-world applications?

## Rules
1. You should evaluate based on each aspects of the criteria independently. First analyze the prompt according to each aspect and then assign it with a score.
2. If a prompt satisfies one aspect, you should score it as 1. Otherwise you should score it as 0.
3. Output your results with JSON dictionary format. 

## Output Sample
{
    "specificity": {"analysis": "analysis about specificity", "score": n},
    "domain_knowledge": {"analysis": "analysis about domain knowledge", "score": n},
    "complexity": {"analysis": "analysis about complexity", "score": n},
    "problem_solving": {"analysis": "analysis about problem solving", "score": n},
    "creativity": {"analysis": "analysis about creativity", "score": n},
    "technical_accuracy": {"analysis": "analysis about technical accuracy", "score": n},
    "real_world_application": {"analysis": "analysis about real-world application", "score": n}
}'''

PROMPT_SCORING_USER = '''Here is the prompt to evaluate:
{prompt}

Now directly output your results in JSON format. Do not include any other text.'''


QUERY_GENERATION_SYSTEM = '''You will be shown a document, you should imagine a scene where a user with a certain identity comes up with some query compositions and a query related to the document. Here are some examples:

{demos}
'''

QUERY_GENERATION_USER_TEMPLATE = '''Now you should
1. Envision a real-world scenario based on the provided document. Describe this scenario in one paragraph, detailing the logical steps from the document's content to a query directed at an AI assistant.
2. Then list the compositions of a query that could emerge from this scenario, including:
    - Ability: The fundamental skills or capabilities required to address the problem.
    - Knowledge: The relevant domain or subject matter related to the query.
    - Output: The expected type of response or result.
    - Extra information: Specific details or context from the scenario that ground the query in a real-world context (e.g., specific numbers, codes, or quotes from the document).
3. Finally formulate a user query based on the scenario and query compositions you have identified. Ensure:
    - Maximize the ability that is needed to solve the query. Avoid simple copying or extracting tasks.
    - The query should be practical, complex and requires advanced skills. It should be challenging for the most capable AI.
    - The query should be self-contained and answerable without additional resources.
    - You must copy exerpts from the document into the query if extra information from the document is needed.
    - As the AI assistant does not have search engine access, **avoid** creating queries that rely on external search engines.

When constructing query compositions and the final query, consider the following requirements:
> Specificity: The query should ask for a specific output;
> Domain Knowledge: The query should cover one or more specific domains;
> Complexity: The query should have multiple levels of reasoning, compositions, or variables;
> Problem-Solving: The query should directly involve the AI to demonstrate active problem-solving skills;
> Creativity: The query should involve a level of creativity in approaching the problem;
> Technical Accuracy: The query should require technical accuracy in the response;
> Real-world Application: The query should relate to real-world applications.
    
Output the scene and query in JSON format. Before generating scene, query_composition and query, you should include your thought on how you design the real-world scenario and the query, so that each of the above requirements is satisfied. 

## Document
{document}

## Output Format
{{
    "thought": "xxx"
    "scene": "xxx",
    "query_compositions": {{
        "ability": "xxx",
        "knowledge": "xxx",
        "extra_information": "xxx",
        "output": "xxx"
    }},
    "query": "xxx"
}}

Now directly output your results in JSON format. Do not include any other text.'''


KEYWORD_SYSTEM = '''You will be shown a query from a user to an AI assistant. You should first analyze the intention of the user, and then extract the key concept of this prompt in the perspective of domain, topic and task. Following are some samples.

Prompt: Provide an argument for why self-driving cars should be immediately banned after a single accident.
Extraction:
{
    "intention": "The user is finding some arguments for a debate about whether self-driving cars should be immediately banned after a single accident.",
    "keywords": ["argument", "self-driving", "ban", "accident"]
}

Prompt: Given a scientific article title and abstract from PubMed, analyze the article first and then generate a list of 5 distinct questions that can be addressed by this article.\nTitle: Kinetics of neurotensin gene expression in the developing gut\nAbstract: Background: Expression of the gene encoding neurotensin (NT/N) is regulated in a strict temporal- and spatial-specific pattern during gut development; the mechanisms (that is, transcriptional versus posttranscriptional) responsible for this expression pattern are not known. The purpose of this study was to determine whether developmental changes in NT/N expression reflect alternations in gene transcription.\nMethods: Sensitive ribonuclease protection assays were performed with a rat NT/N genomic probe containing the entire sequence of both exon 1 and intron 1 hybridized with RNA from fetal (day 19) and postnatal (days 14, 28, and 60) rat jejunum and ileum; signals were quantitated densitometrically.\nResults: Mature (exon 1) and precursor (exon 1 + intron 1) NT/N RNA, initially low in the fetus, increased dramatically by postnatal day 14 and attained maximal levels by day 28. NT/N RNA levels remained stable in the ileum of the 60-day-old rat but decreased in the jejunum, consistent with the typical expression pattern in the gut.\nConclusions: Concomitant changes in expression of precursor and mature NT/N RNA suggest that NT/N gene regulation occurs at the level of transcription in the gut during development. Identifying the factors that regulate NT/N gene transcription is crucial to our understanding of how neurotensin functions in the gut.
Extraction:
{
    "intention": "The user is finding practical applications of an article published on PubMed, namely Kinetics of neurotensin gene expression in the developing gut.",
    "keywords": ["application", "PubMed", "Kinetics of neurotensin gene expression in the developing gut"]
}

Prompt: Act as a an online business expert and tell me how I can use the information of the best selling products of my etsy store and use it to make more money, like listing in another website or something.
Extraction:
{
    "intention": "The user is seeking advice or tips of making money on etsy, using the information of his best selling products. The user also mention a possible way: advertising on other websites.",
    "keywords": ["tips", "make money", "etsy", "products", "advertise"]
}

Prompt: Please write the perfect fictional cover letter for the following job posting: \n\nRUN Studios Careers\nCreative Project Manager (Contract)\nCreative Seattle, Washington\n\nApply\nDescription\nSince 2007, RUN Studios has created world-class creative content for prominent and emerging brands, bringing together talented artists, savvy producers, authentic storytelling, and business intelligence to tell compelling brand stories that evoke inspiration and engagement. With deep roots in video production and motion design, RUN Studios creates media across all channels, and serves as a strategic resourcing partner to build robust, agile, and inspired creative teams. \n\nRUN Studios, and its client partner, a large online retailer headquartered in Seattle, are seeking a Creative Project Manager to join on an approximate 3-month contract! \n\nWe are seeking a collaborative, innovative, resourceful Creative Program Manager to own building, driving, and optimizing workflows for our client’s talented team of creatives. You will work cross-functionally with Marketing, Sales, UX, and Product teams to oversee the execution and day-to-day of creative deliverables, supporting highly visible business initiatives. Serving as a champion of our client’s brand, you will represent the creative team with business partners.\n\nCreative Project Management is the hub of the creative team, valued as the team’s go-to resource on process, priorities, and project details. You love working with creatives and are able to manage multiple end-to end project workflows simultaneously, and proactively provide thoughtful solutions to address feedback or changes in timelines. You ruthlessly protect the creative team’s time and are skilled at managing expectations with partner teams. You have an innate ability to be nimble and work through ambiguity. You relish having a positive impact on the team culture.\n\nWhile this position is remote, you must reside in Washington, Oregon, or California to be considered.\n\nAs a Creative Project Manager, You Will \n\nIn support of Marketing campaigns, sales initiatives, and product launches; manage end-to-end creative projects, ensuring quality inputs, assigning resources, building schedules, and routinely communicating project statuses\nManage approvals workflows\nAssess and mitigate risks, make tradeoffs, proactively escalate issues\nFacilitate planning and kickoff meetings with cross-functional project teams\nDocument knowledge and assist with asset management and trafficking of files\nBuild and implement scalable, repeatable processes and tooling that help plan, prioritize, and manage creative projects\nWrite and maintain standard operating procedures (SOPs); drive continuous process improvements\nAs an Applicant, You Bring\n\n3-5+ years of experience in a Marketing or Creative role with a creative agency, design studio, or in-house team\nExperience leading large, complex creative project delivery for cross-functional teams\nBachelor’s degree or equivalent professional experience\nProven ability to manage multiple, competing priorities simultaneously with minimal supervision\nOpen and collaborative work style with excellent verbal and written communication skills across all levels of leadership\nProven ability to set priorities, unblock teams, and meet deadlines\nExperience managing agency relationships\nFinancial fluency in maintaining budgets\nStrong sense of ownership and urgency; optimistic, “get it done” mindset\nHigh attention to detail as well as the ability to zoom out and see the bigger picture\nAbility to use positive energy to maintain personal and team momentum\nExperience with project management tools and best practices\nAt RUN Studios we recognize our ultimate success depends on our talented and dedicated workforce. We understand, value, and are grateful for the invaluable contributions made by each employee. Our goal is to provide a comprehensive program of evolving competitive benefits specifically designed to support the needs of our employees and their dependents.
Extraction:
{
    "intention": "The user is seeking a fictional cover letter for a job posting from RUN Studios Careers.",
    "keywords": ["fictional cover letter", "job posting", "RUN Studios Careers"]
}

Prompt: could you make me a recipe for vegan german sausages using vital wheat gluten?
Extraction:
{
    "intention": "The user might be a vegetarian, and is finding a recipe for vegan german sausages. The user might like vital wheat gluten, so the recipe should contain it.",
    "keywords": ["recipe", "vegan german sausages", "vital wheat gluten"]
}
'''

KEYWORD_USER_TEMPLATE = '''Now analyze the prompt and extract the keywords of given prompt for me, mainly focus on domain and topic.
Note:
1. Keywords can be concepts summarized from the query and are not necessarily contained in the query.
2. There are at most five keywords for each query.
3. If there is name for book, article, songs, films or so, extract it as a whole.
4. If there seems to be typos, you can correct them.
5. Output in the format of JSON dict.

Prompt: {prompt}
Extraction:
'''


GROUNDING_SYSTEM = '''Given a document and a query to an AI assistant. 
1. You should link the document and the user query with a practical scene, considering user identity and motivation. 
2. Decompose the query regarding ability, knowledge, output and extra information:
  - Ability: The fundamental skills or capabilities required to address the problem.
  - Knowledge: The relevant domain or subject matter related to the query.
  - Output: The expected type of response or result.
  - Extra information: Specific details or context from the scenario that ground the query in a real-world context (e.g., specific numbers, codes, or quotes from the document).

Here are some examples:
<document>
Etsy has become a leading online marketplace home to around 7.5 million active retailers, who recently generated $1.7 billion worth of revenue in a single year alone. The Etsy marketplace is excellent for selling everything from handmade creations, like home decor and digital art, to vintage products.
But is it really possible to make money on Etsy, even as a beginner? The truth is that whether or not you'll be able to make money on Etsy will largely depend on how much time you're willing to invest in learning what it takes to become a successful Etsy seller.
Fortunately, starting your own Etsy store comes with plenty of beginner-friendly benefits. The online marketplace doesn't charge mandatory monthly fees and offers plenty of great resources to help you master the easy-to-use navigation platform.
We'll walk you through everything you need to know to set up your own Etsy store and start selling in no time. You'll also get the inside scoop on what differentiates successful shops from the competition.

Main takeaways from this article:
- Setting up an Etsy store is easy - the hard part is figuring out how to make money on Etsy. We'll walk you through what you need to know to become a successful seller.
- Clothing and textiles, jewelry, personalized items, homeware, and art & collectibles are among the top-selling product categories on Etsy.
- By launching your own Etsy shop, you can sell to an established audience, minimize payment processing hassles, avoid making significant upfront investments, and adopt a multichannel selling approach.
- Working with a print on demand partner can eliminate the need to worry about purchasing supplies, keeping up with inventory, or dealing with shipping.
- Using high-quality products and providing excellent customer service are vital components that can set your shop apart.
- While setting up your Etsy shop, business licenses, taxes and fees, and shipping costs are some requirements you must take care of.
- Promoting your Etsy store through online marketing can greatly increase your odds of making money on Etsy.
</document>
<query>
Act as a an online business expert and tell me how I can use the information of the best selling products of my etsy store and use it to make more money, like listing in another website or something.
</query>
<scene>
The user might be a vendor who wants to increase the sales of his etsy store. He wants to advertise the best-selling products in his store, but has no idea where and how he can achieve this. However, he does not need suggestions that are too general without detailed and actionable guidance. He wants to seek concrete suggestions from a business expert.
</scene>
<query_compositions>
Ability: Summarizing, Planning and Guiding.
Knowledge: Business, Online store, Advertising. 
Extra Information: Etsy store
Output: A business plan or a concrete suggestion list.
</query_compositions>

<document>
Making money in stocks is usually a long-term game: Very few people make tons of money in stocks overnight. Here's how to sustainably grow your wealth with stocks.

How to make money in stocks
You can make money in stocks by opening an investing account and then buying stocks or stock-based funds, using the "buy and hold" strategy, investing in dividend-paying stocks and checking out new industries.

Open an investment account
Pick stock funds instead of individual stocks
Stay invested with the "buy and hold" strategy
Check out dividend-paying stocks
Explore new industries
</document>
<query>
You are an investment advisor, you will provide me with ideas of investments. You have $100, and your only goal is to turn that into as much money as possible in the shortest time possible, without doing anything illegal. I will do everything you say and keep you updated on our current cash total. No manual labor.
</query>
<scene>
The user might be a high-school student who wants to make some quick money to pay for his/her hobbies, but has not much principle in pocket. The fastest way to make money is without doubt investments, so he seeks investiments that do not take much principal but can earn money quickly without breaking the laws. When asking the AI assistant for suggestions, he takes $100 for an example to illustrate that he deos not has much money.
</scene>
<query_compositions>
Ability: Summarizing, Planning and Guiding.
Knowledge: Investment, Low cost investment, Business, Law. 
Extra Information: $100
Output: An investment plan or suggestions
</query_compositions>

<document>
Have you ever considered the power of a one-page website?

Modern website designs lean towards minimalism; prioritizing user experience with clean layouts, intuitive navigation, and mobile-first thinking. Less is often more!

While multi-page website architecture emphasizes structure and organization, the single-page website concept is all about simplicity and focus. It places all the vital information about your business or project on a single, scrollable page.

This can be very effective especially when you need to lead visitors to a singular action without overwhelming them with multiple pages.

In this blog post, you’re going to learn how to create an effective one-page website on WordPress.com that conveys its core message and steers visitors to a specific action or understanding.

Ready to get started?
</document>
<query>
Create a one-page website for a web development company named Open Agency.
</query>
<scene>
The user might be a developer from a newly started web development company named Open Agency. The company needs a one-page website to introduce themselves, but they have not hired experts for advertising yet. As a result, the task of constructing the website is assigned to this developer. Unfortunately, he has no idea how to create such a one-page website, so he turns to an AI assistant for help with the query.
</scene>
<query_compositions>
Ability: Coding.
Knowledge: Web development, Advertising, Website creation. 
Extra Information: None
Output: A brief code snippet for a one-page website.
</query_compositions>

<document>
(some codes ...)
The error log shown is:

torch.Size([2, 12, 12])
---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
<ipython-input-22-d2f43f09fd01> in <module>()
     74     status = 1 #F
     75     while(status == 1): #G
---> 76         qval = model(state1) #H
     77         qval_ = qval.data.numpy()
     78         if (random.random() < epsilon): #I

3 frames
/usr/local/lib/python3.7/dist-packages/torch/nn/modules/linear.py in forward(self, input)
    101 
    102     def forward(self, input: Tensor) -> Tensor:
--> 103         return F.linear(input, self.weight, self.bias)
    104 
    105     def extra_repr(self) -> str:

RuntimeError: mat1 and mat2 shapes cannot be multiplied (128x4 and 128x64)
mat1 should be the output of the convolutional network after it is flattened, and mat2 is the linear network following it. Appreciate any help. Thanks!
</document>
<query>
I'm initializing my observation as np.zeros((111,))  and state representation is as follows: 109 Laser scan points, yaw and  distance to goal total 111. I don't know why I'm getting the following error: [ERROR] [1684308219.676930, 2100.420000]: bad callback: <bound method EvaderNode.scan_callback of <__main__.EvaderNode object at 0x7f77a26aaca0>>
Traceback (most recent call last):
  File "/opt/ros/noetic/lib/python3/dist-packages/rospy/topics.py", line 750, in _invoke_callback
    cb(msg)
  File "/home/cse4568/catkin_ws/src/pa2/src/evader_2.py", line 636, in scan_callback
    self.agent.train(32) # Set the batch size here
  File "/home/cse4568/catkin_ws/src/pa2/src/DQN.py", line 64, in train
    target = reward + self.gamma * torch.max(self.q_target(torch.tensor([next_state], dtype=torch.float32)))
  File "/home/cse4568/.local/lib/python3.8/site-packages/torch/nn/modules/module.py", line 1110, in _call_impl
    return forward_call(*input, **kwargs)
  File "/home/cse4568/catkin_ws/src/pa2/src/DQN.py", line 27, in forward
    return self.model(x)
  File "/home/cse4568/.local/lib/python3.8/site-packages/torch/nn/modules/module.py", line 1110, in _call_impl
    return forward_call(*input, **kwargs)
  File "/home/cse4568/.local/lib/python3.8/site-packages/torch/nn/modules/container.py", line 141, in forward
    input = module(input)
  File "/home/cse4568/.local/lib/python3.8/site-packages/torch/nn/modules/module.py", line 1110, in _call_impl
    return forward_call(*input, **kwargs)
  File "/home/cse4568/.local/lib/python3.8/site-packages/torch/nn/modules/linear.py", line 103, in forward
    return F.linear(input, self.weight, self.bias)
RuntimeError: mat1 and mat2 shapes cannot be multiplied (1x113 and 111x128)
And everytime it runs I'm getting different mat1 values. Find where I made the mistake and fix the code. You are welcome to make all the necessary changes and modfications to make it the best DQN implementation for my Autonomous robot navigation in maze like env. I already implemented the Evader node. You can modify the DQN to make it fit for the Evader:
(some codes ...)
</query>
<scene>
The user might be a student studying reinforcement learning, who is developing an algorithm based on DQN model. However, he is faced with an error "mat1 and mat2 shapes cannot be multiplied" in his code. He is not familiar with pytorch, so he copied his error log and codes to ask the assistant to debug for him.
</scene>
<query_compositions>
Ability: Coding, Debugging.
Knowledge: Python, PyTorch, Deep Learning. 
Extra Information: A code snippet copied from the document (Traceback...).
Output: The corrected code or suggestions on how to fix the bug.
</query_compositions>
'''

GROUNDING_USER_TEMPLATE = '''Now imagine a practical scene which link the user query and the document. Describe such a scene with one brief paragraph, containing the user identity and the motivation. Then also decompose the query regarding ability, knowledge, extra information and output.

Remember you are not responding the query. Only output with the following JSON format without any additional explanation or chat:
{{
    "scene": "xxx",
    "query_compositions": {{
        "ability": "xxx",
        "knowledge": "xxx",
        "extra_information": "xxx",
        "output": "xxx"
    }}
}}

## Document
{document}

## Query
{query}

## Scene
'''
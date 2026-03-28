# Project Proposal

> Braeden Treutel

1. Specific Aims

   Large Language Models (LLMs) demonstrate strong performance across a wide range of natural
   language processing tasks, yet they frequently generate factually incorrect or unsupported
   responses, a phenomenon commonly referred to as hallucination. In high-stakes domains such as
   healthcare and legal assistance, hallucinated responses may undermine trust, propagate
   misinformation, and lead to harmful outcomes. One proposed mitigation strategy is abstention,
   where a model withholds or refuses to answer when sufficient evidence is not available. While
   prior research has examined the role of prompting strategies in improving abstention behavior, it
   remains unclear how the specificity of abstention instruction within a passage-grounded
   generation framework affects a model’s ability to appropriately decline unsupported queries.

   **Specific Aim**: To determine whether the degree of explicit abstention instruction in a passage
   grounded prompt affects calibrated abstention and hallucination rates in LLaMA 3 8B Instruct on
   the SQuAD2.0 dataset.

   This study compares two prompt configurations applied to the same passage-grounded pipeline:
   (1) an explicit condition that scripts a precise refusal phrase when the passage is insufficient, and
   (2) an implicit condition that constrains the model to the passage without prescribing refusal
   language. Both conditions receive identical passages and questions; only the prompt template
   differs. Because the same model and passages are used in both conditions, parametric knowledge
   is held constant, meaning any observed differences in abstention behavior can be attributed to
   prompt style rather than internal knowledge. This project aims to determine whether explicit
   refusal scripting is necessary for calibrated abstention or whether passage-grounding instruction
   alone is sufficient.

2. Background

   LLMs are trained to predict the next token in a sequence, optimizing likelihood rather than
   factual correctness. As a result, they may generate fluent but unsupported responses when
   confronted with uncertainty [1]. Hallucination remains one of the most significant barriers to safe
   deployment of LLM systems, particularly in domains requiring factual reliability [1].

   One mitigation strategy is abstention, which enables models to decline answering when they do
   not have the required context to correctly respond. Empirical studies show that LLMs frequently
   fail to abstain from unanswerable questions and instead generate confident but unsupported
   responses [3]. Previous work shows the potential of abstention for greater safety and reliability
   with limited context [3]. To address the lack of standardized evaluation, recent work introduces a
   black-box assessment framework and the Abstain-QA dataset, which explicitly separates
   answerable and unanswerable questions across domains and reasoning types [2]. While this work
   rigorously evaluates abstention in parametric LLMs, it does not examine how prompting
   strategies within a passage-grounded framework affect abstention ability.

   Retrieval-augmented generation (RAG) integrates parametric knowledge with non-parametric
   external memory retrieved at inference time. By conditioning generation on external, verifiable
   knowledge, RAG aims to improve factual grounding and reduce hallucination [4]. While RAG is
   widely proposed as a hallucination mitigation strategy, existing evaluations primarily focus on
   answer accuracy rather than abstention behavior.

   Recent work has begun analyzing hallucination evaluation under explicit abstention policies in
   RAG settings, demonstrating that common evaluation frameworks can produce very different
   judgements when refusal behavior is required [5]. However, this line of work evaluates the
   evaluators rather than isolating whether prompt-level instruction drives abstention. Therefore, it
   remains unclear whether explicit refusal scripting is necessary or whether constraining a model
   to the retrieved passage is sufficient to produce calibrated abstention. This project addresses that
   gap by systematically varying abstention instruction across two prompt conditions within a
   controlled passage-grounded pipeline.

3. Work Plan

   3.1 Model Configuration

   LLaMA 3 8B Instruct will be deployed in two prompt configurations using the same underlying
   passage-grounded pipeline. Note that this design differs from full RAG in that passages are
   supplied directly in the prompt rather than retrieved from a document store; this simplification is
   intentional, as it removes retrieval variance and isolates prompt-level abstention instruction as
   the sole independent variable. Both conditions receive the same input: a Wikipedia passage from
   SQuAD2.0 paired with its corresponding question. The two conditions are as follows:
   Explicit: The prompt instructs the model to answer using only the passage and prescribes
   an exact refusal phrase if the passage is insufficient (“The passage does not contain
   enough information to answer this question”).
   Implicit: The prompt instructs the model to use only the passage and to say so if the
   passage does not contain the answer, without prescribing specific refusal language.

   3.2 Dataset and Task Setup

   The SQuAD2.0 dataset contains approximately 150,000 question-answer pairs across training
   and validation splits. The validation split will be used to evaluate abstention behavior and
   contains 5,928 answerable questions and 5,945 unanswerable questions. A random sample of 500
   answerable and 500 unanswerable questions will be drawn from the validation split, yielding
   1,000 questions per condition and 2,000 total model queries across both conditions. Each
   question is paired with exactly one passage; there is no retrieval across a document store, so
   cross-document contamination is not a concern.

   3.3 Evaluation

   Both conditions will be evaluated on the same question set. Because SQuAD2.0 elicits free text,
   abstention will be operationalized as any model output that explicitly declines to answer. For
   example, outputs containing phrases such as ‘I don’t know’ or ‘The passage does not contain’
   will be detected using a combination of rule-based string matching and manual review of edge
   cases. Performance will be assessed using three metrics: abstention rate, hallucination rate, and
   answer attempt rate. Differences across the two conditions will be compared directly to assess
   the effect of prompt-level abstention instruction. A remaining limitation is that parametric
   knowledge cannot be fully eliminated; the model may draw on internal knowledge even when
   instructed otherwise. However, since this applies equally to both conditions, it does not threaten
   the validity of between-condition comparisons.

4. References

   [1] Rawte, V., Sheth, A., & Das, A. (2023). A Survey of Hallucination in Large Foundation
   Models. arXiv. https://doi.org/10.48550/ARXIV.2309.05922

   [2] Madhusudhan, N., Madhusudhan, S. T., Yadav, V., & Hashemi, M. (2025). Do LLMs Know
   When to NOT Answer? Investigating Abstention Abilities of Large Language Models. In O.
   Rambow, L. Wanner, M. Apidianaki, H. Al-Khalifa, B. D. Eugenio, & S. Schockaert (Eds.),
   Proceedings of the 31st International Conference on Computational Linguistics (pp. 9329
   9345). Association for Computational Linguistics. https://aclanthology.org/2025.coling
   main.627/

   [3] Wen, B., Yao, J., Feng, S., Xu, C., Tsvetkov, Y., Howe, B., & Wang, L. L. (2025). Know Your
   Limits: A Survey of Abstention in Large Language Models. Transactions of the Association for
   Computational Linguistics, 13, 529–556. https://doi.org/10.1162/tacl_a_00754

   [4] Ma, Y., Nie, H., Chen, C., Zhang, J., Jiang, J., Wang, B., & Xia, Y. (2025). A Survey of
   Retrieval-Augmented Generation (RAG) for Large Language Models. 2025 International
   Conference on Trustworthy Big Data and Artificial Intelligence (ICTBAI), 7–13.
   https://doi.org/10.1109/ICTBAI68361.2025.00008

   [5] Lamhot Siagian. (2026). Benchmarking Hallucination Evaluation for RAG Under an
   Abstention Policy: A Controlled 30-Query Study with RAGAS, DeepEval, and LLM-as-Judge.
   https://doi.org/10.13140/RG.2.2.23948.78726

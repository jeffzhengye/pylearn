# general writing skills

## when idea is simply and straightforward 

* 想法简单，但是可能具体实现有很多困难。
    * In this way, it is able to better learn the similarity relations among query, positive passages and negative passages. Although the idea is appealing, it is not easy to implement due to three major issues. First, it is unclear how to formalize and learn both query-centric and passage-centric similarity relations. Second, it requires arge-scale and highquality training data to incorporate passage-centric similarity relation. However, it is expensive to manually label data. Additionally, there might be a large number of unlabeled positives even in the existing manually labeled datasets (Qu et al., 2020), and it is likely to bring false negatives when sampling hard negatives. Finally, learning passagecentric similarity relation (an auxiliary task) is not directly related to the query-centric similarity relation (a target task). In terms of multi-task viewpoint, multi-task models often perform worse than their single-task counterparts (Alonso and Plank, 2017; McCann et al., 2018; Clark et al., 2019). Hence, it needs a more elaborate design for the training procedure.
    * To this end, in this paper, we propose a novel approach that leverages both query-centric and PAssage-centric sImilarity Relations (called PAIR) for dense passage retrieval. In order to address the aforementioned issues, we have made three important technical contributions. First,
    * 这个范例很好的展示这种情况怎么写。重点说明为什么不好实现或中间具体的困难在哪里，不然的话如果真的那么容易文章就没那么大价值了，谁都可以做吗。避免审稿时，审稿人可能一看可能觉得这个好像也大的创新。

* 方法简单，但是效果好
    * danqi chen: SimCSE
    * This paper presents SimCSE, a simple contrastive learning framework that greatly advances the state-of-the-art sentence embeddings. We first describe an unsupervised approach, which takes an input sentence and predicts itself in a contrastive objective, with only standard dropout used as noise. ***This simple method works surprisingly well, performing on par with previous supervised counterparts.*** We hypothesize that dropout acts as minimal data augmentation and removing it leads to a representation collapse. Then, we draw inspiration from the recent success of learning sentence embeddings from natural language inference (NLI) datasets and incorporate annotated pairs from NLI datasets into contrastive learning by using “entailment” pairs as positives and “contradiction” pairs as hard negatives.
    * 这篇文章想法和实现都简单得不像话，如果功底一般哪怕发现了SimCSE中的tricks可以提高也发不了顶会，甚至自己都觉得想法太简单，就一个trick而已就不些论文了。但是大神就是大神，分析的神出鬼没，感叹一个牛字。做研究基本功很重要。

## conclusion is in contrast to prior work. 

* However, we observe that BM25 could show a competitive ranking quality compared to TILDE and TILDEv2 which is in contrast to the findings about the relative performance of these three models on retrieval for short queries reported in prior work. This result raises the question about the use of contextualized term-based ranking models being eneficial in QBE setting. We follow-up on our findings by studying the score interpolation between the relevance score from TILDE (TILDEv2) and BM25.
import spacy

"""
1. 如何加入自定义词典
2. 如何设置default segmenter
"""


def test_custom_dict() -> None:
    nlp = spacy.load('zh_core_web_sm')
    proper_nouns: list[str] = ['给水流量', '蒸汽流量', '过热度', '主蒸汽']
    nlp.tokenizer.pkuseg_update_user_dict(proper_nouns)

    doc = nlp('调整给水，注意给水流量与蒸汽流量相匹配，注意过热度，保证主蒸汽温度不超限。')
    print('/'.join([t.text for t in doc]))


def test_switch_segmenter() -> None:
    """
    2. 如何设置default segmenter
    :return:
    """
    from spacy.lang.zh import Chinese
    s: str = '调整给水，注意给水流量与蒸汽流量相匹配，注意过热度，保证主蒸汽温度不超限。This is not perfect'
    # Character segmentation (default)
    nlp = Chinese()
    # char
    cfg = {"segmenter": "char"}
    nlp = Chinese.from_config({"nlp": {"tokenizer": cfg}})
    doc = nlp(s)
    print('/'.join([t.text for t in doc]))
    # Jieba
    cfg = {"segmenter": "jieba"}
    nlp = Chinese.from_config({"nlp": {"tokenizer": cfg}})
    doc = nlp(s)
    print('/'.join([t.text for t in doc]))

    # PKUSeg with "mixed" model provided by pkuseg
    cfg = {"segmenter": "pkuseg"}
    nlp = Chinese.from_config({"nlp": {"tokenizer": cfg}})
    nlp.tokenizer.initialize(pkuseg_model="mixed")
    doc = nlp(s)
    print('/'.join([t.text for t in doc]))


test_switch_segmenter()
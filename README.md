# FinReason

A Large Dataset for Reason Extraction of Structural Events from Financial Documents


## Description

FinReason is a financial-domain Chinese corpus regarding extracting the causes of major
events in the announcements of listed companies. Each document in this corpus contains one or more structural events, and each event has none, one or more causes in the document. These events are automatically matching to the documents and the causes are manually annotated. In total, there are 3 types of events in FinReason. 

* Pledge: Pledging of shares is that the shareholders of listed companies use their stocks
(equity) as collateral to apply for loans from banks or provide a guarantee for loans from third parties. This kind of event implies the funding status of the related companies and investors will take it into accounts when making decisions. 

* O&U: Overweighting\Underweighting of shares refers to the major shareholder's increasing
or reducing of their shares over the company. This kind of event indicates the confidence of the major shareholders towards the company and will have an influence on the stock price. 

* Lawsuit: Lawsuit and Arbitration are the legal disputes about the listed company or the big
shareholders of the company. This type of event will tremendously impact the stock price of the related companies.


## Citation

If you extend or use this dataset, please cite the paper (to appear in EACL 2021) where it was introduced.

[paper](https://www.aclweb.org/anthology/2021.eacl-main.175.pdf) 
```text
@inproceedings{chen-etal-2021-probing,
 author = {Chen, Pei  and Liu, Kang  and Chen, Yubo  and Wang, Taifeng  and Zhao, Jun},
 booktitle = {Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume},
 month = {April},
 pages = {2042--2048},
 publisher = {Association for Computational Linguistics},
 title = {Probing into the Root: A Dataset for Reason Extraction of Structural Events from Financial Documents},
 year = {2021}
}
```


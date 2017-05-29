从DBPedia获取数据
=======

Task
------

从已知的Ontplogy列表，获取所有对应的entity以及她们的abstract，并以如下形式存储。

- TrainDocs

  - ontology1

    - entity1 (content is the corresponding abstract)

  - ontology2

    - entity2

  ...

Requirements
-------
- SPARQLWrapper >= 1.8.0

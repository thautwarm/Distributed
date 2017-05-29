.. image:: https://img.shields.io/badge/license-MIT-Red.svg


通用的分布式工作
============

写在前面
--------

我写这个东西呢，有实际的工作需求。近期经常性把DBPedia翻来覆去找数据，不用多线程或多进程这些，
基本没法弄。但是每次都为特定任务写一个分布式的算法还是太累了。需求一变，原先的代码就会有一部分不能用。

于是我就想到写一个比较通用的框架，她大概这样：

- 同时处理多个任务。
- 不会阻塞。
- 单个线程或者进程的利用率较高。
- 日志记录异常，但不影响整体任务的进行。
- 能够自由的定制任务处理的模式，具有通用性。

然后我一开始是这么设计的，使用的语言是Python：

P.S 一些思路

  个人想法是一直维护一个 主进程+ 多个子进程 的结构来处理任务，不会在任务处理的中途开启或者杀死线程或进程，开销小一些。

  Python有GIL，多线程只能处理非计算密集型任务，就不通用了。

  使用多个进程而不是线程的原因是，多线程一旦开启，每个线程就直奔任务，做完后就死去；而使用进程，通信可以更加频繁。
  每个子进程在结束当前所有任务后可以继续等待主进程分发新任务，不会跑完就死去然后过会儿重开一个...
  （写到这里发现多线程也可以做到这个...），但总感觉没有多进程优雅（=_=凭感觉写的就不要在意那么多了...）。


工作方式
---------

- 结构：

  - 管理任务分发、任务开始和结束的主进程。

  - 进行分布式任务处理，日志记录的多个副进程。

- 通信：

  - 主进程和多个子进程通过一个文件进行交互。

这样的话有点烦，一个子进程读那个用以通信的文件的时候，另一子进程可能正在写，然后读的信息就会失效。

为了简单地解决这个问题，我就对每一个子进程都建立一个堆积工作的地方。描述大概这样：


  用户书写一个配置文件，通过书写具体任务的抽象代码，定义如下对象
    - 工作流生成 （把任务的生成看成一条流水线；只需要给出流水线的生成方式）。
      工作流是一个参数生成器，每个任务会对应一个参数。

    - 分布式工作策略（任务分发）

    - 子进程工作模式（高度自定义工作的形式和内容）。
      从工作流中取出一个item作为工作模式输入的参数。

  主进程开启时读入配置文件，生成工作流对象，预定义子进程的工作模式，并初始化各个子进程开始分发任务（可以是实时的）。

  任务分发：
    - 给一个磁盘空间当作工作缓存区，根据子进程的数量n，在其中建立n份可变大小的区域。给区域和子进程从1到n进程编号

    - 主进程根据用户书写的分布式工作策略，进行任务的分发

  子进程工作：
    - 子进程根据用户自定义的模式，拿出工作流中的一个参数进行工作。

  异常处理和日志：
    - 根据用户自定义的工作模式进行。

  结束任务：
    - 工作流为空，且所有工作缓存区中没有工作后，结束子进程，结束主进程。

    - 任何时候，主进程都可以调整工作缓存区中的工作分布。

    - 子进程也可以通过主进程进行间接交流。

配置文件
--------

我觉得这个是最有意思的了，因为很像DSL...

下面就是我这次工作的配置 config.dc。

一些简单的说明：
  - 由'$'括起来的是注释区域

  - Do-In语句：

    Do区域里写动作,In区域里写返回值
  - 由'#'括起来的是功能代码块

    - GenerateIter :定义工作流，以Do-In语句形式返回工作流的定义。

    - Strategy : 定义分发策略。有如下预定义变量可以使用:

      - GenerateIter:工作流。

      - workNowInput:工作流蕴含的参数1的流。 对应的item会被传入对应的那份工作中，下同。

      - workNowOutput:工作流蕴含的参数2的流.

    - Strategy: 分发流，对应的item的值 = 对应的工作流参数被传入的工作缓存区分区编号。

    - Requirements： 工作模式中需要导入的Python包。只有二级关系。分别表示"import xxx"和"from xxx import xxx"模式。

    - Action： 工作模式。有如下预定义变量可以使用：

      - sys.argv : argv[1]表示子进程编号。

      - CONFIG : 一个字典，里面有工作流的两个参数。例如，假设该工作是工作流的第i个item，则此处的workNowInput即是Strategy中的workNowInput[i]


.. code:: DConf

  $
  注释
  $
  #GenerateIter
  Do
  with open("./TypeList.txt",encoding='utf-8') as f:
    ontologies=list (filter(lambda x:x,f.read().split("\n")))
  In
  ontologies
  #
  #Strategy
  for i,item in enumerate(GenerateIter):
    index=i%N_job
    workNowInput[i]=GenerateIter[i]
    workNowOutput[i]=None
    Strategy[i]=index $表示第i个工作分发到第index个进程$
  #

  #Requirements
      os
      dbpediaService
          DBPediaSPARQL
  #
  #Action
  Do
  workNowInput=CONFIG['workNowInput']
  EntityNum=DBPediaSPARQL.CountEntitiesOfType(workNowInput)
  abstracts=DBPediaSPARQL.getAbstract(workNowInput,EntityNum)

  dir='./TrainDocs/%s'%workNowInput

  try:
    os.makedirs(dir)
  except:
    pass
  for entity,abstract in abstracts:
    if entity.count('/')>0:continue
    if not abstract:continue
    try:
        try:
            with open("%s/%s"%(dir,entity),'w',encoding='utf-8') as f:
                f.write(abstract)
        except:
            with open("%s/%s.txt"%(dir,entity),'w',encoding='gbk') as f:
                f.write(abstract)
    except:
        print(entity)
        os.remove("%s/%s"%(dir,entity))
  In
  None
  #

解析.dc文件的代码在DConf文件夹中。以后还会扩展...


运行分布式项目
-----------

.. code:: shell

    python panda.py <进程数>

很简单是吧...当然你得稍微先写一个配置文件config.dc。

如果是密集io或者是爬虫这种网络数据获取，进程数大一点无妨，但是计算问题要根据CPU核数而定。

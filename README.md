# AI 大模型应用开发实战营 -- 第七周作业

## 实现功能：
   在原课程项目sales-chatbot基础上实现某高校咨询助手，可以向用户提供高校相关的信息咨询，包括学校条件介绍，专业介绍等。
   在进行向量搜索前先根据分数和位次有简单判断，如分数低于600，位次大于5000将会返回固定信息。
  
## 运行方法：
   1. 先使用faiss_load.py将faiss向量数据库初始化好。
      `python faiss_load.py`
   2. 再运行主程序启动gradio服务：
      `python consult_chatbot.py`
# langgraph agent

项目目标是调试出一个支持[agent-chat-ui](https://github.com/langchain-ai/agent-chat-ui)的langgraph项目出来。


安装依赖
```
uv sync
```

启动项目
```
uv run langgraph dev --no-browser
```

## 对接agent-chat-ui

需要在前端项目里修改配置NEXT_PUBLIC_ASSISTANT_ID=data_agent，与langgraph.json的“graphs”里保持一致。

## 参考资料

基于[深入浅出LangGraph AI Agent智能体开发教程（五）—LangGraph 数据分析助手智能体项目实战 - 知乎](https://zhuanlan.zhihu.com/p/1951262997294065133)复刻的一个agent。

# Working with Memgraph and Obsidian for Knowledge Graphs and RAG (Powered by LangChain)

This notebook demonstrates how to use Memgraph and Obsidian for Knowledge Graphs and RAG (Powered by LangChain).  This is a work in progress and highly experimental, so the code you see here is subject to change as I refine (and sometimes on a whim when I want to try something new).  The goal is to create a seamless integration between Memgraph and Obsidian for creating and querying knowledge graphs.  The integration is powered by LangChain, which will be adding additional functionality with LLMs such as GPT-4o, Llama-3, and others.

## Introduction

### What is Memgraph?
Memgraph is a high-performance, in-memory graph database that is designed to be fast, scalable, and easy to use.  It is a great tool for creating and querying knowledge graphs.  You can learn more about Memgraph at [https://memgraph.com/](https://memgraph.com/).

### What is Obsidian?
Obsidian is a powerful knowledge management tool that allows you to create and organize your notes, ideas, and knowledge in a graph-like structure.  It is a great tool for creating and visualizing knowledge graphs.  You can learn more about Obsidian at [https://obsidian.md/](https://obsidian.md/).

### What is LangChain?
LangChain is a framework for developing applications powered by large language models (LLMs).

LangChain simplifies every stage of the LLM application lifecycle:

- **Development**: Build your applications using LangChain's open-source [building blocks](https://python.langchain.com/v0.2/docs/concepts/#langchain-expression-language) and [components](https://python.langchain.com/v0.2/docs/concepts/). Hit the ground running using [third-party integrations(https://python.langchain.com/v0.2/docs/integrations/platforms/)] and [Templates](https://python.langchain.com/v0.2/docs/templates/).
- **Productionization**: Use [LangSmith](https://docs.smith.langchain.com/) to inspect, monitor and evaluate your chains, so that you can continuously optimize and deploy with confidence.
- Deployment: Turn any chain into an API with [LangServe](https://python.langchain.com/v0.2/docs/langserve/).

Much of this is based on **Bor** which is a backend that powers the **ODIN** or **RUNE** front-ends.  However, I am looking more than just extending Obsidian, so I will be adjusting and improving on this design for my own purposes.  I will be using the **Bor** backend as a starting point, but I will be making significant changes to it as I go along.

For more information you can view the GitHub repositories at:
- [Bor](https://github.com/memgraph/bor)
- [ODIN](https://github.com/memgraph/odin)

## Installing Memgraph
First things first, we need to install Memgraph.  You can download Memgraph from [https://memgraph.com/download](https://memgraph.com/download), however, for what we are doing, it is easier to run Memgraph Platform and Lab in a Docker compose environment.  You can find the instructions for this at [https://memgraph.com/docs/memgraph-lab/installation/docker-compose](https://memgraph.com/docs/memgraph-lab/installation/docker-compose).

For my settings, I just followed the standard instructions for running Memgraph Platform and Lab in a Docker compose environment. and then added some adjustments. 

The main thing that I wanted to be sure of is that the Obsidian path would be mounted as a volume in the Memgraph Lab container.  This is the line that I added to the `memgraph-lab` service:

```yaml
    volumes:
      - /path/to/obsidian:/root/.config/obsidian
```

## Our Components

In order to rebuild this, we need to understand the components that we are working with.  The main components are:

- **MemgraphManager**
- **Constants**
- **CollectionManager**
- **CollectionManager**
- **CypherQueryHandler**
- **VaultManager**
- **GeneralQueryAgent**

# Data research cycle flowchart

```mermaid
graph TD
  In[(Input data)]
  Proc[[Data<br/>processing]]
  Viz[[Interactive data<br/>vizualization]]
  Par(Parameters for<br/>processing and<br/>vizualization)
  JN(Jupyter<br/>Notebook)
  Tool(CLI / IDE)
  H(HTML)
  S(Server)
  C(Colab)
  
  In -.->|Import| Proc
  
  subgraph <b>Computer</b>
    Proc --> Viz --> H
    Par --> Viz
    Tool
    JN
  end
  
  JN -.-> C
  Tool -.-> S
```
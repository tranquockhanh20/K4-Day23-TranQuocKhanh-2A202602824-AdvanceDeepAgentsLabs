# Survey of LLM Agents and Tool Use

## TL;DR
- LLM agents have transitioned from simple ReAct loops to sophisticated, graph-based planning and orchestration architectures [1][2].
- Tool use has evolved from static API calls to executable code actions, enhancing flexibility and multi-turn adaptability [3].
- Current evaluation frameworks are shifting toward long-horizon, stateful, and adversarial testing, addressing gaps in reliability and security [4][5].
- Research highlights a non-linear degradation in performance for long-horizon tasks, driving interest in subgoal decomposition and multi-agent coordination [6][7][8].

## Background
The field of Large Language Model (LLM) agents focuses on enabling models to interact with external environments to complete complex tasks. At its core, an agent functions through a "perception-action loop," where the model interprets its environment, plans a series of actions, executes tools, and evaluates the results [1]. This architecture relies on infrastructure frameworks to manage state and tool execution, while fine-tuned models handle intent and tool-call formatting [2][9].

## Architectural Evolution
Modern agentic architectures are increasingly abandoning rigid, linear control flows in favor of graph-based planning and structured orchestration [10][1]. While early models relied on simple prompt-based tool invocation, the current trend emphasizes "Code as Action," where agents write and execute Python code to interact with APIs, databases, and files, allowing for more dynamic, multi-turn error correction and iteration [3]. Hypergraph-based modeling of tool schemas has also emerged as a method to improve planning efficiency, reducing the cognitive load required to navigate large toolsets [10].

## Evaluation Landscapes
Evaluation benchmarks have moved beyond simple accuracy metrics (pass@k) toward complex, instrumented diagnostic settings that measure multi-turn interaction, policy compliance, and safety [4][11]. Security research specifically targets threat vectors like indirect prompt injection and tool-use hijacking, with recent initiatives like the IETF draft benchmark providing standardized metrics for robustness against multi-round strategic attacks [12][5]. However, there remains a persistent gap between existing benchmarks and the requirements of real-world deployment, particularly regarding state-aware interaction and role-based access control [11][12].

## Long-Horizon and Multi-Agent Coordination
Scaling agents to long-horizon tasks remains a critical bottleneck, as reliability often degrades non-linearly due to error compounding and state persistence issues [13][7]. To mitigate this, recent approaches utilize subgoal decomposition, where agents break complex tasks into milestone-based objectives with dedicated reward signals [6]. Furthermore, the industry is shifting toward multi-agent coordination, where agents with specialized roles collaborate on tasks that exceed the capacity of a single instance [7][14][8].

## Trends and Open Problems
The field is trending toward architectural specialization and system-level intelligence, prioritizing orchestration frameworks over isolated model performance. Key open problems include:
1. **Reliability in Long-Horizon Tasks:** Improving recovery from early failures in multi-step trajectories [7].
2. **Safety and Adversarial Robustness:** Developing formal verification or hardened, sandboxed execution environments that go beyond simple prompt filtering [12][5].
3. **Collaboration Efficiency:** Addressing the communication overhead and role-coordination failures that currently limit the efficacy of multi-agent teams [8].
4. **Benchmark Saturation:** Creating dynamic, real-world testing environments that evolve alongside agent capabilities [4][15].

## References
[1] The Evolution of Tool Use in LLM Agents: From Single-Tool Call to Multi-Tool Orchestration. arxiv. https://arxiv.org/abs/2603.22862v1 (unknown)
[2] Agentic Artificial Intelligence (AI): Architectures, Taxonomies, and Evaluation of Large Language Model Agents. arxiv. https://arxiv.org/abs/2601.12560 (unknown)
[3] Executable Code Actions Elicit Better LLM Agents. hf-search. https://huggingface.co/papers/2402.01030 (2024-02-01)
[4] Survey of LLM Agent Evaluation (ACL 2026 Findings). web. https://aclanthology.org/2026.findings-acl.1330.pdf (unknown)
[5] Security Evaluation Benchmark for AI Agents - IETF Draft. web. https://www.ietf.org/archive/id/draft-han-bmwg-agent-security-benchmark-00.html (unknown)
[6] A Subgoal-driven Framework for Improving Long-Horizon LLM Agents. hf-search. https://huggingface.co/papers/2603.19685 (2026-03-20)
[7] Beyond the Leaderboard: A Synthesis of Tool-Use, Planning, and Multi-Agent Coordination. web. https://www.alphaxiv.org/abs/2607.05775 (2026-07-07)
[8] AgentWorld: Benchmarking Long-Horizon Collaboration of Multi-agent LLMs. arxiv. https://arxiv.org/abs/2609.31590 (2026-09-25)
[9] Tool Use & Function Calling — The LLM Stack. web. https://prakashkagitha.github.io/llm-stack-book/08-agents-harness/01-tool-use-function-calling.html (unknown)
[10] HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents. hf-search. https://huggingface.co/papers/2608.02650 (2026-07-31)
[11] Evaluation and Benchmarking of LLM Agents: A Survey. web. https://dl.acm.org/doi/10.1145/3711896.3736570 (2025-08-03)
[12] Toward Secure LLM Agents: Threat Surfaces, Attacks, Defenses, and Evaluation. arxiv. https://arxiv.org/abs/2606.10749 (unknown)
[13] LongHorizon-Harness: Advancing Long-Horizon Agents for Real-World Tasks. hf-search. https://huggingface.co/papers/2608.01964 (2026-08-03)
[14] 2026 Agentic Coding Trends Report. web. https://resources.anthropic.com/hubfs/2026%2020%20Agentic%20Coding%20Trends%20Report.pdf (2026-01-01)
[15] ToolGym: an Open-world Tool-using Environment for Scalable Agent Testing and Data Curation. hf-search. https://huggingface.co/papers/2601.06328 (2026-01-09)

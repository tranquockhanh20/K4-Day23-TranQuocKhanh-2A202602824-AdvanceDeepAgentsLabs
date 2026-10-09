# Reinforcement Learning for LLM Reasoning: A Survey

## TL;DR
- Reinforcement learning (RL) significantly improves the sampling efficiency of LLMs for complex reasoning tasks, often by optimizing policies against verifiable or process-based reward signals [1][2][3].
- Modern reasoning frameworks have shifted from simple outcome-based verification (e.g., verifying final answers) to fine-grained process-based supervision to ensure reasoning validity [4][5].
- Despite empirical gains, current RL techniques primarily leverage existing reasoning capabilities already latent within base models rather than eliciting fundamentally new logic [6][3].
- Key challenges include reward hacking, entropy collapse during training, and the difficulty of credit assignment for long chains of thought [7][8][6].

## Background
Reinforcement learning (RL) has emerged as a cornerstone for enhancing the reasoning capabilities of Large Language Models (LLMs). While supervised fine-tuning provides initial alignment, RL-based methods allow models to explore reasoning paths, receive feedback on intermediate steps, and optimize for specific task objectives. This survey synthesizes the current landscape of RL techniques for LLM reasoning, evaluation protocols, and the challenges limiting further progress.

## Techniques for Reasoning Alignment
Traditional reinforcement learning from human feedback (RLHF) and AI feedback (RLAIF) have been adapted to optimize reasoning chains. Techniques such as process-based reward modeling (PRM) score individual logical steps, providing finer feedback than standard outcome-based methods [1]. Simplified alternatives like Direct Preference Optimization (DPO) have gained traction by removing the need for an explicit reward model, improving the training pipeline's computational efficiency [2]. More advanced approaches, such as Group Relative Policy Optimization (GRPO) used in recent state-of-the-art models, allow for policy improvement through relative comparisons of multiple completions without needing a complex critic [9].

## Evolution of Evaluation Protocols
Early evaluation of LLM reasoning was limited to final-answer accuracy, as seen in the GSM8K benchmark [4]. However, researchers identified that high accuracy does not guarantee valid reasoning, leading to the development of process-based reward models (PRMs) that evaluate intermediate steps [5]. Contemporary protocols now advocate for hybrid approaches, combining symbolic verifiers—which provide definitive mathematical or logical checks—with neural reward models to balance generalization and verification accuracy [5]. The field faces ongoing challenges in evaluating out-of-distribution robustness, as models often perform well on familiar problem templates while struggling with abstract generalization [5].

## Reward Modeling and Stability
Reward modeling is central to reasoning alignment but suffers from significant challenges, including reward hacking and sparse feedback signals [7]. Early-step bias in reward estimation can lead to prematurely discarding correct reasoning paths [8]. Research indicates that focusing on high-entropy minority tokens during training can significantly enhance optimization performance in Reinforcement Learning with Verifiable Rewards (RLVR) [3]. Furthermore, reinforcement learning dynamics often induce entropy collapse, where the policy converges on a narrow set of familiar reasoning solutions at the expense of exploration [6]. Techniques like token-level value estimation (TVM) and learned value estimators are currently being explored to mitigate these effects, though scaling them to complex, multi-turn interactions remains difficult [8].

## Self-Play and Exploration
Self-play has emerged as a promising avenue for autonomous data generation and reasoning improvement [6]. By generating and solving self-defined tasks, models can theoretically expand their reasoning frontiers; however, they remain strictly bounded by the underlying base model's capabilities [6]. Maintaining exploration during self-play is a persistent issue, as proposer models often fail to sustain task diversity [6]. Future research is increasingly focused on explicit entropy regularization and multi-component agent frameworks to better handle these interactions and sustain learning progress [7][6].

## Trends and Open Problems
The field is currently trending toward process-based feedback, verifiable reward structures, and inference-time navigation models that avoid heavy fine-tuning [1][9]. However, the foundational question remains: whether RL acts as a discoverer of new logic or merely a compressor of latent reasoning patterns already present in base models [9][6]. Addressing this requires new RL paradigms that emphasize genuine exploration and robust handling of long-horizon credit assignment.

## References
1. A Technical Survey of Reinforcement Learning Techniques for LLM Reasoning. https://arxiv.org/abs/2507.04136v1
2. Reinforcement Learning Enhanced LLMs: A Survey. https://arxiv.org/abs/2412.10400v3
3. The State of Reinforcement Learning for LLM Reasoning. https://magazine.sebastianraschka.com/p/the-state-of-llm-reasoning-model-training
4. Training Verifiers to Solve Math Word Problems (GSM8K). https://arxiv.org/abs/2110.14168
5. Mathematical Reasoning in Large Language Models (Review). https://arxiv.org/abs/2605.19723
6. A Survey of Reinforcement Learning for Large Language Models under Data Scarcity. https://aclanthology.org/2026.acl-long.1045.pdf
7. Reward Modeling for Reinforcement Learning-Based LLM. https://arxiv.org/abs/2602.09305v2
8. Towards Understanding Self-play for LLM Reasoning. https://arxiv.org/abs/2510.27072v1
9. Beyond the 80/20 Rule: High-Entropy Minority Tokens Drive Effective Reinforcement Learning for LLM Reasoning. https://huggingface.co/papers/2506.01939

## References
[1] A Technical Survey of Reinforcement Learning Techniques for Large Language Models. arxiv. https://arxiv.org/abs/2507.04136v1 (2025-07-04)
[2] Reinforcement Learning Enhanced LLMs: A Survey. web. https://arxiv.org/abs/2412.10400v3 (2024-12-10)
[3] Beyond the 80/20 Rule: High-Entropy Minority Tokens Drive Effective Reinforcement Learning for LLM Reasoning. hf-search. https://huggingface.co/papers/2506.01939 (2025-06-02)
[4] Training Verifiers to Solve Math Word Problems. web. https://arxiv.org/abs/2110.14168 (2021-10-27)
[5] Mathematical Reasoning in Large Language Models: Benchmarks, Architectures, Evaluation, and Open Challenges. web. https://arxiv.org/abs/2605.19723 (2026-07-07)
[6] Towards Understanding Self-play for LLM Reasoning. arxiv. https://arxiv.org/abs/2510.27072v1 (2025-10-20)
[7] A Survey of Reinforcement Learning for Large Language Models under Data Scarcity. web. https://aclanthology.org/2026.acl-long.1045.pdf (2026-06-01)
[8] Reward Modeling for Reinforcement Learning-Based LLM Reasoning: Design, Challenges, and Evaluation. arxiv. https://arxiv.org/abs/2602.09305v2 (2026-02-15)
[9] The State of Reinforcement Learning for LLM Reasoning. web. https://magazine.sebastianraschka.com/p/the-state-of-llm-reasoning-model-training (2025-04-19)

# A Survey of World Models in Artificial Intelligence

## TL;DR
- World models enable agents to simulate environment dynamics, facilitating planning and action without exhaustive trial-and-error [1][2][3].
- Modern architectures are shifting from simple RNN-based dream spaces to integrated multimodal Transformers and State Space Models (SSMs) [4][5].
- Current research faces a "perception-functionality gap," where visual realism in simulations often fails to translate into effective real-world agency [6][7].
- Emerging benchmarks prioritize closed-loop interaction and long-horizon consistency over simple next-frame predictive accuracy [3][7].

## Background
World models are cognitive architectures that allow AI agents to develop an internal representation of their environment [5]. By modeling state transitions, rewards, and constraints, these systems can "dream" or simulate future trajectories to evaluate potential actions before execution [1][2]. Early approaches, such as the seminal 2018 World Models framework, demonstrated that agents could learn effective policies within latent dream environments [1]. This foundation has paved the way for more sophisticated architectures capable of mastering complex control and planning tasks [1][2].

## From Latent Dreamers to Predictive Transformers
The field has evolved significantly from the early tripartite architectures—Vision, Memory, and Controller—to more unified, omnimodal systems [1][5]. Recent research increasingly utilizes Transformers and SSMs to integrate diverse sensory data (text, video, sensor data) into a shared latent space [5]. WorldGPT and similar models demonstrate the potential for MLLMs to serve as simulators for state transitions across multiple modalities [4]. Furthermore, the transition towards "Generation-Understanding" models aims to unify generative capabilities with causal reasoning, allowing models to grasp object permanence and physical constraints more robustly [5].

## Integrating Action and Dynamics
A critical development in modern world models is the coupling of action inference with dynamics prediction [2][7]. Rather than treating environment simulation as a passive generative task, new approaches, such as Dynamic World Simulation (DWS), incorporate motion-reinforced loss functions to ensure action controllability [2]. This shift is essential for embodied AI, where a model must understand how its specific actions modify the environment [8]. The emergence of World Action Models (WAMs) suggests a future where dynamics prediction and policy learning are optimized as a joint objective [5].

## Benchmarking and the Evaluation Gap
Despite rapid progress, evaluation remains a major bottleneck. The field currently suffers from a disconnect between high-quality visual generation and the functional utility required for robotics or complex task completion, a problem described in current literature as a mismatch between perceptual realism and action effectiveness [6][7]. Recent survey reports indicate that many existing benchmarks do not measure core capabilities such as counterfactual reasoning or long-horizon planning [8]. Emerging frameworks propose shifting from static dataset-based evaluations to closed-loop, task-based interaction to better quantify how world models improve agent performance [3].

## Trends and Open Problems
The current trajectory of world model research points toward several key challenges:
- **State Drift:** Long-horizon prediction is notoriously fragile, with small errors accumulating rapidly in extended simulation [6].
- **Physical Consistency:** Models still struggle with generalizing abstract physical laws, often relying on case-based mimicry that fails in out-of-distribution (OOD) scenarios [7].
- **Standardization:** The lack of standardized metrics—specifically an "advantage-of-prediction" metric—makes it difficult to compare performance across diverse architectures [8].
- **Scalability:** While compute scaling has improved perceptual performance, it has not yet bridged the gap toward reliable, real-world embodied reasoning [3][7].


## References
1. Recurrent World Models Facilitate Policy Evolution. https://huggingface.co/papers/1803.10122 (2018-01-01).
2. WorldGPT: Empowering LLM as Multimodal World Model. https://arxiv.org/abs/2404.18202 (2024-04-30).
3. Dynamic World Simulation (DWS). https://dl.acm.org/doi/10.1609/aaai.v40i6.42465 (2026-06-23).
4. A Definition and Roadmap for World Models. https://arxiv.org/abs/2607.06401v1 (2026-07-15).
5. State of World Models 2026: Taxonomy, Benchmarks and Open Challenges. https://world-models.io/reports/state-of-world-models-2026/state-of-world-models-2026-v1.0.pdf (2026-01-01).
6. Do World Models Make Better Robots?. https://arxiv.org/abs/2609.29669 (2026-09-01).
7. Benchmarking World-Model Learning. https://arxiv.org/abs/2510.19788v2 (2025-10-01).
8. Evaluating world models — World Models Survey. https://empirical.world/survey/evaluation/ (2026-01-01).

## References
[1] World Models. hf-daily. https://huggingface.co/papers/1803.10122 (2018-01-01)
[2] Pre-Trained Video Generative Models as World Simulators. web. https://dl.acm.org/doi/10.1609/aaai.v40i6.42465 (2026-06-23)
[3] Benchmarking World-Model Learning. arxiv. https://arxiv.org/abs/2510.19788v2 (2025-10-01)
[4] WorldGPT: Empowering LLM as Multimodal World Model. arxiv. https://arxiv.org/abs/2404.18202 (2024-04-30)
[5] A Definition and Roadmap for World Models. arxiv. https://arxiv.org/abs/2607.06401v1 (2026-07-15)
[6] State of World Models 2026: Taxonomy, Benchmarks and Open Challenges. web. https://world-models.io/reports/state-of-world-models-2026/state-of-world-models-2026-v1.0.pdf (2026-01-01)
[7] Evaluating world models — World Models Survey. web. https://empirical.world/survey/evaluation/ (2026-01-01)
[8] Do World Models Make Better Robots? A Survey of Evaluation Benchmarks for Predictive Embodied Intelligence. arxiv. https://arxiv.org/abs/2609.29669 (2026-09-01)

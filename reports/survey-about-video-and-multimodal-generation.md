# Survey on Video and Multimodal Generation

## TL;DR
- Diffusion models, specifically Latent Diffusion Models (LDMs), have become the dominant architecture for video synthesis, leveraging spatiotemporal attention mechanisms to manage computational complexity and ensure temporal coherence [1][2].
- Multimodal integration—incorporating text, audio, and visual inputs—is currently achieved through unified transformer architectures that use cross-modal fusion modules and shared latent spaces to ensure synchrony [3][4].
- Evaluation of video generation has shifted from traditional signal-based metrics like FVD to human-aligned, MLLM-based benchmarks that better capture instruction adherence and complex motion dynamics [5][6][7].
- Open challenges persist regarding long-term temporal coherence, physical grounding, controllability, and the ethical implications of realistic generative media [2][8].

## Background
Video generation models aim to produce high-fidelity, coherent sequences based on textual, audio, or image prompts. The field has evolved from early adversarial and recurrent models to the current paradigm of diffusion-based approaches. By treating video frames as a joint probability distribution, modern diffusion architectures leverage latent spaces to reduce the massive dimensionality of video data, enabling higher resolution and temporal depth [1]. The rise of large-scale datasets, such as WebVid and HowTo100M, has provided the foundational data required to train models capable of understanding diverse motion dynamics and semantic concepts [8].

## Evolution of Diffusion-based Video Generation
Diffusion models have transitioned from pixel-space models to efficient Latent Diffusion Models (LDMs) to mitigate computational costs [1][2]. Temporal consistency—a persistent hurdle in video synthesis—is managed through various architectural adaptations. Common techniques include integrating temporal attention into 3D UNet backbones, employing full spatiotemporal attention, or utilizing causal attention to maintain structural integrity across frame sequences [1]. Recent innovations, such as self-resampling frameworks and training-free inference refinements like FreeInit, allow models to improve temporal smoothness and subject appearance without expensive, repeated retraining [3][4].

## Multimodal Fusion and Integration
Contemporary research emphasizes the synthesis of videos that are tightly aligned with audio and textual conditioning. Unified frameworks, such as the Tri-Modal Diffusion Transformer (3MDiT), treat video, audio, and text as jointly evolving streams, employing "omni-blocks" for explicit feature-level fusion [3]. These models often utilize large language models (LLMs) or multimodal LLMs as orchestrators, mapping linguistic hidden states into semantic spaces accessible by diffusion generators [4]. Furthermore, explicit alignment techniques—such as injecting phonetic and rhythmic instructions into acoustic generation—ensure that sound and motion remain synchronized [8].

## Evaluation Frameworks
As generative models grow more complex, simple metrics like the Fréchet Video Distance (FVD) have proven insufficient to capture human-centric nuances. Consequently, the research community has shifted toward hierarchical benchmark suites like VBench++ and Video-Bench, which employ Large Multimodal Models (MLLMs) to score videos on criteria such as motion quality, instruction-following, and cross-modal consistency [6][7]. These MLLM-based evaluators use "chain-of-query" mechanisms to mimic human judgment, providing more reliable feedback on model performance in real-world, instruction-heavy scenarios [5].

## Trends and Open Problems
The field is currently moving toward unified, flexible architectures capable of handling diverse multimodal inputs, including reference images and audio [9]. Despite significant progress, several challenges remain. Achieving long-range temporal consistency without artifact accumulation remains difficult for autoregressive approaches [8]. Physical grounding—ensuring that generated actions obey real-world physics—is increasingly identified as a critical bottleneck for high-utility video generation [2]. Finally, as models achieve higher degrees of realism, ensuring safety and mitigating the risks of synthetic media (such as misinformation or non-consensual content) remains a paramount concern for researchers and developers alike [8].

## References
[1] Video Diffusion Models: A Survey. arxiv. https://arxiv.org/abs/2405.03150 (2024-11-17)
[2] Video diffusion generation: comprehensive review and open problems. web. https://link.springer.com/article/10.1007/s10462-025-11331-6 (2025-08-20)
[3] 3MDiT: Unified Tri-Modal Diffusion Transformer for Text-Driven Synchronized Audio-Video Generation. arxiv. https://arxiv.org/abs/2511.21780 (2025-11-26)
[4] JavisGPT: A Unified Multi-modal LLM. web. https://proceedings.neurips.cc/paper_files/paper/2025/file/d1422213c9f2bdd5178b77d166fba86a-Paper-Conference.pdf (2025-01-01)
[5] A Survey of AI-Generated Video Evaluation. web. https://arxiv.org/pdf/2410.19884 (2024-10-25)
[6] VBench++: Comprehensive and Versatile Benchmark Suite for Video Generative Models. hf-search. https://huggingface.co/papers/2411.13503 (2024-11-20)
[7] Video-Bench: Human-Aligned Video Generation Benchmark. hf-search. https://huggingface.co/papers/2504.04907 (2025-04-07)
[8] Text-to-video generators: a comprehensive survey. web. https://link.springer.com/article/10.1186/s40537-025-01314-3 (2025-11-14)
[9] SkyReels-V3 Technique Report. hf-search. https://huggingface.co/papers/2601.17323 (2026-01-24)

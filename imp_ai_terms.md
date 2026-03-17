# Essential AI/ML Terms Every Developer Should Know

A comprehensive glossary of artificial intelligence and machine learning terminology for software developers.

---

## Core Concepts

### Artificial Intelligence (AI)
**Definition:** The broad field of computer science focused on creating systems capable of performing tasks that typically require human intelligence. This includes reasoning, learning, perception, decision-making, and language understanding.

**Developer Context:** AI encompasses everything from simple rule-based systems to complex neural networks. Modern AI development largely focuses on machine learning approaches.

### Machine Learning (ML)
**Definition:** A subset of AI where systems learn patterns from data without being explicitly programmed for each scenario. Models improve through experience (training) rather than hard-coded rules.

**Developer Context:** Most practical AI applications today use ML. Developers work with training data, model architectures, and inference pipelines.

### Deep Learning (DL)
**Definition:** A specialized branch of ML that uses multi-layered neural networks (deep neural networks) to learn hierarchical representations of data. Particularly effective for image, speech, and text processing.

**Developer Context:** Requires specialized frameworks (TensorFlow, PyTorch), GPU acceleration, and careful attention to model architecture design.

### Neural Network
**Definition:** A computational model inspired by biological neurons, consisting of interconnected nodes (neurons) organized in layers. Each connection has a weight that gets adjusted during training.

**Developer Context:** Basic building block of deep learning. Understanding forward propagation, backpropagation, and gradient descent is essential.

---

## Model Types & Architectures

### Large Language Model (LLM)
**Definition:** A transformer-based neural network trained on vast amounts of text data, capable of understanding and generating human-like text. Examples include GPT-4, Claude, and Llama.

**Developer Context:** Used for chat applications, code generation, summarization, translation, and more. Consider prompt engineering, token limits, and API costs when integrating.

### Transformer Architecture
**Definition:** A neural network architecture based on self-attention mechanisms, introduced in "Attention Is All You Need" (2017). Excels at handling sequential data like text.

**Developer Context:** Foundation for GPT, BERT, T5, and most modern LLMs. Understanding attention mechanisms helps with model optimization and debugging.

### Convolutional Neural Network (CNN)
**Definition:** A neural network architecture designed for processing grid-like data (images). Uses convolutional layers to detect spatial hierarchies of features.

**Developer Context:** Standard for image classification, object detection, and computer vision tasks. Common frameworks: ResNet, EfficientNet, YOLO.

### Recurrent Neural Network (RNN)
**Definition:** A neural network with loops that allow information to persist, designed for sequential data. Variants include LSTM (Long Short-Term Memory) and GRU (Gated Recurrent Unit).

**Developer Context:** Historically used for NLP and time series, though largely superseded by transformers for text tasks. Still relevant for certain sequential problems.

### Generative Adversarial Network (GAN)
**Definition:** A model architecture consisting of two networks—a generator (creates synthetic data) and a discriminator (distinguishes real from fake)—that train adversarially.

**Developer Context:** Used for image generation, style transfer, data augmentation. Famous examples: StyleGAN, CycleGAN.

### Diffusion Model
**Definition:** A generative model that learns to gradually denoise data from random noise. Used in state-of-the-art image generation systems like DALL-E 2, Stable Diffusion, and Midjourney.

**Developer Context:** Current SOTA for image generation. Involves forward/backward diffusion processes and requires significant computational resources.

---

## Training & Inference

### Training
**Definition:** The process of teaching a machine learning model by feeding it labeled data (supervised) or finding patterns in unlabeled data (unsupervised). The model adjusts its internal parameters (weights) through backpropagation.

**Developer Context:** Most expensive phase computationally. Requires data preparation, model selection, hyperparameter tuning, and monitoring for overfitting.

### Inference
**Definition:** The phase where a trained model makes predictions on new, unseen data. Much less computationally intensive than training.

**Developer Context:** Production AI systems spend most resources on inference. Optimization techniques include model quantization, pruning, distillation, and hardware acceleration.

### Fine-tuning
**Definition:** The process of taking a pre-trained model (e.g., GPT-4) and further training it on a smaller, task-specific dataset to adapt it for a particular use case.

**Developer Context:** Cost-effective way to create specialized models. Requires understanding of learning rates, gradient updates, and potential catastrophic forgetting.

### Transfer Learning
**Definition:** Using knowledge gained from solving one problem to solve a different but related problem. Typically involves using a pre-trained model as a starting point.

**Developer Context:** Standard practice in modern ML development. Saves significant time and computational resources compared to training from scratch.

### Hyperparameter Tuning
**Definition:** The process of optimizing the configuration parameters of a model (learning rate, batch size, number of layers, etc.) that are set before training begins.

**Developer Context:** Can significantly impact model performance. Tools: Grid Search, Random Search, Bayesian Optimization, Optuna, Ray Tune.

---

## Data & Evaluation

### Training Set
**Definition:** The portion of data (typically 60-80%) used to train the model—teaching it patterns and relationships.

**Developer Context:** Quality and diversity of training data directly impact model performance. Ensure representative samples and proper labeling.

### Validation Set
**Definition:** The portion of data (typically 10-20%) used during training to tune hyperparameters and monitor for overfitting.

**Developer Context:** Used to make decisions about model architecture and hyperparameters. Don't use test data for this.

### Test Set
**Definition:** The portion of data (typically 10-20%) used only after training is complete to evaluate the final model's performance on unseen data.

**Developer Context:** Provides unbiased estimate of real-world performance. Keep it separate from training and validation—don't peek!

### Ground Truth
**Definition:** The known, correct labels or outcomes in supervised learning. The "answer key" against which predictions are compared.

**Developer Context:** Essential for evaluating model accuracy. Ground truth quality determines evaluation reliability.

### Labeled Data
**Definition:** Training data where each input example is paired with its correct output (supervision). Creating labeled data often requires human annotation.

**Developer Context:** Labeled data is expensive and time-consuming to create. Consider semi-supervised learning or weak supervision when labeling budget is limited.

### Embedding
**Definition:** A dense vector representation of discrete data (words, images, etc.) in a continuous vector space. Similar items have similar embeddings.

**Developer Context:** Foundation of modern NLP. Word2Vec, GloVe, BERT embeddings. Used in semantic search, recommendation systems, and as input features.

### Feature Engineering
**Definition:** The process of selecting, transforming, and creating input variables (features) from raw data to improve model performance.

**Developer Context:** Historically critical for ML. Less important with deep learning (which can learn features automatically), but still valuable for tabular data and model efficiency.

---

## Performance Metrics

### Accuracy
**Definition:** The proportion of correct predictions out of all predictions made. Common classification metric.

**Developer Context:** Can be misleading with imbalanced datasets. Use precision, recall, and F1-score for better insights.

### Precision
**Definition:** The proportion of true positives among all positive predictions. "When the model says positive, how often is it correct?"

**Developer Context:** Important when false positives are costly (spam detection, legal document review).

### Recall (Sensitivity)
**Definition:** The proportion of true positives that were correctly identified. "Of all actual positives, how many did we find?"

**Developer Context:** Critical when missing positives is dangerous (medical diagnosis, fraud detection).

### F1-Score
**Definition:** The harmonic mean of precision and recall. Balances both metrics into a single score.

**Developer Context:** Useful when you need to balance precision and recall, or with imbalanced datasets.

### ROC-AUC
**Definition:** Area Under the Receiver Operating Characteristic curve. Measures model's ability to discriminate between classes across all classification thresholds.

**Developer Context:** Popular for binary classification problems, especially with imbalanced data. Values range from 0.5 (random) to 1.0 (perfect).

### Mean Squared Error (MSE)
**Definition:** The average of squared differences between predicted and actual values. Common regression metric.

**Developer Context:** Punishes large errors more heavily. Use RMSE (Root MSE) for interpretability in original units.

### Perplexity
**Definition:** A measure of how well a probability model predicts a sample. Lower perplexity indicates better performance. Commonly used for language models.

**Developer Context:** Standard metric for evaluating language models. Equivalent to exp(cross-entropy loss).

---

## Common Issues & Challenges

### Hallucination
**Definition:** When an AI model generates false, misleading, or fabricated information that appears plausible. Common in LLMs where the model produces confident but incorrect statements.

**Developer Context:** Major challenge for production AI applications. Mitigation strategies: retrieval-augmented generation (RAG), citation requirements, human review, temperature control, and prompt engineering.

### Overfitting
**Definition:** When a model learns the training data too well, including noise and outliers, resulting in poor performance on new, unseen data. The model "memorizes" rather than generalizes.

**Developer Context:** Signs: training accuracy high, validation/test accuracy low. Solutions: more data, regularization, dropout, early stopping, simpler models.

### Underfitting
**Definition:** When a model is too simple to capture the underlying patterns in the data, resulting in poor performance on both training and test data.

**Developer Context:** Signs: training accuracy low, validation accuracy similarly low. Solutions: more complex model, better features, less regularization, more training.

### Bias-Variance Tradeoff
**Definition:** The fundamental tension in ML: high bias (underfitting, oversimplified model) vs. high variance (overfitting, too complex model). The goal is finding the optimal balance.

**Developer Context:** Guided model selection and regularization tuning. As model complexity increases, bias decreases but variance increases.

### Catastrophic Forgetting
**Definition:** When a neural network learns new information but rapidly forgets previously learned information. Common in sequential learning scenarios.

**Developer Context:** Challenge for continual learning and fine-tuning. Solutions: elastic weight consolidation, progressive networks, replay buffers.

### Mode Collapse
**Definition:** In generative models (especially GANs), when the generator produces limited variety of outputs, ignoring modes in the data distribution.

**Developer Context:** Generator finds a few outputs that fool the discriminator and reuses them. Solutions: mini-batch discrimination, unrolled GANs, different architecture.

### Vanishing/Exploding Gradients
**Definition:** In deep neural networks, gradients that become extremely small (vanish) or large (explode) during backpropagation, hindering training.

**Developer Context:** Common with deep networks and certain activation functions. Solutions: proper weight initialization, batch normalization, gradient clipping, residual connections.

---

## Specialized Techniques

### Prompt Engineering
**Definition:** The practice of crafting input prompts to elicit desired behaviors from large language models. Involves structuring queries, providing context, and using specific prompting techniques.

**Developer Context:** Critical skill for working with LLMs via APIs. Techniques: few-shot prompting, chain-of-thought, system prompts, role-playing, template design.

### Retrieval-Augmented Generation (RAG)
**Definition:** An architecture that combines retrieval-based and generative approaches. First retrieves relevant information from a knowledge base, then uses that context to generate accurate responses.

**Developer Context:** Reduces hallucinations and provides up-to-date information. Implementation: vector database + LLM. Tools: LangChain, LlamaIndex, Pinecone.

### Reinforcement Learning from Human Feedback (RLHF)
**Definition:** A training technique for aligning AI systems with human preferences. Humans rank model outputs, a reward model is trained on these rankings, and the main model is fine-tuned with reinforcement learning.

**Developer Context:** Used to train helpful, harmless, and honest AI assistants (ChatGPT, Claude). Expensive and complex process.

### Quantization
**Definition:** Reducing the numerical precision of model weights and activations (e.g., from 32-bit floats to 8-bit integers) to reduce model size and accelerate inference.

**Developer Context:** Essential for deploying models on edge devices and reducing inference costs. Can be applied during or after training. Trade-off: slight accuracy loss for efficiency gains.

### Pruning
**Definition:** Removing unnecessary weights, neurons, or layers from a neural network to reduce size and computational requirements.

**Developer Context:** Can dramatically reduce model size with minimal accuracy loss. Types: weight pruning, neuron pruning, layer pruning.

### Knowledge Distillation
**Definition:** Training a smaller, more efficient "student" model to mimic the behavior of a larger, more powerful "teacher" model.

**Developer Context:** Effective for model compression while preserving performance. Used in TinyBERT, DistilGPT, and many production models.

### Attention Mechanism
**Definition:** A neural network component that allows the model to focus on different parts of the input sequence when producing each element of the output sequence. The key innovation behind transformers.

**Developer Context:** Enables models to handle long-range dependencies. Self-attention, multi-head attention are key concepts. Essential for understanding transformer models.

---

## Development & Operations

### Model Drift
**Definition:** The degradation of model performance over time due to changes in the underlying data distribution. Also known as data drift or concept drift.

**Developer Context:** Models trained on today's data may become obsolete tomorrow. Solution: continuous monitoring, periodic retraining, and drift detection systems.

### MLOps
**Definition:** The practice of applying DevOps principles to machine learning systems. Includes model versioning, continuous integration/deployment, monitoring, and governance.

**Developer Context:** Essential for production ML. Tools: MLflow, Kubeflow, TensorFlow Extended (TFX), Weights & Biases, Evidently.

### Model Versioning
**Definition:** Tracking and managing different versions of ML models, their training data, hyperparameters, and code. Similar to Git for models.

**Developer Context:** Critical for reproducibility, rollback, and A/B testing. Tools: DVC, MLflow Models, Weights & Biases.

### A/B Testing
**Definition:** Comparing two versions of a model (or system) by randomly assigning users to each and measuring performance metrics.

**Developer Context:** Standard method for evaluating model improvements in production. Requires careful statistical analysis and traffic splitting.

### Canary Deployment
**Definition:** Gradually rolling out a new model to a small subset of users before full deployment, allowing for monitoring and quick rollback if issues arise.

**Developer Context:** Reduces risk of bad model deployments. Part of safe ML deployment strategies.

### Model Interpretability
**Definition:** Techniques and methods to understand how ML models make decisions. Makes model behavior transparent and explainable.

**Developer Context:** Required for regulatory compliance (e.g., EU AI Act), debugging, and user trust. Techniques: SHAP, LIME, feature importance, attention visualization.

### Responsible AI
**Definition:** The practice of developing and deploying AI systems ethically, considering fairness, transparency, privacy, accountability, and social impact.

**Developer Context:** Increasingly important for compliance and brand reputation. Check for bias, ensure accessibility, protect user data, document limitations.

---

## Advanced Topics

### Few-Shot / Zero-Shot Learning
**Definition:** Few-shot: learning from very few examples (1-5 per class). Zero-shot: classifying/processing inputs from classes never seen during training.

**Developer Context:** Enabled by large pre-trained models. Useful for rapidly adapting to new tasks without extensive retraining.

### Embedding Space
**Definition:** The continuous, lower-dimensional vector space where learned representations (embeddings) of data points reside. Similar items cluster together.

**Developer Context:** Used for semantic search, clustering, recommendation. Visualization techniques (t-SNE, UMAP) help explore this space.

### Embedding Dimension
**Definition:** The size (number of elements) of the vectors in an embedding space. Higher dimensions can capture more nuance but increase computation costs.

**Developer Context:** Trade-off: larger dimension = more expressive but slower. Common: 768, 1024, 4096 for text embeddings.

### Token
**Definition:** A discrete unit of text (word, subword, or character) that serves as input to language models. LLMs process sequences of tokens.

**Developer Context:** Important for API cost calculation, context window management, and model input preparation. Tokenization strategies affect model performance.

### Context Window
**Definition:** The maximum number of tokens (words/subwords) that an LLM can process in a single input-output cycle. Also called context length or sequence length.

**Developer Context:** Critical limitation when designing applications. Strategies: truncation, summarization, retrieval-augmented approaches, context-winding.

### Temperature
**Definition:** A parameter that controls the randomness of LLM outputs. Lower temperature = more deterministic, higher temperature = more creative/random.

**Developer Context:** Tune for application: low (0.1-0.3) for factual Q&A, medium (0.5-0.7) for balanced responses, high (0.8-1.2) for creative tasks.

### Top-p (Nucleus) Sampling
**Definition:** A stochastic decoding strategy where the model samples from the smallest set of tokens whose cumulative probability exceeds p (e.g., 0.9), rather than considering all tokens.

**Developer Context:** Often used with temperature for better quality text generation. Helps avoid low-probability nonsense tokens.

### Chain-of-Thought (CoT)
**Definition:** A prompting technique that encourages LLMs to reason step-by-step before providing a final answer, similar to showing work in math problems.

**Developer Context:** Dramatically improves performance on complex reasoning tasks. Use phrases like "Let's think step by step" or provide examples with reasoning.

### Vector Database
**Definition:** A database optimized for storing and querying high-dimensional vectors (embeddings) with similarity search capabilities.

**Developer Context:** Essential component of RAG systems and semantic search. Popular options: Pinecone, Weaviate, Qdrant, Milvus, pgvector.

### Mixture of Experts (MoE)
**Definition:** A model architecture where different "expert" subnetworks specialize in different types of inputs, with a router deciding which experts to activate for each input.

**Developer Context:** Enables larger model capacity with fewer active parameters during inference. Used in models like Mixtral 8x7B and GPT-4.

### Parameter
**Definition:** The learnable weights and biases in a neural network. The number of parameters indicates model size and capacity.

**Developer Context:** More parameters generally mean more capability but higher compute costs. Current LLMs range from billions to trillions of parameters.

### Compute-Optimal Scaling
**Definition:** The principle that model performance improves predictably with increased training compute, data, and parameters up to certain limits.

**Developer Context:** Chinchilla scaling laws inform optimal model size given training compute budget. More data+compute often better than bigger model alone.

### In-Context Learning
**Definition:** The ability of LLMs to learn from examples provided within the prompt without updating model weights. The model uses these examples as context for subsequent queries.

**Developer Context:** Enables few-shot learning via prompting. Limited by context window. Different from fine-tuning as no parameter updates occur.

### System Prompt
**Definition:** A hidden or special prompt that sets the behavior, constraints, and personality of an AI system before user interactions begin.

**Developer Context:** Crucial for defining AI assistant behavior, safety guidelines, and response formats. Often processed differently than user prompts.

### Guardrails
**Definition:** Mechanisms (prompt-based, filtering, or architectural) that prevent AI systems from generating harmful, inappropriate, or undesired content.

**Developer Context:** Essential for production deployments. Can be implemented via prompt engineering, input/output filters, or constitutional AI approaches.

### Constitutional AI
**Definition:** An AI training approach where models critique and revise their own outputs according to a set of constitutional principles, reducing the need for human feedback on harms.

**Developer Context:** Developed by Anthropic for creating helpful, harmless, and honest AI systems. Can scale supervision beyond human capacity.

### Constitutional AI
**Definition:** An AI training approach where models critique and revise their own outputs according to a set of constitutional principles, reducing the need for human feedback on harms.

**Developer Context:** Developed by Anthropic for creating helpful, harmless, and honest AI systems. Can scale supervision beyond human capacity.

### Diffusion
**Definition:** A generative modeling technique where noise is gradually added to data (forward diffusion) and then learned to be removed (reverse diffusion) to generate new samples.

**Developer Context:** State-of-the-art for image generation. Process involves many denoising steps. Recent advances: diffusion transformers, latent diffusion.

### Model Interpretability
**Definition:** Methods and techniques to understand and explain how ML models make decisions. Makes model behavior transparent and interpretable to humans.

**Developer Context:** Important for debugging, regulatory compliance (especially in high-stakes domains), and building user trust. Approaches: post-hoc explanations, inherently interpretable models.

---

## Framework & Library Terms

### Tensor
**Definition:** The fundamental data structure in deep learning frameworks. A multi-dimensional array (similar to numpy arrays but with GPU support and automatic differentiation).

**Developer Context:** Operations on tensors are the building blocks of model computation. Shape, rank, dtype are key properties.

### Automatic Differentiation (Autograd)
**Definition:** A technique for automatically computing gradients of operations in a computational graph. Essential for training neural networks via backpropagation.

**Developer Context:** Frameworks like PyTorch and TensorFlow track operations on tensors and can compute gradients automatically. Enables gradient-based optimization.

### Computational Graph
**Definition:** A directed acyclic graph representing mathematical operations in a neural network. Nodes are operations, edges are tensors flowing between operations.

**Developer Context:** Underlies automatic differentiation. Dynamic graphs (PyTorch) vs static graphs (TensorFlow 1.x).

### Epoch
**Definition:** One complete pass through the entire training dataset during model training.

**Developer Context:** Multiple epochs typically needed for convergence. Number of epochs is a hyperparameter. Watch for overfitting in later epochs.

### Batch Size
**Definition:** The number of training examples processed before the model's parameters are updated.

**Developer Context:** Trade-off: larger batches = more stable gradients but more memory; smaller batches = more updates, possibly better generalization. Common sizes: 16, 32, 64, 128.

### Learning Rate
**Definition:** A hyperparameter that controls how much to adjust model weights in response to estimated error during training. Usually represented as a small decimal (e.g., 0.001).

**Developer Context:** Most important hyperparameter! Too high = unstable training; too low = slow/gets stuck. Often use learning rate schedules or warmup.

### Gradient Descent
**Definition:** The optimization algorithm used to minimize the loss function by iteratively adjusting parameters in the direction of steepest descent (negative gradient).

**Developer Context:** Foundation of neural network training. Variants: SGD, Adam, RMSprop, Adagrad. Adam is most commonly used default.

### Stochastic Gradient Descent (SGD)
**Definition:** A variant of gradient descent where updates are made using a randomly selected subset (batch) of training data rather than the entire dataset.

**Developer Context:** More computationally efficient and can escape local minima better than batch gradient descent. Implemented via mini-batch processing.

### Activation Function
**Definition:** A mathematical function applied to each neuron's output, introducing non-linearity into the network. Common: ReLU, Sigmoid, Tanh, GELU.

**Developer Context:** Enables neural networks to learn complex, non-linear relationships. ReLU is most common in hidden layers. Output layer activation depends on task (softmax for classification).

### Backpropagation
**Definition:** The algorithm for efficiently computing gradients in neural networks. Works backwards from the output layer to compute error gradients for each layer.

**Developer Context:** Core algorithm that makes deep learning possible. Uses chain rule to propagate gradients through computational graph.

### Dropout
**Definition:** A regularization technique where randomly selected neurons are "dropped out" (temporarily deactivated) during training to prevent overfitting.

**Developer Context:** Simple but effective regularization. Typical dropout rates: 0.2-0.5. Turn off during inference.

### Batch Normalization
**Definition:** A technique that normalizes the inputs to each layer, reducing internal covariate shift and enabling faster, more stable training.

**Developer Context:** Allows higher learning rates and reduces sensitivity to initialization. Usually not used with dropout. Operates on mini-batch statistics during training.

---

## Prompt Engineering Terms (LLM-Specific)

### Prompt
**Definition:** The input text provided to a language model that instructs it on what task to perform. Can include instructions, context, examples, and the actual query.

**Developer Context:** Crafting effective prompts is crucial for good LLM performance. Structure: role, task, context, format specification.

### System Prompt
**Definition:** A special instruction (often hidden from end users) that defines the AI's behavior, constraints, personality, and response format. Sets the overall context.

**Developer Context:** Used to establish guardrails, define expertise, set tone, and specify formatting requirements. Usually placed at the beginning of the conversation.

### User Prompt
**Definition:** The actual query or instruction from the end user. Combined with the system prompt and possibly conversation history.

**Developer Context:** What your application's users see and provide. May need preprocessing, validation, or augmentation before passing to LLM.

### Few-Shot Prompting
**Definition:** Providing a few example input-output pairs within the prompt to demonstrate the desired behavior before presenting the actual query.

**Developer Context:** Helps models understand task format and desired response style. Each example consumes tokens from context window.

### Zero-Shot Prompting
**Definition:** Asking the model to perform a task without providing any examples, relying solely on its pre-trained knowledge.

**Developer Context:** Simpler, uses fewer tokens, but may produce less consistent results than few-shot for specialized formats.

### One-Shot Prompting
**Definition:** Providing exactly one example in the prompt, between zero-shot and few-shot.

**Developer Context:** Single example can dramatically improve formatting consistency for tasks with specific output structures.

### Chain-of-Thought (CoT) Prompting
**Definition:** Prompting technique that elicits step-by-step reasoning from the model. Can include examples showing intermediate reasoning steps.

**Developer Context:** Particularly effective for math, logic, and multi-step reasoning tasks. Can be combined with few-shot examples ("few-shot CoT").

### Role-Playing Prompt
**Definition:** Assigning a specific persona or expertise to the LLM (e.g., "You are a senior Python developer...").

**Developer Context:** Can improve response quality by activating relevant knowledge patterns and adjusting language/style appropriately.

### Prompt Template
**Definition:** A structured format for prompts with placeholders for dynamic content. Enables systematic prompt construction.

**Developer Context:** Essential for production applications. Libraries like Jinja2 or LangChain's PromptTemplate facilitate this. Improves consistency and maintainability.

### Temperature
**Definition:** Controls randomness in generation. Lower values (0.1-0.3) make output more deterministic; higher values (0.7-1.0+) increase creativity/variability.

**Developer Context:** Tune per use case: low for factual Q&A/code; medium for general conversation; high for creative writing/ideation. Use temperature=0 for deterministic outputs.

### Top-K Sampling
**Definition:** At each generation step, only consider the K most likely next tokens, discarding others before sampling.

**Developer Context:** Simple way to reduce nonsense outputs. Common K: 40-50. Doesn't dynamically adapt to probability distribution shape.

### Top-P (Nucleus) Sampling
**Definition:** At each generation step, consider the smallest set of tokens whose cumulative probability exceeds p (e.g., 0.9), sample from that set.

**Developer Context:** Often better than top-k as it adapts to the distribution. May consider fewer than K tokens if low-probability tail is long. Default in many LLMs: p=0.9-0.95.

### Maximum Likelihood Estimation (MLE)
**Definition:** The standard training objective for language models—predicting the next token given context, maximizing the probability of the actual next token in training data.

**Developer Context:** What LLMs do during training. At inference, greedy MLE decoding can produce repetitive text; sampling strategies preferred.

### Beam Search
**Definition:** A search algorithm that keeps track of multiple candidate sequences (beams) during generation to find sequences with higher overall probability.

**Developer Context:** Can find higher-probability sequences than greedy decoding but may produce repetitive text. Often used with length penalty. Not ideal for conversational use.

### Token
**Definition:** The unit of text processing in LLMs. Can be whole words, subwords, or characters depending on tokenizer. Not exactly equal to words.

**Developer Context:** Important for cost calculation (most APIs charge per token), context management, and understanding model limits. Estimate: ~4 characters per token for English.

### Context Window
**Definition:** The maximum number of tokens an LLM can process in a single API call (includes both input and output). Also called context length or max sequence length.

**Developer Context:** Major constraint for applications. Limits: retrieval-augmented generation (RAG), summarization of long documents, multi-turn conversations. Solutions: chunking, summarization, sliding window.

### Token Limitation
**Definition:** The constraint on the number of tokens an LLM can accept as input in a single request. Excess tokens beyond the context window are truncated.

**Developer Context:** Must be managed in production systems. Count tokens before sending to API. Strategy: relevant context selection, summarization, hierarchical processing.

### Prompt Injection
**Definition:** A malicious technique where adversaries craft inputs that override or manipulate the system prompt, causing the LLM to ignore instructions or reveal sensitive information.

**Developer Context:** Security vulnerability in LLM applications. Mitigation: input filtering, output scanning, defense-in-depth, validating LLM outputs, not trusting LLM decisions for security-critical paths.

### Jailbreak
**Definition:** User prompts designed to circumvent safety guardrails and elicit harmful, unethical, or policy-violating content from an AI system.

**Developer Context:** Challenge for deployed systems. Defense: multiple layers of validation, input/output filtering, constitutional AI principles, not over-relying on prompt-based safety.

---

## Ethics & Safety

### AI Alignment
**Definition:** The research problem of ensuring AI systems act in accordance with human values, intentions, and ethical principles.

**Developer Context:** Critical as AI systems become more capable. encompasses: value learning, interpretability, robustness, avoiding reward hacking.

### Hallucination
**Definition:** When an AI model generates false, misleading, or nonsensical information with high confidence. "Confidently incorrect."

**Developer Context:** Major issue for factual applications. Never trust LLM outputs without verification. Mitigate with: RAG, citations, human review, constraint prompts.

### Bias in AI
**Definition:** Systematic and unfair discrimination in AI system outputs, often reflecting biases present in training data or algorithm design.

**Developer Context:** Can manifest as gender, racial, ethnic, or other biases. Test for bias, use diverse datasets, apply fairness constraints, include diverse teams in development.

### Fairness Metrics
**Definition:** Quantitative measures of how equally an AI system performs across different demographic groups. Common: demographic parity, equal opportunity, equalized odds.

**Developer Context:** Required for responsible AI development. Trade-offs often exist between different fairness metrics and accuracy.

### Model Card
**Definition:** A documentation framework for ML models that reports performance across different demographics, intended use cases, limitations, and ethical considerations.

**Developer Context:** Increasingly expected by stakeholders and regulators. Promotes transparency and informed use. Similar to nutrition labels for models.

### Data Card / Dataset Documentation
**Definition:** Documentation that describes a dataset's composition, collection methods, preprocessing, intended uses, and potential biases.

**Developer Context:** Essential for reproducibility and ethical use. Helps users understand dataset limitations and appropriate applications.

---

## Infrastructure & Tooling

### Containerization (Docker)
**Definition:** Packaging an application and its dependencies into a standardized unit (container) that runs consistently across different environments.

**Developer Context:** Essential for reproducible ML deployments. Include CUDA versions, Python environment, model files, and inference code.

### Kubernetes
**Definition:** An orchestration platform for managing containerized applications across clusters of machines.

**Developer Context:** Used for scaling ML inference services, managing model deployments, and ensuring high availability.

### ONNX (Open Neural Network Exchange)
**Definition:** An open format for representing machine learning models, enabling interoperability between different frameworks (PyTorch, TensorFlow, etc.).

**Developer Context:** Facilitates model conversion for deployment to different hardware targets (CPU, GPU, edge devices).

### TensorRT
**Definition:** NVIDIA's platform for high-performance deep learning inference on GPUs. Optimizes models through layer fusion, precision calibration, and kernel auto-tuning.

**Developer Context:** Can provide 5-10x speedup for inference on NVIDIA GPUs. Support for TensorFlow, PyTorch, ONNX models.

### Triton Inference Server
**Definition:** NVIDIA's open-source inference serving software that supports multiple frameworks and optimizes GPU utilization for production deployments.

**Developer Context:** Handles concurrent requests, dynamic batching, model ensemble execution, and multi-GPU scaling. Industry standard for high-throughput serving.

### Model Servicing
**Definition:** The infrastructure and processes for hosting trained models and providing low-latency, scalable inference APIs.

**Developer Context:** Production systems need: scaling, monitoring, versioning, A/B testing, request routing. Solutions: TorchServe, TensorFlow Serving, KServe, Seldon Core.

---

## Performance Monitoring

### Real-User Monitoring (RUM)
**Definition:** Tracking actual user interactions with ML-powered features in production, including latency, accuracy feedback, and business metrics.

**Developer Context:** Captures the full user experience including network latency, frontend rendering, and business outcome—different from offline metrics.

### Shadow Mode
**Definition:** Running a new model in production alongside the existing system without affecting users, while comparing its predictions against the production model.

**Developer Context:** Safe way to test model performance on real traffic before full deployment. Log both models' outputs for comparison.

### A/B Testing (Canary Deployment)
**Definition:** Gradual rollout of a new model to a small percentage of traffic, monitoring for regressions before full deployment.

**Developer Context:** Production best practice. Enable quick rollback if metrics degrade. Monitor both ML metrics and business KPIs.

### Drift Detection
**Definition:** Monitoring systems that alert when the statistical properties of incoming data differ significantly from training data distribution.

**Developer Context:** Essential for maintaining model performance. Methods: statistical tests (KS test), embedding distance monitoring, prediction distribution analysis.

### Model Degradation
**Definition:** The gradual decline in model performance over time due to changes in data distribution, feature relationships, or world events.

**Developer Context:** Normal for most models. Requires retraining or updating. Expect degeneration after weeks or months depending on domain volatility.

---

## Regulatory & Compliance

### Explainable AI (XAI)
**Definition:** Techniques and methods that make AI model decisions interpretable and understandable to humans. Often required for high-stakes decisions.

**Developer Context:** Legal/regulatory need in finance, healthcare, hiring, etc. Techniques: SHAP, LIME, attention visualization, feature importance.

### GDPR (General Data Protection Regulation)
**Definition:** EU regulation on data protection and privacy that affects AI development, including requirements for automated decision-making transparency and data subject rights.

**Developer Context:** Impacts: data collection consent, right to explanation, automated decision restrictions, data portability, breach notification.

### Algorithmic Accountability
**Definition:** The principle that organizations should be responsible for the impacts of their automated decision-making systems and able to explain their operation.

**Developer Context:** Emerging legal and ethical requirement. Document model development, data provenance, decision processes, and potential biases.

### AI Audit
**Definition:** Systematic evaluation of AI systems for compliance, fairness, performance, and risk. Different from model evaluation—examines the entire system and process.

**Developer Context:** Increasingly required by regulators and enterprise customers. Includes: data lineage, model provenance, bias testing, security assessment.

### Right to Explanation
**Definition:** A legal concept (prominent in GDPR) that individuals have the right to obtain an explanation for automated decisions that significantly affect them.

**Developer Context:** Challenging for complex models like deep neural networks. May require post-hoc explanation methods or using inherently interpretable models in regulated contexts.

---

## Cost & Efficiency

### Cost per Token / Cost per 1K Tokens
**Definition:** Pricing metric used by LLM APIs (OpenAI, Anthropic, etc.) where customers pay per thousand tokens processed (input + output).

**Developer Context:** Major cost driver for applications. Calculate estimated monthly costs based on user volume, average token counts, and chosen model. Optimize with: caching, cheaper models for simple tasks, truncation, batching.

### Model Quantization
**Definition:** Reducing the numerical precision of model weights and activations (e.g., from 32-bit floating point to 8-bit integers).

**Developer Context:** Reduces model size by ~4x and increases inference speed with small accuracy trade-off. Types: post-training quantization, quantization-aware training.

### Model Pruning
**Definition:** Removing unnecessary connections, neurons, or layers from a trained neural network to reduce size and computation requirements.

**Developer Context:** Can achieve 2-10x compression with minimal accuracy loss. Often followed by fine-tuning to recover performance.

### Knowledge Distillation
**Definition:** Training a smaller "student" model to mimic the outputs (or internal representations) of a larger "teacher" model.

**Developer Context:** Popular technique for deploying compact models. Distilled models often achieve much of the teacher's performance at fraction of the size and cost. Examples: DistilBERT, TinyBERT.

### Latency
**Definition:** The time elapsed from when a request is sent to the model until a response is received. Critical for user experience.

**Developer Context:** LLM inference can take seconds. Optimize with: model optimization (quantization, pruning), hardware acceleration (GPU/TPU), efficient batching, and edge deployment.

### Throughput
**Definition:** The number of inference requests a model can process per unit of time (e.g., requests/second). Critical for cost efficiency at scale.

**Developer Context:** Trade-off with latency: batching increases throughput but can increase individual request latency. Requirements depend on application.

---

## Testing & Quality

### Unit Test
**Definition:** Testing individual components (functions, classes) in isolation to ensure they work correctly.

**Developer Context:** Essential for ML pipelines: test data preprocessing, model layers, metrics calculation. Use fixtures and mocks for reproducibility.

### Integration Test
**Definition:** Testing how different components work together (data pipeline → model → post-processing).

**Developer Context:** Catch issues in component interactions. Test: data flows correctly, shapes match, serialization/deserialization works, API responses formatted properly.

### Golden Dataset / Golden Set
**Definition:** A curated, high-quality test dataset with manually verified correct outputs that serves as a benchmark for model evaluation.

**Developer Context:** More reliable than automatically generated test sets. Used for regression testing—ensure model changes don't break known-good cases.

### Regression Test
**Definition:** Tests that ensure new code changes don't break existing functionality. In ML: ensure metrics don't degrade on benchmark datasets.

**Developer Context:** Automated CI/CD should include regression tests on golden datasets. Flag significant metric drops.

### Synthetic Data Generation
**Definition:** Using models (GANs, language models) to create artificial training data that mimics real data distributions.

**Developer Context:** Useful when real data is scarce, sensitive, or imbalanced. Quality control essential—synthetic data quality determines model quality.

### Data Augmentation
**Definition:** Creating modified versions of training examples to increase dataset diversity and improve model generalization.

**Developer Context:** Common in computer vision (rotations, flips, crops) and NLP (synonym replacement, back-translation). Simple but effective technique.

---

## Where to Learn More

### Official Documentation
- **PyTorch:** pytorch.org/docs
- **TensorFlow:** tensorflow.org/guide
- **Hugging Face:** huggingface.co/docs
- **OpenAI:** platform.openai.com/docs

### Courses
- **fast.ai** - Practical Deep Learning for Coders
- **Coursera** - Machine Learning by Andrew Ng
- **Stanford CS229** - Machine Learning (lecture notes)

### Papers
- **Attention Is All You Need** (2017) - Transformer architecture
- **BERT: Pre-training of Deep Bidirectional Transformers** (2018)
- **GPT Series** (2018-2023) - Generative Pre-trained Transformers
- **Language Models are Few-Shot Learners** (GPT-3, 2020)
- **Training Verifiers to Solve Math Word Problems** (Chain-of-Thought, 2021)

### Communities
- **r/MachineLearning** (Reddit)
- **Hugging Face Forums**
- **Papers With Code**
- **ML subreddits** (r/LocalLLaMA, r/learnmachinelearning)

---

## Quick Reference Table

| Term | Type | Key Points |
|------|------|------------|
| LLM | Architecture | Transformer-based, massive text training, in-context learning |
| RAG | Technique | Retrieval + generation, reduces hallucinations |
| Fine-tuning | Training | Adapt pre-trained model to specific task |
| Hallucination | Issue | False but confident outputs |
| Embedding | Representation | Dense vector semantic representation |
| Token | Unit | Subword text unit for LLMs |
| Temperature | Parameter | Controls randomness (0=deterministic, 1=creative) |
| Overfitting | Issue | Model memorizes training data |
| Cross-Entropy | Loss | Standard for classification |
| Autoencoder | Architecture | Learns efficient data encoding |
| GAN | Architecture | Generator + Discriminator, adversarial training |
| Transfer Learning | Technique | Reuse model for related tasks |
| Attention | Mechanism | Focus on relevant input parts |
| BERT | Model | Bidirectional encoder, good for classification |
| GPT | Model | Decoder-only, good for generation |
| Diffusion | Architecture | Denoising process for generation |
| Reinforcement Learning | Paradigm | Learn via rewards/penalties |
| Multi-modal | Capability | Process multiple data types (text+image) |
| Tokenization | Preprocessing | Text → tokens for model input |
| Context Window | Limitation | Max tokens per LLM request |
| Prompt Engineering | Technique | Craft inputs to get desired outputs |
| Few-shot | Technique | Provide examples in prompt |
| Hallucination | Problem | Model generates false info |
| Interpretability | Concern | Understanding model decisions |
| MLOps | Practice | ML in production (CI/CD, monitoring) |
| Quantization | Optimization | Reduce precision for efficiency |
| Pruning | Optimization | Remove unnecessary parameters |
| Distillation | Optimization | Small model from large model |

---

## Conclusion

This glossary covers the essential AI/ML terms every developer should know in 2024. The field evolves rapidly—stay curious, keep learning, and don't be afraid to experiment with new tools and techniques.

**Remember:** The best AI systems combine sound ML principles with thoughtful engineering, rigorous testing, and ethical consideration. Happy building!

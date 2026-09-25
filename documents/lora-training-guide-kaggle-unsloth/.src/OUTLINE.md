Section: Start with one repeatable adapter pipeline
Claim: A developer can fine-tune role behavior on Kaggle or an RTX 3060 by keeping the base frozen, training a small adapter, and validating before deployment.
Source: User request; Hugging Face PEFT LoRA guide; Unsloth model and workflow documentation.

Section: LoRA changes behavior without retraining the base
Claim: LoRA trains low-rank update matrices while leaving base weights frozen; QLoRA adds 4-bit base loading to reduce VRAM.
Source: Hugging Face PEFT conceptual LoRA guide.

Section: Standardize the fleet on one base
Claim: Adapters are architecture and checkpoint specific, so model choice is an operational standard, not a cosmetic preference.
Source: PEFT model behavior; llama.cpp adapter compatibility documentation; Qwen model cards.

Section: Dataset quality decides the adapter
Claim: A clean, licensed, representative dataset and held-out split matter more than raw row count.
Source: User-approved scope; common supervised fine-tuning practice.

Section: Kaggle is the zero-cost batch path
Claim: Kaggle can run an Unsloth QLoRA job headlessly through the CLI using a private GPU kernel and downloadable output.
Source: Kaggle CLI documentation and user-approved scope.

Section: One training script should run in both places
Claim: A parameterized Unsloth script minimizes drift between Kaggle and the local RTX 3060.
Source: Unsloth/Hugging Face workflow and user-approved scope.

Section: The RTX 3060 is the iteration path
Claim: The 12 GB RTX 3060 can be practical for 4B and careful 7B-8B QLoRA experiments by controlling sequence length, micro-batch, checkpointing, and optimizer state.
Source: User hardware statement; 4-bit/PEFT mechanics; practical configuration guidance.

Section: Export format follows the serving target
Claim: Keep the PEFT adapter for reuse and hot-swapping; produce GGUF or a merged model only when the runtime requires it.
Source: Unsloth save/export API; llama.cpp and vLLM adapter documentation.

Section: Evaluation is a gate, not a graph
Claim: A run ships only after held-out tests, baseline comparison, regression checks, and human review on open-ended outputs.
Source: User-approved scope; standard evaluation practice.

Section: Legal role adapters require retrieval and boundaries
Claim: A legal LoRA can teach response patterns, but current law and citations must come from verified retrieval, with jurisdiction and human-review controls.
Source: User-approved scope; legal role risk described in conversation.

Section: A one-page command sheet makes the workflow reusable
Claim: The minimum commands from authentication through download and inference can be run without reopening the full guide.
Source: Commands established in the guide.

Section: Sources
Claim: Every external technical claim can be traced to an accessible primary or practical source.
Source: Source URLs collected during research.

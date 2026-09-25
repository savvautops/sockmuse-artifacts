Section: Can we see what an LLM is thinking?
Claim: The model is not a black box because its internals are hidden; it is a black box because its fully visible computation is too distributed and entangled to read directly.
Source: Requester-provided explainer; Anthropic, “Mapping the mind of a large language model.”

Section: High-dimensional space is ordinary math with more coordinates
Claim: R^4096 is the same construction as a number line, a plane, or 3D space, just with 4,096 coordinates instead of one, two, or three.
Source: Requester-provided explainer; standard linear algebra.

Section: A token becomes a moving point, not a stored definition
Claim: Token embeddings and later hidden states are vectors whose meaning depends on context and changes layer by layer.
Source: Requester-provided explainer; Vaswani et al., “Attention Is All You Need.”

Section: The model repeats simple operations at enormous scale
Claim: Learned matrices, attention, nonlinear functions, and residual updates transform each token representation through tens of layers; LLaMA examples make the scale concrete.
Source: Requester-provided explainer; LLaMA paper, Table 2.

Section: Weights stay put, activations flash into existence
Claim: Weights are persistent learned settings, while activations are input-specific states recomputed on each forward pass and discarded afterward.
Source: Requester-provided explainer.

Section: Superposition packs many features into overlapping directions
Claim: Models can represent more useful features than they have cleanly separable dimensions by reusing directions, which makes single-neuron interpretation unreliable.
Source: Elhage et al., “Toy Models of Superposition”; Anthropic, “Mapping the mind of a large language model.”

Section: Nonlinear mixing turns tracing into unmixing paint
Claim: Repeated linear projections plus nonlinear gates cause features to combine, split, amplify, and suppress one another across layers, defeating simple backward narratives.
Source: Requester-provided explainer; Transformer and LLaMA architecture papers.

Section: Interpretability can find local circuits, not a complete transcript
Claim: Feature dictionaries and circuit tracing can reveal useful mechanisms, but they are approximations that do not yet produce a faithful, exhaustive explanation of a frontier model.
Source: Anthropic interpretability research; “Tracing the thoughts of a large language model.”

Section: The mystery is scale, distribution, and dynamics
Claim: The right takeaway is neither mysticism nor hopelessness; the numbers are observable, but turning them into human concepts remains an open scientific problem.
Source: Requester-provided conclusion and cited interpretability research.

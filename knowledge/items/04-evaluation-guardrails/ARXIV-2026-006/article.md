# Future Dynamic 3D Reconstruction: A 3D World Model with Disentangled Ego-Motion

---

- Local ID: ARXIV-2026-006
- Source: arXiv
- arXiv ID: 2606.18250v1
- Date: 2026-06-16
- Authors: Nils Morbitzer, Jonathan Evers, Artem Savkin, Thomas Stauner, Nassir Navab, Federico Tombari, Stefano Gasperini
- Categories: cs.CV
- URL: https://arxiv.org/abs/2606.18250v1
- PDF: https://arxiv.org/pdf/2606.18250v1
- Capture depth: metadata + abstract

---

## Abstract

Forecasting the evolution of dynamic environments is crucial for autonomous agents. While generative world models have recently achieved high photorealism in 2D video synthesis by mixing ego-motion and environmental dynamics within the image plane, they exhibit physical inconsistencies, such as morphing or vanishing objects, especially over long time horizons. In this paper, we propose FR3D, a world model that predicts a persistent 3D latent representation for future dynamic 3D reconstruction. Unlike prior works that treat the world as a sequence of image-based features, FR3D explicitly decouples the 3D evolution of the scene from the agent's trajectory, treating the inferred ego-motion as a latent proxy for action. This disentanglement resolves the ambiguities between self-motion and world-motion, ensuring geometric consistency into the future. Furthermore, we introduce a teacher-student distillation strategy that leverages the spatial "common sense" of off-the-shelf foundation models, leading to robust zero-shot generalization. Extensive experiments demonstrate FR3D's strong performance for future dynamic 3D reconstruction from monocular observations across multiple datasets, even 2 seconds into the future. Project page: https://fr3d-wm.github.io.

## Capture Notes

This is an abstract-level paper capture from the arXiv API. The PDF URL is preserved for full-text reading and later deep extraction.

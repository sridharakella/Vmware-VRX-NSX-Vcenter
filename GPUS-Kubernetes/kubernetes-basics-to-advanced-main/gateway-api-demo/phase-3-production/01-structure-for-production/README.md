# Gateway API – Production Structure (Phase 3)

This folder demonstrates how to structure Kubernetes Gateway API resources for **real production environments**.

Up to Phase 2, the focus was on learning how Gateway API works.
In Phase 3, the focus shifts to **how Gateway API is actually used by platform teams in production** — with environment separation, safety, and scalability in mind.


This example focuses on one core production problem:

> How do you structure Gateway API manifests so that
> multiple environments (staging, production) can safely share the same base configuration?

## Directory Structure

```
k8s/
├── base/
│   ├── gateway.yaml
│   ├── httproutes.yaml
│   └── apps.yaml
│
├── overlays/
│   ├── staging/
│   │   └── gateway-patch.yaml
│   │
│   └── prod/
│       └── client-settings.yaml
```

## Ownership Model

This structure reflects how real platform teams work:

- **base/**
  - Shared, stable resources
  - Owned by the platform team
  - Rarely changed

- **overlays/staging/**
  - Looser configuration for testing and validation
  - Fewer restrictions
  - Used to experiment safely

- **overlays/prod/**
  - Strict production policies
  - Client limits, upstream protection, and safety controls
  - Designed to reduce blast radius when things go wrong
 
## Why Staging and Production Are Not Identical

Staging is intentionally more permissive:
- Higher timeouts
- Fewer limits
- Easier debugging

Production is intentionally strict:
- Client request limits
- Backend protection
- Predictable failure behavior

This difference is **intentional** and reflects real-world production systems.

## How This Ties to the Video (Phase 3 – Video 1)

This example is used in **Phase 3 – Video 1** of the Kubernetes Gateway API series.

In this video, we focus on the **first production mistake** teams make after Gateway API starts working:
using flat, unstructured YAML that does not scale to real environments.

The manifests in this folder are used to demonstrate:

- Why flat Gateway API YAML works for demos but fails in production
- How platform teams separate shared configuration from environment-specific behavior
- Why staging and production must behave differently, even with the same base resources
- How Gateway API becomes the first line of defense before traffic reaches applications

This structure is intentionally simple but realistic.
Later Phase 3 videos will **build on top of this layout** to demonstrate:
- Canary and blue-green deployments
- Multi-tenant Gateway setups
- Zero-trust networking with mTLS

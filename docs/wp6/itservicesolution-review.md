# WP6: `bpo:ITServiceSolution`, a referent-level review

2026-11-03. Registered as a **suspected semantic defect** (BPO architect, 2026-11-03,
§6). Nothing is changed in the ontology yet: the architect asked for the referent to
be established, and the existing vocabulary checked, before any replacement class.
S2 is not to be frozen until this is decided.

## The class as it stands (slice 8)

```
bpo:ITServiceSolution ⊑ cco:ont00000117 (Information Processing Artifact)
  "An Information Processing Artifact that is an assembled, deployable
   information-technology offering (a configured system, application, or
   service package) made available by an IT function for use by its customers."
```

In the pinned CCO (2024-11-06), Information Processing Artifact is "A Material
Artifact that is designed to use algorithms to transform some Information Content
Entity into another Information Content Entity". The definition's three examples
name three kinds of entity:

- a **configured system**: material (devices with software installed on them);
- an **application**: software, an information content entity, which is not a
  material artifact because it is installed on one;
- a **service package**: an offering, which depending on its sense is a
  specification (directive information) or the provision of a service (a process).

It is the same defect `ITInfrastructureComponent` had (corrected in `df04151`), but
the fix there (hardware-only) is not open here: applications are part of what the
class is meant to cover.

## What the corpus does with it

It is used in 20 process definitions, always as a participant
(`has participant`, `obo:BFO_0000057`), never as an input or output. Grouped by what
the process does to it:

| Group | Processes | What the participant is in that process |
|---|---|---|
| Build and test | P20808 create and test, P20809 development lifecycle, P20813 integrate components and services, P20814 validate, P20844 consolidate change | the solution being built: software configured and installed in a build or test environment |
| Package | P20815 deployment packaging, P20823 fixed/enhanced packaging | the solution the package is for (the output is a deployment plan) |
| Deploy and roll out | P20679, P20697, P20848, P20851, P20853 software change/release, P20855 distribute software components network-wide, P20857 roll back, P20858 rollout, P20862 rollout plans | the deployed system, changed by installing software releases on it |
| Maintain and operate | P20817, P20818 maintenance, P20821 remediation, P20822 operate | the running system |

In all 20, the participant is something that is installed, changed, run, rolled back
or maintained: a configured system in which the software is concretized. None of the
20 needs the software itself, the information content that the same release would
also have on a disk or in a repository, as a participant. None needs a service in the
process sense either: where a process is the provision of the service (P20821, P20822,
both Acts of Service Provision), the solution is what the provision acts on.

## Existing vocabulary checked (D6, pinned CCO 2024-11-06)

| Candidate | Status |
|---|---|
| Software, Computer Program | **No such class** in the pinned CCO |
| `cco:ont00000653` Algorithm | Directive ICE: "prescribes some Process and contains a finite sequence of unambiguous instructions". The information-content side of an application; not what any of the 20 processes act on |
| `cco:ont00000117` Information Processing Artifact | Material Artifact "designed to use algorithms to transform" ICEs. Fits a single device, not an assembled system of devices and installed software |
| `cco:ont00000870` Infrastructure System | Material Entity (`BFO_0000040`) "composed of elements bearing Infrastructure Roles and is by itself sufficient to provide a planned service or benefit to some organization that maintains its elements" |
| `cco:ont00001141` Infrastructure Role | the role those elements bear (a Role, `BFO_0000023`) |
| `cco:ont00001301` Service Artifact Function | "An Artifact Function that is realized in a process of providing intangible goods to consumers" |
| BPO `ITInfrastructureComponent`, `ITAsset` | hardware only since `df04151` |
| BPO `ITServiceSolutionApproach` (965), `ITServiceSolutionRegister` (853), `ITServiceSolutionSunsetPlan` (965), `ITServiceCatalog`, `ITSolutionDesignSpecification` | the information *about* or *prescribing* the solution; already separate classes |

## Assessment against the architect's four readings

| Reading | Fits the 20 uses? |
|---|---|
| A specification of a proposed IT solution (Directive ICE) | No. Already covered by `ITSolutionDesignSpecification` and `ITServiceSolutionApproach`. Nothing is installed on or rolled back from a specification |
| A physical deployment of information-processing equipment (material) | Yes, for all 20, provided the software is counted as concretized in the equipment, not as a separate part |
| An IT service being provided (process) | No. The provision acts already exist (Act of Service Provision) and take the solution as participant |
| A heterogeneous solution to decompose | Only if some process needs the software as information content. None of the 20 does |

## Recommendation, for the architect's decision

**Re-anchor `bpo:ITServiceSolution` under CCO Infrastructure System
(`cco:ont00000870`)**, keeping the IRI and the 20 participant restrictions, with a
definition that keeps applications in the class as concretized, not as material
parts:

> An Infrastructure System, composed of information processing artifacts and the
> software concretized in them, that an IT function configures and makes available
> to provide an IT service to its customers.

- **Applications are kept, honestly.** In BFO, software, as information content, is
  concretized by a quality of the material bearer. The system bears the
  application's concretization; it does not have the software as a material part.
  So the definition is not narrowed by dropping "applications".
- **No new class, no new relation.** The class keeps its IRI, and the
  information-content side of an application stays where CCO already puts it (an
  Algorithm, a Directive ICE). The specification and register classes are untouched.
- **What it changes.** The class leaves Information Processing Artifact (117), and so
  Material Artifact (995). Infrastructure System (870) is directly a Material Entity.
  Through the participant restrictions the 20 processes keep a material participant.
  The inferred-hierarchy change will be measured when it is applied.
- **One caution.** Infrastructure System requires elements "bearing Infrastructure
  Roles". That is a commitment about the parts, which the corpus does not model. It
  would be stated by the definition, not axiomatized.

The alternative, if the architect reads "IT service/solution" as the APQC offering
in a broader sense, is to split the class: an Infrastructure System for the deployed
solution, with the offering left to the existing specification and register classes.
Only the first would be a participant of the 20 processes, so the split would not
change their axioms.

## Decision and application (BPO architect, 2026-11-03)

**Conditionally approved:** re-anchor under Infrastructure System (`870`), restricted to
material infrastructure systems, as an intentional semantic correction. The architect's
definition, applied:

> An Infrastructure System that consists of configured information-technology equipment
> and related material components organized to provide an IT service to an organization
> or its customers.

It covers physical systems that execute software, without asserting that the software
(information content) is a material component. It excludes software-only applications,
service specifications, and the service-provision processes. This narrows the
recommendation above, which kept applications in the class "as concretized".

**The 20 references, checked against the narrowed meaning.** The table above said all
20 fit the material reading. Checked one by one against each process's definition, APQC
source text and example, four do not:

| Process | Referent of the participant | Disposition |
|---|---|---|
| P20679 Define and implement IT service management | the service-management activities being put into operation, prescribed by the input `ITServiceManagementPlan`. No configured system participates in every instance | restriction **removed**; the plan (input) is the existing class |
| P20697 Determine and implement IT portfolio adjustments | IT investments, projects and activities, guided by the input `ITPortfolioAdjustmentDecision`. An adjustment can cancel or re-fund a project with no system participating | restriction **removed**; the decision (input) is the existing class |
| P20815 Bundle service/solution deployment packaging | the build being packaged (software; the example: "packages the build and writes the deployment runbook") and the output `DeploymentPlan`, which is *about* the deployed system | restriction **removed**; `DeploymentPlan` (output) is the existing class |
| P20823 Prepare fixed/enhanced service/solution packaging | as P20815, for a fixed or enhanced solution | restriction **removed**; `DeploymentPlan` (output) |
| the other 16 (build/test, validate, integrate, maintain, remediate, operate, consolidate change, deploy, release, distribute, roll back, roll out) | the configured system that is built and tested, changed, run or rolled back | **kept** |

Two of the 16 kept are judgment calls, recorded so they can be revisited:
- **P20814** validation: the APQC text says "the *proposed* IT service/solution", which
  could be a design. It is kept because the element follows integration (8.5.4.1.4) in
  the lifecycle, so what it validates is the integrated system.
- **P20844** consolidate IT change: the consolidation could be read as scheduling (an
  information act). It is kept because its definition and source text describe
  integrating the changes into the system, "to make more efficient use of resources and
  down time".

No class and no property was added. Where the participant was the only object of the
act, the act keeps its input or output plan. The software-only referent (the build in
P20815/P20823) is not given a class: no process needs it as a participant, and the
architect asked that such a class be justified independently.

**Not changed:** P20824 "Deploy services/solutions" has no `ITServiceSolution` participant
today. Adding one is not in scope here.

Inferred-hierarchy and validation effects: `semantic-impact-2026-11-03.md`.

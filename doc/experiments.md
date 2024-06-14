# Experiments

We designed a single and comprehensive experiment that simulates a
real-world usage of Fides. This document describes how we set up an environ-
ment that allows us to run experiments and simulate real-world situations
in the peer-to-peer network where the peers communicate and share threat
intelligence.
In the [Sampling Threat Intelligence](#sampling-threat-intelligence) section we describe how we sample threat intelligence shared by
the peers. In the following [Peer’s Behavioral Patterns section](#peer’s-behavioral-patterns),
we list different types of peers in
the network, what is their goal, and how they behave. [Environment Simulation section](#environment-simulation) then
describes how we designed the environment and what are the inputs for
the simulation itself. The last [Experiments Evaluation section](#experiments-evaluation)
presents how we evaluate each
scenario and explains the vital simulation indicators.


## Sampling Threat Intelligence
Threat intelligence, which is being shared on the peer-to-peer network
and is aggregated by Fides, is generated inside Slips by various modules.
Each module provides a score on its own and Slips aggregates these evalua-
tions into a single value. This means that threat intelligence is computed as
a sum of independent random variables and that tends to follow the normal
distribution. For that reason, we sample threat intelligence values from the
normal distribution.
As peers have different behavior, we will sample the threat intelligence
provided by them every time when they are asked for it. We will characterize
the peer’s behavior by the threat intelligence it provides, with respect to the
baseline, and the ground truth of the target being benign or malicious.
As described in the previous documents, threat intelligence consists of a
score and the confidence in that score. We use the notation μs for the mean
threat intelligence score and σs for the standard deviation of the score.
Similarly, we use μc for mean confidence and σc for the standard deviation
of the confidence.
Fides also in some cases employs a recommendation protocol, so in the
simulations, the peers might be asked to provide recommendations about
other peers. They will follow their behavioral strategy when providing the
data. Recall the recommendation description from the
[Recommendations section](https://github.com/stratosphereips/fides/blob/master/doc/design.md#recommendations). 
A single
recommendation response contains __cb(k,j)__ , __ib(k,j)__ , __sh(k,j)__ , __r(k,j)__ and __η(k,j)__ . We will be
sampling those from the normal distribution as well with the corresponding
pairs of (μcb, σcb ), (μib, σib ), (μsh, σsh ), (μr , σr ) and (μη , ση ). Every peer will
provide recommendations based on his behavioral strategy with respect to
the ground truth.



## Peer’s Behavioral Patterns
For the sake of experiments, we chose the behavior of each peer in the
simulated network. We identified multiple different behavioral patterns for
the benign as well as for the malicious peers. Every behavior is different and
is defined by the (μ, σ) for every data we sample and by the intent the peer
has in the network. Most of the behavior depends on the baseline, which is
the ground truth for any target in the system, if it is benign or malicious.
We note the baseline score as SB ∈ {−1, 1}, where SB = −1 means that the
target is malicious and SB = 1 means that the target is benign.

### Confident Correct Peer
This behavior corresponds to an honest peer that provides correct data
according to the baseline. Meaning, that if the target (domain/IP address
that we have threat intelligence for) is benign, the peer with confident correct
behavior will provide threat intelligence that says that the target is benign.
Moreover, the peer will provide the data with high confidence.
The very same thing applies to the situation when this peer is asked
to provide a recommendation for any other peer. The provided recommen-
dation will reflect the real behavior of said peer and it will indicate high
confidence in the recommendation. This peer has the ideal behavior as its
data are useful and correct. Table 5.1 describes the data used for sampling
the threat intelligence this peer provides.

![Screenshot_20240614_164959](https://github.com/stratosphereips/fides/assets/41242896/6fdefc69-3bb6-4380-8713-92906082f952)

### Uncertain Peer
This behavior simulates peers that do not have enough information to
provide reasonably good data, but they are benign and honest with their
behavior. The peer can provide essentially any score but with very low
confidence in said score. That is why the μup
 s is quite high whereas the
mean for this behavior is 0.
![Screenshot_20240614_165056](https://github.com/stratosphereips/fides/assets/41242896/943e6bb7-c892-4ad3-a826-8a99c839390b)


### Confident Incorrect
The peer with this behavior is confident about their data and the threat
intelligence, but their threat intelligence is wrong. However, this peer is
still benign and is making honest mistakes. This strategy simulates peers
that were not attacked by a malicious device and they consider it benign
because they do not have any information indicating malicious intent. Thus,
whenever the peer is asked to provide threat intelligence, it responds with a
score that is opposite of the baseline and with a high confidence value.
![Screenshot_20240614_165114](https://github.com/stratosphereips/fides/assets/41242896/2e41e7a5-cab4-43e0-b04b-a57067598c43)

### Malicious Peer
The malicious peer is going to provide wrong threat intelligence inten-
tionally to achieve their goal of influencing the trust decisions of the local
peer. The sampling data are the same as for the confident incorrect 
([Environment Simulation section](#environment-simulation)) behavior, 
but the difference is that the malicious peer is providing
misleading data intentionally. Moreover, intelligent malicious peer knows,
that it their incentive is to gain the service trust at the beginning in order
to more impact the decisions of the trust model in the later stages. We sim-
ulate this by introducing a grace period when the malicious peer does not
lie, but rather behaves like any other normal peer. This period then allows
the malicious peers to gain the initial trust. After that period, they start to
lie and thanks to the initial trust, they can influence the Fides’s decisions
with a larger impact.
As stated before, this behavior simulates knowledgeable adversaries that
are able to follow the Fides’s protocol and their goal is to influence decisions
of the local trust model. The adversaries can be either trying to bad-mouth
or provide unfair praises. In our case, it does not matter why they do
that, but rather the fact, that they do that intentionally and that they are
providing the opposite of the baseline score with the high confidence.
We decide to design an attacker, that is trying to hide in the data and
it is not providing score {−1, 1} with the confidence of 1 all the time, but
rather uses a distribution that is close to these values. The reason is that if
the model sees that there is a peer that provides {−1, 1} with high confidence
all the time, it would be very easy to detect and penalize this behavior.

![Screenshot_20240614_165156](https://github.com/stratosphereips/fides/assets/41242896/da658fd9-82ad-43e7-9f9f-a8d116825977)



## Environment Simulation
It is important in the simulations to also simulate time. This is because
the trust model depends on when peers join the network and when they
decided to lie or not. It is also because new peers are subject to recommen-
dation requests, but only when they are new.
Time in the simulations is measured in clicks. The local instance of
Fides performs a single action and receives responses from other peers in
the network in exactly one click. For example, this is the series of events
that happen in a single click. Fides asks the network for threat intelligence,
receives the responses, aggregates network opinion, and evaluates the inter-
actions with peers. Another series of events happening in a single click is the
actions of recommendation protocol: a new peer joins the network, Fides
asks for the recommendation for a new peer, collects the responses, computes the reputation, and evaluates the received recommendations. What is
the relation between real time and the clicks depends solely on the network
layer, mostly on the speed of messages convergence described in-depth in the [Global P2P Network for Confidential Sharing of
Threat Intelligence and Collaborative Defense](https://www.stratosphereips.org/thesis-projects-list/2022/3/12/global-permissionless-p2p-system-for-sharing-distributed-threat-intelligence) thesis

In order to simulate the environment, we have multiple parameters that
correspond to the expectations of how does the peer-to-peer network looks
like. We start with the number of peers in network that simulates the
size of the network and how many different peers can appear during the
whole simulation.
The network anatomy is another parameter for the simulation, where
we define what percentage of peers are using what strategy that was
described in the [Peer’s Behavioral Patterns section](#peer’s-behavioral-patterns). In other words, how many peers in the network
are adversarial and how many of them are benign.
Another parameter is the number of targets (IP addresses and DNS
domains) that will be used when Fides will be requesting the network threat
intelligence. For each target, we know the label (malicious and benign)
and we will be sampling threat intelligence that came from the local Slips
instance. The local threat intelligence will be sampled from the parameters
of one of the strategies described in [Peer’s Behavioral Patterns section](#peer’s-behavioral-patterns) - confident correct, uncertain,
or confident incorrect - which is yet another parameter that describes how
the local Slips instances behave.
For each remote peer, we select one of the behaviors from [Peer’s Behavioral Patterns section](#peer’s-behavioral-patterns)
and the number of peers for each behavior is determined by the con-
figuration of the simulation. We also determine if the peer is pre-trusted
or if it is a member of the pre-trusted organization. The percentage of
pre-trusted peers is again configurable. Next, we determine the time (in
clicks), when the peer is going to join the network. This allows us to eval-
uate the recommendation part of Fides, because if the peer joins late, Fides
requests recommendations from the other peers which can lead to further
problems if the recommending peers are adversarial.
If the strategy selected in the previous step is malicious (with its behavior
as described in [Peer’s Behavioral Patterns section](#peer’s-behavioral-patterns)), we determine for how many targets is the
peer going to lie about. This allows us to also simulate a highly advanced
attacker that lies only selectively for the targets that they control. It is not
rational for the attacker to lie about targets that are not known to them as
they do not gain any advantage from that. On the contrary, if they do not
lie, they gain more trust which they can use to further influence the local
decisions.
The last simulation parameter is how many clicks are left at the begin-
ning, for the pears to gain the initial trust. This means that in that initial


time period, malicious peers will behave like confident ones ([Peer’s Behavioral Patterns section](#peer’s-behavioral-patterns)),
in order to gain initial trust, and after that, they will switch to their own
malicious behavior ([Peer’s Behavioral Patterns section](#peer’s-behavioral-patterns)). This allows us to evaluate how fast is
the trust model able to determine that the peer, with the existing service
trust, is malicious.

## Experiments Evaluation
An important part of the experiments is how to evaluate what Fides
setup (interaction evaluations, threat intelligence aggregation) is better in
which scenario. We will be measuring two performance metrics that are
relevant for each situation.

### Target Detection Performance Metric
This first metric, tdp, measures performance of the target detection. We
compute tdp in Equation 5.1 as an average distance between the ground
truth for the target and the final detection made by Fides at the end of the
simulation. We use the following notation: τ is the set of targets in the
kmaxsimulation, GST is the ground truth score of the target, ST is then the
aggregated score ([Network Intelligence Aggregation section](https://github.com/stratosphereips/fides/blob/master/doc/design.md#network-intelligence-aggregation)) for the given target computed by Fides at the
end of the simulation.


![Screenshot_20240614_165344](https://github.com/stratosphereips/fides/assets/41242896/2e2617a3-c17b-4902-b568-e021c2357cc8)



This metric provides information on how good Fides was in computing the
score (malicious / benign) for some target. It holds that 0 ≤ tdp ≤ 2 where
0 is the best detection and 2 is the worst detection. Moreover, if tdp ≤ 1
the Fides was on average able identify all targets correctly.

### Peer’s Behavior Detection Performance Metric
The peer’s behavior detection performance metric pbdp measures how
close was the trust model’s service trust value for the remote peer to the
peer’s real behavior in the simulation. We measure it in the [Peer’s Behavioral Patterns section](#peer’s-behavioral-patterns), as an average
distance between computed service trust and the ground truth behavior of
the peer in the simulation.


![Screenshot_20240614_165323](https://github.com/stratosphereips/fides/assets/41242896/43263d11-c210-4bfd-833f-840b3c55a31b)

P is the set of remote peers in the simulation, stkmax is the service trust
i,jthat the local trust model (i ) had for the remote peer (j ) at the end of the
 ̄simulation. bj is then the ground truth behavior of the remote peer and we
compute it in the Equation 5.3.

![Screenshot_20240614_165406](https://github.com/stratosphereips/fides/assets/41242896/379ae1df-81fa-4c1c-92cc-04b52a44ae33)


Recall the description of the peers’ behaviors from the [Peer’s Behavioral Patterns section](#peer’s-behavioral-patterns), where
each peer’s behavior b had μbs that was used during threat intelligence sam-
pling. Because the sampled score is [−1, 1] and service trust [0, 1], we can not
use the μbs directly, but we need to scale it to the correct interval. Moreover,
as malicious and incorrect peers do have μbs on the opposite scale that the
ground truth is, we need to shift it before normalizing it. For that reason,
shif t = −1 for malicious and incorrect peers and shif t = 1 for confident
correct, and uncertain behaviors and thus the Equation 5.3.


### Environment Hardness
In order to be able to measure how hard it is for Fides to operate in some
environment, we designed the environment hardness variable eh. It holds
that 0 ≤ eh ≤ 10 and the higher the value is, the easier is for Fides to
operate in such environment as there are more confident correct peers that
provide correct threat intelligence and recommendations. On the contrary,
the lower the eh is, the harder it is for Fides to operate as there are more
byzantine peers.

![Screenshot_20240614_165428](https://github.com/stratosphereips/fides/assets/41242896/840766d4-bf66-4c8c-a1e4-ea84887725dc)

Where PCC is a set of peers in simulation that behave like a confident
correct ([Peer’s Behavioral Patterns section](#peer’s-behavioral-patterns)) peer and PU P that behave like an uncertain peer
([Peer’s Behavioral Patterns section](#peer’s-behavioral-patterns)).

## Simulation Execution
The simulations and experiments were designed to evaluate the trust
model in multiple ways and environments. In order to run arbitrary sce-
narios, we developed a framework, that allows us to simulate virtually any
environment with various combinations of Fides configuration.

Unfortunately, it is not possible to run and evaluate all possible scenar-
ios, as there are 14 different sets of parameters that can have many different
values. This leads to a combinatorial explosion and therefore we were un-
able to cover all possible existing scenarios. However, alongside the Fides
implementation, we published the simulation framework as well, so anybody
can simulate their preferred scenarios.
In the next document 6 we describe how we evaluated the experiments and
what we learned about the trust model behavior in various environments
with focus on the evaluation of Fides’s resilience.

---

Refer to the [Results document](https://github.com/stratosphereips/fides/blob/master/doc/results.md) for the results of the above experiments.


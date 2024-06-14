
# Results

This document presents and evaluates the results of the simulations that
were designed in the [Experiments Document](https://github.com/stratosphereips/fides/blob/master/doc/experiments.md). Since there are too many different
scenarios to evaluate each setup thoroughly, we mainly focus on evaluating
Fides under specific conditions that verify its resilience. These conditions
are the more important for the administrator, such as situations with many
byzantine peers.
The evaluation focus on finding a scenario where there are as many
adversarial peers as possible, and Fides is still able to guarantee that it can
come up with the correct target score. This is worst case scenario that every
trust model should be evaluated under, since there is no point in evaluating
a situation only with good and trusted peers.
However, since the reader may be interested in trying different scenarios,
we developed and published [a simulation framework](https://github.com/stratosphereips/
fides) where anyone can
verify and simulate any scenario they are interested in.
Note that all figures in this chapter can be replicated by re-running the
simulation Python code in [simulations/cases/figures](https://github.com/stratosphereips/fides/tree/master/simulations/cases/figures). The graphs
may differ slightly because the threat intelligence and recommendations are
sampled from a probability distribution as described in the
[Sampling Threat Intelligence section](https://github.com/stratosphereips/fides/blob/master/doc/experiments.md#sampling-threat-intelligence), but the
overall results should be the same.

## General Overview of a Single Simulation
To understand the results of our simulation we first need describe how
does the outcome of a simulation looks like, such as the example shown in
Figure 6.1. The simulation framework provides this graph for each possible
simulation.

![Screenshot_20240614_165722](https://github.com/stratosphereips/fides/assets/41242896/a99e194b-345c-4971-9627-440de9e0140a)

![Screenshot_20240614_170607](https://github.com/stratosphereips/fides/assets/41242896/2388cb1d-5471-47b5-9b23-111d1c2a99c2)

![Screenshot_20240614_170647](https://github.com/stratosphereips/fides/assets/41242896/4cd5e8eb-2023-49c6-bf4f-b6b09b7784ef)

Figure 6.1: An example outcome from a single simulation. The graph on
top shows how service trust changes as time goes by. In this example there
are four peers, two confident correct, one uncertain and one malicious. The
graph in the middle shows the score for the targets as computed by Fides
based on what the peers said. There are two targets (imagine google.com and
evil.com) and Fides computes the score for each of them: 1 means benign,
-1 means malicious. The lower graph shows the aggregated confidence for
the same targets. That means how confident is Fides about the score in the
middle graph.

The graph’s headline explains which setup parameters were used for the
trust model. In the case of Figure 6.1 Fides, For aggregating
threat intelligence, Fides used the aggregation described in 
[the Network Intelligence Aggregation section](https://github.com/stratosphereips/fides/blob/master/doc/design.md#network-intelligence-aggregation). The
local Slips instance behaved like a confident correct peer outlined in Sec-
tion 5.2.1.
The graph on top in Figure 6.1 shows the development of the service trust
st(i,j) ([the Service Trust section](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#service-trust)) on the vertical axis over time on the horizontal axis. As
mentioned in the [Environment Simulation section](https://github.com/stratosphereips/fides/blob/master/doc/experiments.md#environment-simulation), the time is measured in clicks. The higher the
service trust is for a peer, the higher impact it has on the final aggregated
threat intelligence. One can see multiple peers that were involved in the sim-
ulation and their respective behavior. All possible behaviors are described in
[the Peer’s Behavioral Patterns section](https://github.com/stratosphereips/fides/blob/master/doc/experiments.md#peer%E2%80%99s-behavioral-patterns). 
There were four different peers that were communicating with
the local instance of Fides, two of them were confident correct, one was an
uncertain peer and the last one was a malicious peer. On the first graph, we
can see that all peers were gaining the service trust at the beginning of the
simulation and then their trust stabilized during the time. The exception is
the malicious peer, its service trust was getting higher at the beginning of
the simulation, but then it took a hit and was lowered when the peer started
to lie.
The dotted line indicates the time when the malicious peers start lying.
As mentioned, one can see that during this first period, when the malicious
peers were not lying (before the line), they were gaining the service trust.
In the case of Figure 6.1 this happened at click 25 when the malicious peers
started lying. After that, it is clear that they started to lose the service
trust.
The second graph in Figure 6.1 shows the target score during the time
(clicks). The target score ST k ([the Network Intelligence Aggregation section](https://github.com/stratosphereips/fides/blob/master/doc/design.md#network-intelligence-aggregation)) is the part of the aggregated
network threat intelligence, that was computed from the scores and confi-
dences provided by each peer. The score was calculated by Fides at click
k for target T . The score graph contains two different targets, one that is
according to the ground truth malicious and a second one that was benign
(imagine google.com and evil.com) and Fides computes the score for each of
them: 1 means benign, −1 means malicious. We also included the moving
average value (indicated as MM) within the window of 10 clicks to make the
graph clear. In a perfect scenario, we would see two straight lines where for
benign target (google.com) would be the line in ST k = 1 and for the malicious
target (evil.com) in ST k = −1. However, in the imperfect world, we can see
that the lines fluctuate according to the score the Fides received from the
peers. In a case, when the lines cross, and the benign target ends up below

the red line (ST k ≤ 0) or the malicious target above the red line (ST k ≥ 0)
the Fides misclassified the targets and the attackers were successfully able
to influence the decision of the trust model.
Finally, the third graph, displays the aggregated confidence CT k (Sec-
tion 3.7) over time (clicks). The graph is similar to the score, we include
raw values for each time window and target, as well as the moving average
within the window of 10 clicks.
In this example output graph, it can be seen that Fides was clearly able
to identify that the malicious peer started to lie after click 25 because of
the service trust stki,j for this peer that fell down almost instantly. At the
same time, we can see that on the score graph, the ST k for both targets were
skewed and started to get closer to 0 because the malicious peer had already
gained service trust and thus the threat intelligence provided by it had an
impact on the final ST k . However, after Fides identified that the peer is lying,
it lowered the service trust for this peer, and the score started to recover
closer to the baseline.


## Evaluation of Fides Resilience
To evaluate the resilience of Fides in different scenarios, we need to find
the optimal configuration for the following parameters in Fides: interaction
evaluation strategy, threat intelligence aggregation function
([the Network Intelligence Aggregation section](https://github.com/stratosphereips/fides/blob/master/doc/design.md#network-intelligence-aggregation)), and initial reputation. Each combination of
parameters is evaluated in its capacity to correctly classify targets in any
network topology.

In this section, we are focusing on finding the best possible combination
of parameters for the worst possible scenario. In other words, we want to
identify a setup, where the Fides can guarantee that it is eventually going to
provide the correct data and will classify the targets correctly even though
the malicious actor controls most of the network.
We show two specific scenarios - one with no pre-trusted peers and one
where there are 25% of peers part of some pre-trusted organization. Because
even the scenario with only 25% peers shows, that in some cases is Fides able
to defend itself against the rest of the network, we do not show scenarios with
more pre-trusted peers, but we include them in the appendix (Figure A.6).



### Scenario With No Pre-Trusted Peers
In this scenario, there are no pre-trusted peers or organizations and Fides
needs to determine trust in each peer by itself. We simulated environments
starting with the 75% of confident correct peers (behavior from [the Peer’s Behavioral Patterns section](https://github.com/stratosphereips/fides/blob/master/doc/experiments.md#peer%E2%80%99s-behavioral-patterns).)
up to 75% malicious peers (behavior from [the Peer’s Behavioral Patterns section](https://github.com/stratosphereips/fides/blob/master/doc/experiments.md#peer%E2%80%99s-behavioral-patterns).) and used all possible
setups.


Target Detection Performance
The target detection performance tdp ([the Target Detection Performance Metric Section](https://github.com/stratosphereips/fides/blob/master/doc/experiments.md#target-detection-performance-metric)) is the most impor-
tant metric because it evaluates how good is Fides in the target classification
- if the Fides is able to correctly come up to a conclusion that evil.com is
the malicious target and google.com is benign.
Figure 6.4 visualizes the target detection performance on three different
graphs where each of the graphs is a single interaction evaluation strategy.
Each graph then displays dots with different colors. Each color a single
threat intelligence aggregation method in combination with different initial
reputation values. A single dot in the graph is the value of tdp and in a case
when the tdp ≥ 1, it means that Fides made on average the wrong decision
about the targets and classified them with the wrong label. In other words,
if tdp ≥ 1, Fides classified benign targets as malicious and the other way
around. We included the red line that shows tdp = 1 so if a dot is above the
red line, the Fides made an incorrect target classification. For that reason,
we optimize the dots to be below the red line (classifications being correct).
The horizontal axis in each graph measures the environment hardness
explained in [the Environment Hardness section](https://github.com/stratosphereips/fides/blob/master/doc/experiments.md#environment-hardness). It is important to note, that hardness essentially
expresses how many peers that can provide correct data are in the simula-
tion. For example, if the hardness is 10, 100% of peers inside the simulation
are providing correct data and behave like confident correct peers. Thus the
higher the value of hardness is, the easier it is for the Fides to do correct
classification.
Specifically, in Figure 6.2 we can see that in the easy environment,
most of the dots are below the red line until the hardness gets close to
3. The metrics perform more or less the same as they are able to stay
below the red line until eh = 3. In that situation, the best performance
and thus the lowest tdp has ThresholdTIEvaluation in combination with
W eightedAverageConfidenceTIAggregation and initial reputation of 0.95.
Because the previous performance of all methods is almost similar, we rec-
ommend using this combination up to eh3 to ensure the best performance
even in the harder situations.
Interestingly, the DistanceBasedTIEvaluation in combination with 0
initial reputation and AverageConfidenceTIAggregation for threat intelli-
gence aggregation, shows the same target classification performance in each
environment - tdp = 0. This suggests that the method was unable to de-
termine any trust for any of the peers. This is then later confirmed by
Figure 6.3.

![Screenshot_20240614_170725](https://github.com/stratosphereips/fides/assets/41242896/150acd4c-13d6-4d0c-a64d-412acdb2770e)
![Screenshot_20240614_170931](https://github.com/stratosphereips/fides/assets/41242896/2637cd16-85d2-45a8-bd06-fb6bb63f8fdb)
![Screenshot_20240614_170954](https://github.com/stratosphereips/fides/assets/41242896/21d95b15-fdb5-41ba-b235-f78c2278e524)

Figure 6.2: Target detection performance (vertical axis) for three different
interaction evaluation strategies in different environments (horizontal axis)
with no pre-trusted peers.


Peer’s Behavior Detection Performance
Figure 6.3 displays two important metrics which are related to how much
Fides trusts the peers in the network. The first is the peer’s behavior de-
tection performance metric pbdp ([the Peer’s Behavior Detection Performance Metric section](https://github.com/stratosphereips/fides/blob/master/doc/experiments.md#peers-behavior-detection-performance-metric)) and the second is the peer’s
average trust.
On the left side, one can see the peer’s behavior detection performance
metric that measures how good was Fides in estimating the peer’s behavior.
The lower value of pbdp the better because the Fides’s service trust for the
peer was closer to the real value used in the simulation.
On the right side, we show the peer’s average trust metric. That is an
average trust of Fides for each peer. We include this metric in order to see
how much trust was Fides able to obtain for the peers in the network. It is
important to note, that there is no correct or desired value of this metric,
because for example in the environment where there are all peers confident
correct, the peer’s average trust should be high, but in the environment with
all byzantine peers, this metric should be low because Fides should not trust
incorrect and malicious peers.
As suggested in the previous section while measuring target detection
performance, the right graph for DistanceBasedTIEvaluation in combi-
nation with AverageConfidenceTIAggregation shows, that this setup is
unable to determine trust for the peers and has average peer’s trust close
to 0. This means that the trust model will almost always aggregate threat
intelligence to score 0 with confidence 0 making it, in a fact, useless.


![Screenshot_20240614_171043](https://github.com/stratosphereips/fides/assets/41242896/0f55f608-06a9-435e-b6d8-ad28c360f3ae)

![Screenshot_20240614_171122](https://github.com/stratosphereips/fides/assets/41242896/db394aee-875e-4b10-aae1-647ff14a8bdd)

Figure 6.3: The behavior of peer’s trust metrics in the different environments
for different Fides’s setups with no pre-trusted peers. On the left side
peer’s behavior detection performance, and on the right side peer’s average
trust.


### Scenario With 25% of Pre-Trusted Peers
In this scenario, Fides assumes that there are 25% of pre-trusted peers.
We simulated environments starting with the 75% of confident correct peers (be-
havior from [the Peer’s Behavioral Patterns section](https://github.com/stratosphereips/fides/blob/master/doc/experiments.md#peer%E2%80%99s-behavioral-patterns)) up to 75% malicious peers (behavior from Sec-
tion 5.2.4) and used all possible setups.
Target Detection Performance
Specifically in Figure 6.4 one can see that until the environment hard-
ness eh ≥ 3, all strategies help Fides to classify the targets correctly. In
general, the DistanceBasedTIEvaluation performs the best in almost all
situations except the easiest one, where the MaxConfidenceTIEvaluation
has slightly better results.
The situation changes after the environment hardness goes over 2.5 (eh ≤
2.5) when the ThresholdTIEvaluation and MaxConfidenceTIEvaluation
misclassify the targets. In that case, all threat intelligence aggregation meth-
ods are the same and all of them misclassify the targets no matter what ini-
tial reputation is used. However, the DistanceBasedTIEvaluation strategy
in combination with AverageConfidenceTIAggregation method is able to
still classify the targets correctly and maintain the tdp ≤ 1 even under the
toughest conditions where there are 75% of adversarial peers in the simula-
tion. We include a more detailed visualization of this case in the appendix
in Figure A.1.
When Fides is used in a similar situation with the threat intelligence
aggregation method W eightedAverageConfidenceTIAggregation, it mis-
classified the targets in one simulation when working in the hardest envi-
ronment. Thus, this method does not provide a guarantee that Fides will
end up with correct classifications for every target.
To summarize, the results have shown that with 25% of pre-trusted peers
is Fides able to classify all the targets properly all the time if the interaction
evaluation strategy DistanceBasedTIEvaluation is used in combination
with the AverageConfidenceTIAggregation. In such case, Fides provides
a guarantee that no matter what the adversaries do, it calculates the correct
threat intelligence.

![Screenshot_20240614_171209](https://github.com/stratosphereips/fides/assets/41242896/cb42f6ec-938f-4273-9fcf-7f68fbcf1307)
![Screenshot_20240614_171258](https://github.com/stratosphereips/fides/assets/41242896/c17697fa-7183-4bb9-87fd-86376b4fff00)

![Screenshot_20240614_171308](https://github.com/stratosphereips/fides/assets/41242896/5df437bc-d40f-4384-878d-786a0adde507)


Figure 6.4: Target detection performance (vertical axis) for three different
interaction evaluation strategies in different environments (horizontal axis)
with 25% pre-trusted peers.


Peer’s Behavior Detection Performance
Figure 6.5 shows the peer’s behavior detection performance pbdp on the
left side and the peer’s average trust on the right side. When we com-
pare Figure 6.3 (no pre-trusted peers) with this Figure 6.5 (25% pre-trusted
peers), we can clearly see that, especially the pbdp metric improved and in
all environments it holds that pbdp ≤ 0.4. This means that Fides’s ability to
identify the true behavior of the peers greatly improved for all interaction
evaluation strategies.
The biggest improvement was in strategy DistanceBasedTIEvaluation
which had poor performance with no pre-trusted peers in Figure 6.3. How-
ever, in the situation with 25% pre-trusted peers it is now able to detect the
true behavior of the peers with the similar precision as the other strategies.
![Screenshot_20240614_171354](https://github.com/stratosphereips/fides/assets/41242896/acc8dce4-cabb-4d35-ae97-832808489ade)

![Screenshot_20240614_171408](https://github.com/stratosphereips/fides/assets/41242896/6c7bc29b-2ca5-40ec-9cab-9277a775403f)

Figure 6.5: The behavior of peer’s trust metrics in the different environments
for different Fides’s setups with 25% pre-trusted peers. On the left side
peer’s behavior detection performance, and on the right side peer’s average
trust.

## Considerations when Evaluating Trust Results
Even though the results from the previous the [[Evaluation of Fides Resilience section](#evaluation-of-fides-resilience)](#evaluation-of-fides-resilience) suggest that a
combination of DistanceBasedTIEvaluation for evaluating the interactions
in combination with AverageConfidenceTIAggregation is the best, there
are corner cases where this is not always true.
For example, recall Figure 6.1 from the
[the General Overview of a Single Simulation section](#general-overview-of-a-single-simulation'), where the presented
situation uses MaxConfidenceTIEvaluation and it is able to correctly de-
tect all types of peers as well as correctly determine the score for the target.
However, if we take the same environment and the only difference is using
DistanceBasedTIEvaluation for evaluating interactions, we get the follow-
ing graph for the service trust in Figure 6.6. The graph for confidence as well
as target score for the situation from Figure 6.6 can be seen in the appendix
in the Figure A.3. This is also the same behavior that we described when
we were describing Figure 6.3 in the previous the [Evaluation of Fides Resilience section](#evaluation-of-fides-resilience).

![Screenshot_20240614_171517](https://github.com/stratosphereips/fides/assets/41242896/fdc6093d-fdc5-4aa2-8510-854ecd0de52a)

Figure 6.6: DistanceBasedTIEvaluation in the situation from the fig-
ure 6.1
The service trust graph in Figure 6.6 suggests that Fides didn’t gain
any trust for any peer in the network. This happens because the evaluation
strategy didn’t have enough information at the beginning to evaluate the
received data properly. That leads to peers never gaining any trust and
thus not producing any valid outputs because, with no trust, the target
score and confidence ended up being 0 as well.
Another thing to consider is that during the simulations from the pre-
vious the [Evaluation of Fides Resilience section](#evaluation-of-fides-resilience), the local Slips did not know anything about the targets.
Which means that whenever Fides requested threat intelligence from Fides,



it responded as uncertain peer ([the Peer’s Behavioral Patterns section](https://github.com/stratosphereips/fides/blob/master/doc/experiments.md#peer%E2%80%99s-behavioral-patterns)). This simulates situations that
are close to the reality when Slips is asking about the targets it does not know
anything about. However, it also means that MaxConfidenceTIEvaluation
strategy will not live to its full potential as it is also using information from
the local Slips.

## Discussion
We discovered that actually there exists a particular setup that guar-
antees that Fides is able to eventually classify the targets correctly in a
very adversarial situation. When Fides communicates with at least 25% of
pre-trusted peers from pre-trusted organizations (0.25 · |P | are pre-trusted)
and uses DistanceBasedTIEvaluation for evaluating the
interactions in combination with AverageConfidenceTIAggregation 
(the [AverageConfidenceTIAggregation section](https://github.com/stratosphereips/fides/blob/master/doc/design.md#averageconfidencetiaggregation)) for aggregating the threat intelligence; then Fides is able to cor-
rectly classify the targets no matter how many adversarial peers are in the
network (up to filling the remaining 75%) or how hard they lie.
We included the graph of this case, similar to the Figure 6.1, with this
particular ”winning” setup in the most hostile environment to the Appendix
in Figure A.1. For the explanation of the graph see
[the General Overview of a Single Simulation section](#general-overview-of-a-single-simulation').

![Screenshot_20240614_171539](https://github.com/stratosphereips/fides/assets/41242896/0a32cbe5-bd9c-4314-a208-ab3308ed46e5)

Figure 6.7: Score in figure A.2.

Interestingly, in this particular case, the initial reputation does not affect
the final outcome of the simulation, but it does affect the progress as when
using an initial reputation higher than 0, Fides provides wrong scores in
the situation when the malicious peers started to lie. However, in time it
discovers that the peers are lying, which decreases their service trust and is
able to eventually recover the correct labels for the targets. The score value


over time for this situation can be seen in Figure 6.7. We included the whole
graph in the Appendix in Figure A.2.
With no pre-trusted peers in the network, the results of each configu-
ration vary and they highly depend on the network topology as well as on
the knowledge of the local Slips instance. The results for the no pre-trusted
scenario are shown in Appendix Figure A.4.
In the scenario of 50% pre-trusted peers, no matter the configuration,
Fides was eventually able to determine the correct target classification with
a high precision of tdp ≤ 0.7. Moreover, Fides was able to correctly identify
the peer’s behavior with the precision of pbdp ≤ 0.2. This is a very favorable
situation for the administrator, where you trust the peers so much that it is
not possible for the adversarial peers to modify the belief. The results for
this scenario are shown in Appendix Figure A.6.
In general, for a case with no pre-trusted peers and organizations, one
should use ThresholdTIEvaluation because it proved to be slightly better
than the others. However, in cases when the local Slips instance has some
local knowledge about the targets the MaxConfidenceTIEvaluation might
be a better choice.
For cases where the Fides communicates with some pre-trusted peers,
one should use the DistanceBasedTIEvaluation threat intelligence eval-
uation strategy in combination with AverageConfidenceTIAggregation.
This combination is even able to guarantee that with at least 25% of pre-
trusted peers, it is able to eventually determine correct threat intelligence
for all the targets.

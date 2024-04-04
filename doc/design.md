# Trust Model Design

Fides aims to design and implement a trust model for sharing threat
intelligence in global peer-to-peer networks where the peers are instances of
intrusion prevention systems.

In this document, we propose a new trust model Fides. Fides was named
after the ancient goddess of trust and good faith Fides.

The trust model utilizes modified SORT’s computational model with multiple modifications
and extensions that allows it to work in highly adversarial global peer-to-
peer networks effectively. Fides is a generic and heavily configurable trust
model specializing in sharing threat intelligence. Thanks to its modular
architecture, it can operate with any data and it is not limited only to threat
intelligence. In the [General Overview of Fides Section](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#general-overview-of-fides) we describe our trust model design and explain
how Fides works on a high level, the inputs and outputs, and how it behaves
in which situation. 

After outlining the general overview, we analyze the weaknesses of the trust models and how they apply to Fides. 
First, we start with the cold start problem in the [Static Initial Trust Section](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#static-initial-trust), 
which describes how peers
can gain trust when they are new in the network and how Fides tackles this
issue. Then, In the [Attack Vectors Section](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#attack-vectors) 
we analyze possible attack vectors on our trust
model.
Once all trust model requirements are explained, we dive deep into Fides’s
computational model in the [Computational Model of Fides Section](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#computational-model-of-fides) 
and explain how it can uncover
trust relationships in the network. 

Because Fides specializes in sharing threat intelligence and integrates with
[Slips IPS](https://github.com/stratosphereips/StratosphereLinuxIPS), 
in the [Network Intelligence Aggregation Section](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#network-intelligence-aggregation) 
we explain how Fides aggregates the weighted threat intelligence from the network.

We use the following terminology to talk about the
trust model:

* Target: An identification of a resource for which is Slips able to generate
threat intelligence. It can be, for example, either an IP address,
a domain, or hashes.

* Local Peer: The unique local instance of Slips that is connected to
the global P2P network and runs Fides. In equations, we use i when
referring to the local peer.

* Remote Peer. A peer on the Internet is connected to the global Slips
P2P network. In equations, we use j when referring to the remote peer.

* Service Trust: How much does Fides trust a remote peer that it
provides the local peer with good service. In other words, to what
extent does Fides trust a specific peer that it provides correct and
valuable threat intelligence. We denote it st and discuss it in detail in [the Service Trust section](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#service-trust)




## General Overview of Fides

In this section we describe how Fides work from a high level perspective.

![image](https://github.com/stratosphereips/fides/assets/41242896/aa45301d-e674-4ec9-934a-943dd4312c9f)

Fides operates in four general phases, which are visualized in Figure 3.1.
In the first phase, a local Fides instance receives threat intelligence data
from the remote peers in the network. 


In the second phase, Fides aggregates the threat intelligence data using
the trust data it has for each remote peer. In general, data from highly
trusted peers have a higher impact on the final aggregated threat intelligence
than the data from peers with low trust. How does Fides does that is described
in the  [Network Intelligence Aggregation Section](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#network-intelligence-aggregation)
The aggregated threat intelligence is also sent to Slips IPS
as an output of the trust model.


In the third phase, Fides evaluates the interactions with each peer. Fides
computes how much it was satisfied with the threat intelligence it received
from each remote peer. The evaluation does not depend on the content of
the threat intelligence and therefore is a generic method. This satisfaction
metric has then a direct influence on the trust relationship between the
local and remote peers because it is used in the next step to compute trust
data. 

In the fourth step, Fides updates the trust data for each peer according
to the satisfaction that is computed in step number three. 

Computations
that allow Fides to do that are described in detail in the [Computational Model of Fides Section](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#computational-model-of-fides)

All operations, including the data flow and the communication with
other peers and Slips, can be found on the operational diagram shown in
Figure 3.2 below.

![image](https://github.com/stratosphereips/fides/assets/41242896/1a66486f-07d9-4119-bdb3-4f3531e31ce0)


## Cold Start Problem

A dynamic and global environment such as a global peer-to-peer network
is open to anyone since any peer can freely join and leave. Because of
that, the local peer will encounter many other peers that were not seen
before. Therefore, the trust model does not have any information about
their reliability or how much it can trust them. New benign peers need to
be somehow trusted by the local peer in order to be a useful part of the
network. However, the local peer also needs to be able to discover new
malicious peers that are trying to gain its trust.
The problem of how to know something about a new entity in order to
quickly work better is called the _Cold Start Problem_. For Fides, it means
how to compute a good initial trust for new unknown peers.
We selected several solutions to this issue, which are all implemented in
Fides. Fides also combines them according to a provided configuration with
the aim to achieve the best result for the cold start problem with adversarial
peers.

### Static Initial Trust

In this approach, whenever the trust model encounters a new peer, it
assigns a static value as an initial trust. The value is assigned by pre-
choosing some third-party trust models in the configuration.

For example, in the [Dovecot trust model](https://dspace.cvut.cz/bitstream/handle/10467/90252/F3-DP-2020-Hollmannova-Dita-final.pdf), 
every peer starts with trust 1 (highest possible), 
and various interactions can lower the trust in the peer to 0.
In other words, the trust model considers new peers honest from
the beginning, and only during this time their reputation can be lowered
when they perform incorrect interactions or are discovered as a malicious
peer.
On the other hand, the Sality botnet uses a value called goodcount as
a counter of good interactions with any other peer, the higher the goodcount,
the greater trust the local peer has on the remote peer. The goodcount for
each new peer starts with 0 in Sality. Meaning, that the botnet does not
trust fresh peers at all and they can gain trust only by following the Sality
protocol.
The model of static initial trust is easy to implement, but it requires
assumptions about the network. If the network is considered mostly benign,
it might be safe to use an initial trust of 1, however, for highly adversarial
networks using an initial trust of 1 might be dangerous and it is better to
use 0. Using low initial trust and no mechanism to gain more trust fast

means that the benign peers that joined recently do not affect the final
decisions of the model, even though they might have useful information
about adversaries.
Static initial trust is supported by Fides as a form of fallback when no

other cold start technique is used. The administrator provides a configuration
that contains the initial reputation for each new peer.

### Pre-Trusted Peers


Fedis is done as a part of a master thesis which was done simultaneously to the master 
thesis on global P2P security TI sharing by Bc. Martin Repa, called [Iris](https://www.stratosphereips.org/thesis-projects-list/%202022/3/12/global-%20permissionless-%20p2p-%20system-%20for-%20sharing-%20distributed-threat-intelligence), 
which implements the new idea of pre-trusted peers in organizations for the Slips IPS. 

Therefore, Fides works with the concept of pre-trusted organizations which
have pre-trusted peers. Iris implements the concept of pre-trusted organizations, 
and Fides uses this knowledge to assign a higher or lower trust to new peers.


The global P2P framework implemented by Repa supports these type of
peers and provides a cryptographically-secure way how to identify a single
peer in the network, and its membership in an organization. This allows
Fides to pre-trust specific peers or all the peers from organizations by assigning
them an initial value.

Fides can be configured to use pre-trust in two different ways. First, to
assign the pre-trusted peers an initial reputation. This means that the peer
will have an initial reputation, but it will be required to interact with the
local peer and it will slowly change that initial reputation according to its
interactions with others. All the interactions will be evaluated and Fides
will compute a service trust for the peer.

Second, Fides can use the initial pre-trusted value read from the configuration
as the final service trust. This effectively means that Fides will not
evaluate any data received from the pre-trusted peer and this service trust
will be kept forever.

This configuration for Fides is called enforceTrust. If it is enabled and
thus ```enforceTrust = False``` is set in the configuration, Fides uses the first
variant where the trust for the peer will move during the interactions. If the
administrator uses ```enforceTrust = True```, Fides uses the second option and
fixates the service trust for the peer to a set pre-trust.


Both options help solve the cold start problem for specific peers and
organizations, as they will start with a high reputation or fixed service trust.
Which organization or peer to trust is completely left to the administrator
of Slips. However, as the administrator needs to know the identity of the
peers or organization, it does not solve the cold start problem globally for
all peers.

### Recommendations

As the local peer might have multiple remote peers that it trusts enough,
Fides uses these relationships to ask the remote peers about how much they
trust a new peer. Fides only asks for recommendations once: when the local
peer finds a new peer for the first time.
Using a recommendation system introduces new attack vectors that can
be exploited by adversaries, either by getting trust for the malicious peer or
by lowering trust in honest peers that might have some threat intelligence
about the malicious actor. These attacks are called bad-mouthing and unfair
praises and we need to consider them and implement countermeasures.
Because of the possible attacks, the local peer should not solely rely on
the network recommendations when computing the final service trust for the
fresh peer. In case when the recommending peers are malicious, it might
skew the decisions of the local peer for the time being. In order to solve
this, when computing the final service trust for the remote peer, the local
peer should take into account its own interaction with the peer as well as
the received recommendations.
Moreover, the local peer should request recommendations only if it has
enough trusted remote peers, otherwise, it can expose itself to bad-mouthing
and unfair praises attacks more easily.
Fides employs recommendation systems based on [SORT](https://ieeexplore.ieee.org/document/6280552) 
but with more strict rules when it is actually used and combines it with the
[pretrusted peers](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#pre-trusted-peers)  
as well as with the [static initial trust ](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#static-initial-trust) 
as a fallback when no other option is available due to constraints such as having not
enough trusted peers. The algorithm used for the recommendation system
is explained in detail in [Computational Model of Fides Section](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#computational-model-of-fides)


## Attack Vectors

Since Fides is a trust model that computes how much to trust peers, it
is potentially open to attacks from adversarial peers. Adversarial peers are
peers that know how to talk the protocol and manipulate the recommendations,
or threat intelligence data in order to influence the final decisions.

Adversarial peers can try to:
* Send bad threat intelligence data
* Lie about a peer that is benign
* Lie about a peer that is malicious


## Computational Model of Fides

This section describes how Fides determines to whom and how much it
can trust other remote peers. Our trust model expresses trust in a specif
peer with metrics called service trust. Service trust is a value that describes
how much the local peer can trust a specific remote peer.
Here, we describe the process top-down starting with
the most important parts - service trust - and then breaking it down into
bits. Note that there are two main ideas behind most of the equations.


The first one, is that we want to robustly capture the average behavior
of the peers. In order to do that, we will be computing the average behavior
of the peers and then approximating the deviations from said behavior.


The second part compares and weights first-hand experience with the
remote experience.
First-hand experience is what happened between local and remote peers during 
the time they interacted. This can be, for example, threat intelligence sharing, 
file-sharing, or the results of the recommendation
protocol. Remote experience is what happened between one remote peer and
another remote peer. In other words, first-hand experience for peer j are
actions between j and z. Whenever j shares information about these actions
with peer i, for i it is a remote experience.

Table 3.1 below describes the most important notation we use in the following
sections.

![Screenshot_20240404_231640](https://github.com/stratosphereips/fides/assets/41242896/d816cf32-49f7-4a93-ad59-4c596594f8a9)



### Service Trust

As outlined previously, service trust is a value that describes how
much peer i trusts that remote peer j will provide a good service.

We compute the _st(i,j)_ in the Equation 3.1 by weighing local experience with
peer's j service, with the reputation j got from the network when it was
first seen by i. The used weight is the size of the service interaction history
shi,j to global maximal history size _sh(max)_.

Equation 3.1 implies that the more interaction there was between peers
i and j, the bigger impact on _st(i,j)_ it has. In other words, the more i and j
interact the less i relies on the reputation that i computed from the values
provided by the network, at the time when j was seen for the first time by
the peer i.

![Screenshot_20240404_011815](https://github.com/stratosphereips/fides/assets/41242896/68bfcc53-ae16-40dd-9905-0a71b28e0237)


### Local Experience for Service Trust

The first part of the Equation 3.1 contains competence belief _cb(i,j)_ , and
integrity belief _ib(i,j)_ . Both values are based solely on the history of the
interactions that the peer i experienced with the peer j.

**Competence Belief**

Competence belief represents how much did peer j satisfied local peer i
with the past interactions. We measure it as an average of interactions from
the past.

![Screenshot_20240404_011933](https://github.com/stratosphereips/fides/assets/41242896/01272308-b4e9-4ed3-a7a7-eb5a5bb51c9e)

**Integrity Belief**

Integrity belief _ib(i,j)_ is a level of confidence in the predictability of future
interactions. It is measured as a deviation from the average behavior _cb(i,j)_ .
Therefore, _ib(i,j)_ is calculated as an approximation to the standard deviation
of interaction parameters.

![Screenshot_20240404_012019](https://github.com/stratosphereips/fides/assets/41242896/034e2eb6-1e92-41f0-94b7-7b885fe17144)

It holds that 0 ≤ _ib(i,j)_ ≤ 1. The more consistent behavior peer j has, the
lower the _ib(i,j)_ is. Consistency is a highly desired property as the local peer
then has more precise estimates about the future behavior of the remote
peer.

### Interaction Satisfaction
_s**k(i,j)_ is _i_’s satisfaction value with interaction with peer j in window k.
(see the table [here](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#computational-model-of-fides))


We outlined before, that each interaction between two peers is evaluated,
_s**k(i,j)_ is a result of this evaluation of a single interaction between peers i
and j. Because our trust model is generic, the evaluation function can
be implemented differently for different data.
However, even with the computed interaction satisfaction value, not all
interactions are the same. Some interactions are more important than others.
Moreover, because peers can change their behavior, most recent interactions
should be more important than the interactions that happened a long time ago.
That is why we include the weight of the interaction and the fading effect.

**Weight of the Interaction**

Because each interaction is different and its importance is different, we
have _w**k(i,j)_ that measures the importance. The weight belongs to interval
0 ≤  _w**k(i,j)_ ≤ 1 and Fides implements it as a discrete function of interaction
type. For example, the weight of interaction when a remote peer shares
the threat intelligence is higher than when the remote peer requests threat
intelligence.

**Fading Effect**

Fading effect _f**k(i,j)_ determines "how much does the algorithm forget" as the
algorithm prefers most recent interactions over past interactions and thus
_f**k(i,j)_ reduces the weight of the past interactions. _f**k(i,j)_ is a non-increasing
function of interaction and time or an index of said interaction in history.
The actual implementation of the fading effect depends on the data the
trust model is processing. For example, SORT implements it as a decreasing
linear function 

![Screenshot_20240404_012153](https://github.com/stratosphereips/fides/assets/41242896/afe31108-d95a-4103-b647-5291d979e578)

However, in our case and after
multiple iterations, we decided not to forget the interactions that the model
remembers and rather have all interactions with the same impact.

![Screenshot_20240404_012153](https://github.com/stratosphereips/fides/assets/41242896/64718ca7-02a9-4d9e-9c29-f84b1a694062)


The way Fides computes  _f**k(i,j)_ might be changed in the future and implemented as a
function of time, we discuss this in more detail as a part of the future work.

### Reputation and Recommendations

In order to mitigate the cold start problem outlined in the [Cold Start Problem Section](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#cold-start-problem)
and in the cases when there are no or few interactions between i and j, the
algorithm relies on _r(i,j)_ - reputation value. _r(i,j)_  is the second part of the
service trust Equation 3.1 that introduces remote experience to the service
trust.
The reputation value is computed from the recommendations received
from the remote peers. This value represents what remote peers think about
another remote peer. However, this value is calculated by the local peer with
respect, to how much it trusts each peer, that provided the recommendation.
When the local peer i encounters remote peer j for the first time and it does
not have any data about its trustworthiness, i can request recommendations
on peer j from i’s most trusted peers. We denote a set of remote peers, that
provided the recommendations as Ti

**Requesting a Recommendation**

The recommendation system built into Fides cannot be used in every
scenario. Because of the sensitive nature of the environment, the trust
model was designed for, there are cases when it is dangerous to ask for
recommendations. This is mainly the case when there are not enough peers
that are trusted enough.
SORT requests recommendations every time it encounters a new peer.
The set of recommending peers is created by taking all known peers and
selecting those that have higher than average service trust. However, those
can also be peers with trust as low as 0.001. In a sensitive environment,
which the peer-to-peer network of IPS definitely is, we do not want to get
recommendations from peers, that have low trust at all. Moreover, given
the nature of Slips, we decided to combine a recommendation system based
on SORT with [ Static Initial Trust](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#static-initial-trust)
and with [Pre-trusted peers](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#pre-trusted-peers).
This approach provides a more robust basis for a trust-sensitive environment
and it helps us to mitigate the [Cold Start Problem](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#cold-start-problem)
If the peer is part of a pre-trusted organization or it is pre-trusted itself,
it inherits the configured reputation _r(i,j)_  from the configuration. In this
case, Fides does not engage the recommendation protocol at all, because
the peer already has reputation _r(i,j)_  assigned from the configuration and it
was recommended by the administrator. Moreover, the administrator can
choose if this value is frozen, or not. Frozen Service Trust configuration
means, that the peer j has in eyes of i static service trust _st(i,j)_  it will never
change and whatever data peer j sends to i will not influence the _st(i,j)_ . On
the other hand, when this configuration is not selected, the peer’s service
trust is going to change during the time when it communicates with the
local instance according to the data and interactions it provides.
In the case where the peer is not pre-trusted, Fides evaluates if it has

enough well-trusted peers that can be trusted to provide the correct 
recommendation. This value as well as a number of maximal peers used for

recommendation is configurable. In addition, the administrator can enforce
that for the recommendation protocol, only the pre-trusted peers or the
peers from pre-trusted organizations are used.


**Recommendation Response**

A single recommendation response from peer z ∈ Ti about giving the
recommendation to peer i about peer j contains the following data.

* _cb(z,j)_ , _ib(z,j)_ - summary of z’s interactions with j, competence belief and
integrity belief

* _sh(z,j)_ - service history size, number of interactions between z and j -
the more interactions they had, then the z’s recommendation has more
credibility

* _r(z,j)_ - summary of recommendations that z received on j
* _η(z,j)_ - number of peers that provided recommendations for j when j
was new to z and their recommendation was used to compute _r(z,j)_


_cb(z,j)_ , _ib(z,j)_ are included in the recommendation in order to provide a view
on what does z think about j. _sh(z,j)_ and _η(z,j)_ are included to indicate how
much experience with j does z actually have. To determine to which extent
is the z sure about correctness of _cb(z,j)_ , _ib(z,j)_ , _r(z,j)_ in the recommendation.
And also to protect the z’s recommendation trust in i’s eyes, if _cb(z,j)_ , _ib(z,j)_ ,
_r(z,j)_ values are wrong, because i inspects _sh(z,j)_ and _η(z,j)_ and does not penalize
z that much, if the history size or the number of original recommender are
low.


**Computing Reputation**

When the local peer receives all recommendations, it computes the rep-
utation value _r(i,j)_  as a weighed expected local experience (_ecb(i,j)_ , _eib(i,j)_ -

estimates about competence and integrity) from the remote peers with their
remote experience (_er(i,j)_  - estimate about reputation of said peer).


![Screenshot_20240404_012511](https://github.com/stratosphereips/fides/assets/41242896/e90d9603-b86b-41b7-b6f8-78b059dd75da)




The weight, used in the Equation 3.5, is the average of history sizes in all 
recommendations to _sh(max)_, maximum interactions history size. We calculate
μsh as follows.

![Screenshot_20240404_012531](https://github.com/stratosphereips/fides/assets/41242896/75be9342-728c-429b-a468-d5255b1c677b)


Again, we are weighing local experience to remote experience. However, in
this case, it is local for the remote peers that provided the recommendations.


### Remote Local Experience

Similarly, when we compute the service trust in Equation 3.1, we need
to get competence and integrity belief. However, while creating reputation
value in 3.5 where the values are coming from the remote peers, we are trying
to estimate those values received from the network. For that reason, we call

them estimated competence belief - _ecb(i,j)_ and estimated integrity belief -
_eib(i,j)_ .

**Estimated Competence Belief**
_ecb(i,j)_ is estimation about competence belief made by i about j. This
value is computed from the received recommendations in combination with
_rt(i,z)_ - a recommendation trust that i has about z. Similarly, as for service
trust, we have a normalization coefficient βecb that moves the resulting data
to the correct interval. It holds that 0 ≤ _ecb(i,j)_ ≤ 1.

![Screenshot_20240404_012635](https://github.com/stratosphereips/fides/assets/41242896/66c5f93d-8e11-4ad8-b349-ea80fe5ec47c)


Recommendation trust is described in detail in the following sections.

**Estimated Integrity Belief**

Following the _ecb(i,j)_ , _eib(i,j)_ is estimation about the integrity belief made
by i about j. Equation 3.8 is almost similar, but we use _ib(z,j)_ instead of _eb(z,j)_ .
This means that normalization coefficient βeib = βecb.

![Screenshot_20240404_012741](https://github.com/stratosphereips/fides/assets/41242896/3dc70de0-0010-4e4c-a0f3-52a35f89a258)

### Remote Remote Experience

Going back to Equation 3.5 from the [Reputation and Recommendations Section](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#reputation-and-recommendations),
we use estimated reputation value _er(i,j)_ . This value represents information that was created

by the peers that are remote even for remote peer j. In other words, this
information came from the second ring of trust - from acquaintances of an
acquaintance.

![Screenshot_20240404_012914](https://github.com/stratosphereips/fides/assets/41242896/13c29d1b-015e-43b1-b78b-041be600e904)


### Recommendation Trust Metric

Recommendation trust - _rt(i,z)_ - is another metric that a peer calculates
and stores. It expresses how much does i trust that z provides good recommendations.
Even though one could theoretically use service trust _st(i,z)_ for
this, we have another trust metric because there are peers that can provide
very good data (service), but they are surrounded by bad peers or the other
way around. This also gives us the ability to have specialized nodes in the
network that serves as a peers registry for organizations - a single node that
only provides recommendations on peers.
We calculate the recommendation trust in a similar way as the service
trust and reputation, but we use recommendation competence belief _rcb(i,z)_ ,
recommendation integrity belief _rib(i,z)_ and reputation _r(i,z)_ . This time, we
use the weight _rh(i,z)_ , which is the size of the history of the recommendations
provided by z to i, and _rh(max)_ , the maximal size of said history.

![Screenshot_20240404_012957](https://github.com/stratosphereips/fides/assets/41242896/ee07c6f4-6dc2-4ce4-9464-49b4c5c0673a)


**Recommendation Competence and Integrity Belief**

Similarly for interactions, we use three different parameters for calculating
the _rcb(i,z)_ and _rib(i,z)_ . We use satisfaction _rs**x(i,z)_ , weight _rw**x(i,z)_ and the
fading effect _rf**x(i,z)_. The parameters have the same background as described
in the 
[Interaction Satisfaction Section](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#interaction-satisfaction), but in this case, they are connected to recommendations
instead of service. We calculate _rcb(i,z)_ as follows:

![Screenshot_20240404_013050](https://github.com/stratosphereips/fides/assets/41242896/bd43ca56-9c88-43f8-b81b-57a72df7c5eb)



And for recommendation integrity we compute _rib(i,z)_ as:

![Screenshot_20240404_013115](https://github.com/stratosphereips/fides/assets/41242896/ad52e16c-3e7f-4c93-a5e8-1e5759a4ef67)

One more time, the computational model is trying to approximate average
behavior in recommendations - _rcb(i,z)_ - and then the deviation from such
behavior - _rib(i,z)_ 

Fading effect _rf**x(i,z)_ has similar properties as the fading effect for service
trust described in [the Interaction Satisfaction Section](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#interaction-satisfaction).
It is a non-increasing function of a number
of recommendations or a time. For the recommendations, Fides implements
it exactly the same as for the service interactions.


![Screenshot_20240404_013215](https://github.com/stratosphereips/fides/assets/41242896/6caee308-eda9-4b58-9001-a447e7aae614)


**Evaluating Received Recommendation** 

As outlined in [Recommendation Trust Metric Section](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#recommendation-trust-metric), 
in order to evaluate a particular recommendation from remote peer z, 
we have satisfaction, weight, and the fading
effect. We calculate the recommendation satisfaction _rs**x(i,z)_ by comparing
values from z’s recommendation _r(z,j)_ , _cb(z,j)_ , _ib(z,j)_ , with values that are the
results of the recommendation algorithm. In other words, we compare
each recommendation, with the aggregated values - _er(i,j)_  , _ecb(i,j)_ and _eib(i,j)_ .
This gives us an estimate of how off was the peer z’s recommendation from
the final result of the recommendation algorithm.

![Screenshot_20240404_013301](https://github.com/stratosphereips/fides/assets/41242896/f8a2cadb-5678-4cf7-b283-506a342b8b82)


We calculate the weight of recommendation _rw**x(i,z)_ as a weighed sum of
the proportion of the size of the service history between z and j with maximal
service history size. And a number of peers that provided the initial
reputations _η(z,j)_ divided by a maximal number of possible recommending
peers.

![Screenshot_20240404_013339](https://github.com/stratosphereips/fides/assets/41242896/ee01149b-155f-48a8-8a88-67b448ac6841)


## Network Intelligence Aggregation

Fides is a trust model designed for global peer-to-peer networks of Slips
instances. It is designed to support Slips in detecting malicious actors on
the network and enables threat intelligence sharing between peers of Slips
instances. Because Slips was designed to be as modular as possible, Fides is
effectively running as a module that provides aggregated threat intelligence
to Slips. In other words, Fides provides a view of what the network thinks
about some threat intelligence target. This is necessary so Slips can have a
unique view of the network on a specific Threat Intelligence. Fides needs
to aggregate elements of threat intelligence from remote peers into a single
value that is then presented to Slips.


Fides needs to say that some reports are better than others, based on the
service trust the local peer has in the remote peer (previously computed as
_st**k(i,j)_. Thus Fides needs to weigh every report based on this trust and come
up with an aggregated score _S**k(T)_  . Apart from the aggregated score, Fides
needs to compute the aggregated confidence _C**k(T)_ that expresses how confident
i is about the aggregated score _S**k(T)_ that was computed in the previous step.
Once aggregated, the computed score and confidence (_S**k(T)_ , _C**k(T)_ ) are sent
to Slips to report data on target T . Apart from sending to Slips, these
same values can be also used to evaluate the interaction of the remote peers,
depending on the selected interaction evaluation strategy.

We designed and implemented two different functions for aggregating
threat intelligence and computing _S**k(T)_ alongside with _C**k(T)_ . Both of them
are implemented in Fides under their respective names.

### AverageConfidenceTIAggregation
In this method, the aggregated score _S**k(T)_ is the sum of _S**k(j,T)_ which is the
score sent by each peer j about target T in time window k; weighed with
the normalized service trust that i computed for peer j, denoted _wst**k(i,j)_ . The
sum is done over the set of remote peers that provided a report to i for T
in time window k, denoted _R**k(i,T)_. We calculate it in Equation 3.22.
 
![Screenshot_20240404_013616](https://github.com/stratosphereips/fides/assets/41242896/bec214a6-eb68-4add-8b6e-0398a0a8a9b2)


The normalized service trust _wst**k(i,j)_ used as weight is computed as:

![Screenshot_20240404_231557](https://github.com/stratosphereips/fides/assets/41242896/742a3e36-3c1f-46c5-b290-655d444270da)



Equation 3.23 estimates the percentage that the service trust on j _st**k(i,j)_ has
relative to the total sum of service trust received by i for all peers, for this
target T , in time window k.
We compute the aggregated confidence _C**k(T)_ for this strategy as:

![Screenshot_20240404_013722](https://github.com/stratosphereips/fides/assets/41242896/1c5ad2e1-0a33-4988-97dc-893f09a19dea)


Which is an average over all the peers that sent to i a report on T in time
window k, of the weighted confidence sent by peer j on target T on time
window k. The weight is done by the service trust that i has on j on time
window k.

### WeightedAverageConfidenceTIAggregation

This strategy uses Equation 3.22 to compute the aggregated score _S**k(T)_
similarly to the [AverageConfidenceTIAggregation](https://github.com/stratosphereips/fides/blob/design_docs/doc/design.md#averageconfidencetiaggregation).
However, the way how this strategy calculates _C**k(T)_ is different. Instead of using
the service trust _st**k(i,j)_ to determine the correct trust in the confidence _C**k(j,T)_ 
submitted by peer j and then diving it by the number of peers, it uses
the normalized service trust _wst**k(i,j)_ computed in Equation 3.23 that already
contains the weight of the peers in the final decision.
![Screenshot_20240404_013751](https://github.com/stratosphereips/fides/assets/41242896/cb7fc65c-1995-454f-ab6b-314fd68f06c9)






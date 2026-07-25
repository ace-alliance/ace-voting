# How Ace Alliance will vote on the Treasury Withdrawals expiring in epoch 646

A [PDF version][pdf-link] of this statement is also made available (canonical: `ipfs://QmNhSqoiZSzXwV6Tgfe31NsSGC1xifd1so9TN5TtP3GcrK`).

[pdf-link]: https://dweb.link/ipfs/QmNhSqoiZSzXwV6Tgfe31NsSGC1xifd1so9TN5TtP3GcrK

The Net Change Limit currently in force is 350,000,000 ada, set by the DReps through an on-chain governance action (gov_action1m3xx08yv788vfxqh6nfvrjtvmqpwezsy0ggaczctkyjmttc2wmxsq4jsr7q) for the period spanning epochs 613 through 713. The limit operates cumulatively: every treasury withdrawal enacted during the period consumes headroom against the 350,000,000 ada ceiling. After accounting for the 335,610,296 ada in withdrawals already enacted this period, 14,389,704 ada of headroom remains.

That number controls what follows, because Article II.7.3 of the Cardano Constitution requires that a Treasury Withdrawals governance action not exceed the Net Change Limit for the period in which it would be enacted. Ace Alliance must therefore make a constitutional ruling on each pending withdrawal based on the amount of ada it requests relative to the headroom that remains at the point of enactment.

## The five governance actions on the table

Five Treasury Withdrawals governance actions expire at the end of epoch 646. In chronological order of submission:

| # | Governance Action | Submitted (UTC) | Amount Requested |
|---|---|---|---|
| 1 | Alchemy by Sundial x Charms: Cardano-Native Bitcoin Treasury Protocol | 2026-06-24 03:01:28 | 10,000,000 ada |
| 2 | Cardano Builder DAO | 2026-06-24 16:47:14 | 20,000,000 ada |
| 3 | Cardano Enterprise Adoption: Ticketing Platform (Anvil) | 2026-06-24 19:30:39 | 4,969,231 ada |
| 4 | Se7en Labs: Daedalus Wallet Maintenance and Improvements 2026-2027 | 2026-06-24 21:25:59 | 1,785,333 ada |
| 5 | Blockfrost's transformation to not-for-profit | 2026-06-26 13:51:52 | 9,832,979 ada |

The only epoch boundary at which any of these can still be ratified and enacted before they expire is the transition from epoch 645 to epoch 646 on 28 July 2026. The question in front of us is which of these actions can constitutionally be enacted at that boundary.

## Alchemy: unconstitutional on structural grounds

Ace Alliance has already found the Alchemy action unconstitutional under Article II.7.5, because no administrator exists at the moment of withdrawal: Intersect is named only as a proposed interim administrator subject to confirmation and final agreement, and no such agreement exists on or off chain. Our full rationale is published at ipfs://QmTtZn3ctHZSVvZZ5y9o2FS16ic8X7QDgXwEwJdAFeqo86. The action is therefore out of consideration regardless of the Net Change Limit arithmetic, and we do not revisit it here.

## Cardano Builder DAO: over the remaining headroom

The Cardano Builder DAO action requests 20,000,000 ada. With 14,389,704 ada of headroom remaining under the 350,000,000 ada Net Change Limit, enacting this withdrawal would push the cumulative net treasury change for the period past the ceiling, a direct violation of Article II.7.3.

The pending governance action proposing to raise the Net Change Limit to 500,000,000 ada for this same period does not salvage this proposal. The new NCL action itself expires only at the end of epoch 646; it can be considered officially approved only after that action period concludes, and only if it clears the constitutionally defined guardrail threshold (TREASURY-01a) of greater than 50% of the active voting stake of DReps. Even if approved, the new limit would take effect starting in epoch 647, after the Builder DAO action must already have been enacted under the limits in force at its point of enactment.

This is a mandatory constraint, and its breach alone renders the action unconstitutional. Ace Alliance will vote accordingly.

## The remaining three: enough headroom for two, but not all

That leaves three actions: the Anvil ticketing platform (4,969,231 ada), Se7en Labs' Daedalus wallet maintenance (1,785,333 ada), and Blockfrost's transformation to not-for-profit (9,832,979 ada).

The Net Change Limit has enough headroom for the Anvil and Se7en Labs withdrawals: together they total 6,754,564 ada, comfortably within the 14,389,704 ada available. If both pass, however, only 7,635,140 ada of headroom would remain, which is not enough for Blockfrost's 9,832,979 ada request. All three together would exceed the remaining headroom by 2,197,839 ada.

This puts Ace Alliance in a position where we must decide how to rule on which governance actions are viable. One available answer is to say that because the Blockfrost action was submitted last, it is unconstitutional: there is not enough headroom left in the NCL for it if the earlier submissions succeed. But that answer would not be fair to Blockfrost if the Anvil or Se7en Labs withdrawal fails to attract DRep support. If either falls short, headroom for Blockfrost exists, and a pre-emptive constitutional veto would have blocked a perfectly enactable withdrawal. There are no perfect options here.

## How we will vote

When six hours remain in epoch 645, at approximately 15:45 UTC on 28 July 2026, we will assess the DRep support of these three governance actions. We will vote constitutional on the actions that have received the requisite level of delegated stake for enactment (67%), up to the NCL cap, giving preference to order of submission.

In practice, that means: among the actions that have attracted enough DRep support to be ratified, we will vote constitutional in the order they were submitted, until the remaining headroom is exhausted. An action that would carry the cumulative total past the cap at that point will receive a no vote from us, not as a judgment on its merits, but because Article II.7.3 leaves us no other option.

## A call to action for DReps

Because our assessment depends on an accurate reading of DRep support, we call on every DRep to cast a definitive vote of Yes, No, or Abstain on each of these governance actions before we take our reading at approximately 15:45 UTC on 28 July 2026, and not to leave a vote uncast. An uncast vote tells us nothing, and in a situation this tight, silence muddies the picture of where delegated stake actually stands. Whatever your position on a given proposal, put it on chain. Clear signals from the DReps are what make a fair and predictable outcome possible at the epoch boundary.

## Our biases, stated plainly

We do this in an attempt to be as fair as possible, and we want to be clear about our biases. A member of Ace Alliance is part of one of these proposals and has recused himself from the constitutional assessment of it per our team policy. We also consider ourselves personal friends of the submitters of the other two proposals.

We recognize that this is not a perfect solution. First-come-first-served up to a cap is a blunt instrument, and reasonable people can disagree about whether submission order is the right tiebreaker. We adopt it because it is transparent, it is announced in advance, and it does not require us to rank the merits of proposals that the DReps, not the Constitutional Committee, are meant to judge.

Finally, we urge the community to develop streamlined mechanisms for submitting treasury withdrawal actions in ways that do not conflict with one another. The Net Change Limit is doing exactly what it was designed to do. What the ecosystem needs now is better coordination tooling, so that worthy proposals are not forced into a race against each other for the last of the headroom.

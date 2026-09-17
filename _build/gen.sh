#!/bin/bash
cd /home/giobi/brain
S="antique 19th century natural history lithograph plate, hand-colored scientific engraving with fine stippling and cross-hatching, single subject centered and isolated on plain aged cream paper, generous empty margins, muted natural pigments, museum atlas illustration, no text, no letters, no numbers, no caption, no border"
gen(){ [ -s storage/tmp/dragondigest/plates/$1.png ] || python3 .claude/skills/imagen/fal_client_wrapper.py image "$2, $S" -m flux -a 4:3 -o storage/tmp/dragondigest/plates/$1.png >/dev/null 2>>storage/tmp/dragondigest/gen.err; }
while IFS='|' read -r slug subj; do gen "$slug" "$subj" & (( ++i % 4 == 0 )) && wait; done <<'L'
bourdieu-gusto|an Indian peacock with fanned tail, side view
rehearsal-system|a ruminating cow lying down chewing cud, side view
sapolsky-1|an olive baboon sitting, side view
sapolsky-2|anatomical study of a human brain, lateral view
sapolsky-3|a plains zebra standing, side view
decss-illegal-prime|a periodical cicada with wings spread, dorsal view, beside its empty nymph shell
amanda-askell-ai-philosophy|a common octopus with curling arms
sfera-di-riemann|a spherical radiolarian skeleton in the manner of Ernst Haeckel
self-domestication|a silver fox standing, side view
microservices-to-monolith|a Portuguese man o' war siphonophore with trailing tentacles
block-universe|a spiral ammonite fossil, polished cross-section showing chambers
ai-energy-footprint|a ruby-throated hummingbird hovering at a flower
ai-agents-eating-saas|a migratory locust with wings open, on a gnawed wheat stalk
leyline-protocol|a hooded peregrine falcon perched on a leather falconry glove
tim-ferriss-fame|a luna moth with wings spread, dorsal view
existentially-starving|a Nepenthes tropical pitcher plant with hanging pitchers, botanical study
calm-tech-indieweb|a garden snail on a leaf, side view
aiws-syndrome|Amanita muscaria fly agaric mushrooms at three growth stages, botanical study
ai-newton|an apple tree branch with leaves, blossom and one ripe apple, with a halved apple showing seeds, botanical study
dragon|a flying dragon lizard Draco volans with its wing membranes spread, dorsal view
L
wait; ls storage/tmp/dragondigest/plates | wc -l

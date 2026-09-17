#!/bin/bash
cd /home/giobi/brain
S="antique 19th century natural history lithograph plate, hand-colored scientific engraving with fine stippling and cross-hatching, single subject centered and isolated on plain aged cream paper, generous empty margins, muted natural pigments, museum atlas illustration, no text, no letters, no numbers, no caption, no border"
gen(){ [ -s storage/tmp/dragondigest/plates/$1.png ] || python3 .claude/skills/imagen/fal_client_wrapper.py image "$2, $S" -m flux -a 4:3 -o storage/tmp/dragondigest/plates/$1.png >/dev/null 2>>storage/tmp/dragondigest/gen.err; }
while IFS='|' read -r slug subj; do gen "$slug" "$subj" & (( ++i % 4 == 0 )) && wait; done <<'L'
ai-agents-eating-saas-03|a line of leafcutter ants carrying green leaf fragments along a twig
ai-energy-footprint-03|honeybees on a piece of honeycomb with hexagonal cells
ai-newton-03|a hawk moth with a very long proboscis feeding at a white star-shaped Darwin's orchid
aiws-syndrome-02|a chameleon gripping a branch, side view, curled tail
aiws-syndrome-03|a large dragonfly with wings spread, dorsal view, detailed compound eyes
amanda-askell-ai-philosophy-03|an African grey parrot perched on a branch, side view
block-universe-03|a fossil dragonfly imprint in a slab of pale limestone
bourdieu-gusto-02|a satin bowerbird beside its bower of twigs decorated with small blue objects
bourdieu-gusto-03|a small warbler feeding an oversized cuckoo chick sitting in a tiny nest
calm-tech-indieweb-03|fern fronds with an unfurling fiddlehead, botanical study
decss-illegal-prime-03|a sunflower head seen from the front showing the spiral seed pattern, botanical study
existentially-starving-03|a sprouting acorn with roots and a young oak seedling with two leaves, botanical study
leyline-protocol-02|a clownfish sheltering among the tentacles of a sea anemone
leyline-protocol-03|woodland mushrooms connected underground by a fine web of white mycelium threads and tree roots, cross-section of soil
microservices-to-monolith-03|a branch of red coral colony, marine study
rehearsal-system-03|a grass snake coiled in a tight spiral, seen from above
sapolsky-1-03|a mother baboon grooming her infant, side view
sapolsky-2-03|a single Purkinje neuron with densely branching dendrites in the manner of Ramon y Cajal, ink drawing
sapolsky-3-03|a dandelion seed head with a few seeds drifting away, botanical study
self-domestication-03|comparative anatomy study of a wolf skull and a smaller dog skull side by side, lateral view
sfera-di-riemann-03|a nautilus shell cut in half showing the logarithmic spiral chambers
tim-ferriss-fame-03|a hermit crab withdrawing into a whelk shell
L
wait; ls storage/tmp/dragondigest/plates | wc -l

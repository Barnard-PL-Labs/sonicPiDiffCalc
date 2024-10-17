import re
from math import gcd
from functools import reduce

def compare_live_loops(code1, code2):
    def extract_rhythm(code):
        sleep_pattern = re.findall(r'sleep\s+([\d.]+)', code)
        return [float(val) for val in sleep_pattern]

    def lcm(a, b):
        return abs(a * b) // gcd(a, b)

    def find_gcd(numbers):
        return reduce(gcd, numbers)

    rhythm1 = extract_rhythm(code1)
    rhythm2 = extract_rhythm(code2)

    if not rhythm1 or not rhythm2:
        return 0.0

    # Find the greatest common divisor for each rhythm
    gcd1 = find_gcd([int(r * 1000) for r in rhythm1])  # Convert to milliseconds for integer GCD
    gcd2 = find_gcd([int(r * 1000) for r in rhythm2])

    # Find the least common multiple of the two GCDs
    common_pulse = lcm(gcd1, gcd2) / 1000  # Convert back to seconds

    # Calculate how well each rhythm aligns with the common pulse
    def alignment_score(rhythm, pulse):
        score = 0
        for r in rhythm:
            if abs(r % pulse) < 0.001 or abs(pulse - (r % pulse)) < 0.001:  # Allow for small float imprecision
                score += 1
        return score / len(rhythm)

    alignment1 = alignment_score(rhythm1, common_pulse)
    alignment2 = alignment_score(rhythm2, common_pulse)

    # Calculate similarity based on alignments
    similarity = 1 - abs(alignment1 - alignment2)

    return similarity

# Example live_loop code blocks
code1 = """
live_loop :drum do
  sample :drum_heavy_kick
  sleep 1
  play 60
  sleep 0.25
  sample :drum_snare_hard
  sleep 0.5
end
"""

code2 = """
live_loop :melody do
  use_synth :piano
  play scale(:c4, :major).choose, release: 0.2
  sleep 0.5
  play scale(:c4, :major).choose, release: 0.2
  sleep 1
  play scale(:c4, :major).choose, release: 0.2
  sleep 0.5
end
"""

# Run the comparison
if __name__ == "__main__":
    score = compare_live_loops(code1, code2)
    print(f"Rhythmic similarity score: {score:.2f}")

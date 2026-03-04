# analyse.py
# Post-processing script: Top 20 words per star rating (1–5)

from collections import defaultdict


def read_results(filename):
    star_word_counts = defaultdict(dict)

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 2:
                continue

            star_word, count = parts
            count = int(count)

            if "_" not in star_word:
                continue

            star, word = star_word.split("_", 1)

            if star in ["1", "2", "3", "4", "5"]:
                star_word_counts[star][word] = count

    return star_word_counts


def get_top_words_per_star(star_word_counts, top_n=20):
    top_results = {}

    for star, words in star_word_counts.items():
        sorted_words = sorted(words.items(), key=lambda x: x[1], reverse=True)
        top_results[star] = sorted_words[:top_n]

    return top_results


def save_results(top_results, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Top 20 Words Per Star Rating\n")
        f.write("=================================\n\n")

        for star in sorted(top_results.keys()):
            f.write(f"⭐ {star}-Star Reviews\n")
            f.write("------------------------------\n")
            for word, count in top_results[star]:
                f.write(f"{word}\t{count}\n")
            f.write("\n")


if __name__ == "__main__":
    results_file = "results.txt"
    output_file = "top_words_per_star.txt"

    star_word_counts = read_results(results_file)
    top_results = get_top_words_per_star(star_word_counts, 20)
    save_results(top_results, output_file)

    print("Top 20 words per star saved to top_words_per_star.txt")

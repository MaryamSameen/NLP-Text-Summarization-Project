import numpy as np
import pandas as pd
import nltk
from transformers import pipeline
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict

nltk.download('punkt')
nltk.download('stopwords')

# Provided text data
text = """
Late at night, guards on the battlements of Denmark's Elsinore castle are met by Horatio, Prince Hamlet's friend from school. The guards describe a ghost they have seen that resembles Hamlet's father, the recently-deceased king. At that moment, the Ghost reappears, and the guards and Horatio decide to tell Hamlet.

Claudius, Hamlet's uncle, married Hamlet's recently-widowed mother, becoming the new King of Denmark. Hamlet continues to mourn for his father's death and laments his mother's lack of loyalty. When Hamlet hears of the Ghost from Horatio, he wants to see it for himself.

Elsewhere, the royal attendant Polonius says farewell to his son Laertes, who is departing for France. Laertes warns his sister, Ophelia, away from Hamlet and thinking too much of his attentions towards her.The Ghost appears to Hamlet, claiming indeed to be the ghost of his father. He tells Hamlet about how Claudius, the current King and Hamlet's uncle, murdered him, and Hamlet swears vengeance for his father. Hamlet decides to feign madness while he tests the truth of the Ghost's allegations (always a good idea in such situations). According to his plan, Hamlet begins to act strangely. He rejects Ophelia, while Claudius and Polonius, the royal attendant, spy on him. They had hoped to find the reason for Hamlet's sudden change in behaviour but could not. Claudius summons Guildenstern and Rosencrantz, old friends of Hamlet to find out what's got into him. Their arrival coincides with a group of travelling actors that Hamlet happens to know well. Hamlet writes a play which includes scenes that mimic the murder of Hamlet's father. During rehearsal, Hamlet and the actors plot to present Hamlet's play before the King and Queen. At the performance, Hamlet watches Claudius closely to see how he reacts. The play provokes Claudius, and he interrupts the action by storming out. He immediately resolves to send Hamlet away. Hamlet is summoned by his distressed mother, Gertrude, and on the way, he happens upon Claudius kneeling and attempting to pray. Hamlet reasons that to kill the King now would only send his soul to heaven rather than hell. Hamlet decides to spare his life for the time being.  Polonius hides in Gertrude's room to protect her from her unpredicatable son. When Hamlet arrives to scold his mother, he hears Polonius moving behind the arras (a kind of tapestry). He stabs the tapestry and, in so doing, kills Polonius. The ghost of Hamlet's father reappears and warns his son not to delay revenge or upset his mother. Hamlet is sent to England, supposedly as an ambassador, just as King Fortinbras of Norway crosses Denmark with an army to attack Poland. During his journey, Hamlet discovers Claudius has a plan to have him killed once he arrives. He returns to Denmark alone, sending his companions Rosencrantz and Guildenstern to their deaths in his place.

Rejected by Hamlet, Ophelia is now desolate at the loss of her father. She goes mad and drowns. On the way back to Denmark, Hamlet meets Horatio in the graveyard (along with a gravedigger), where they talk of the chances of life and death. Ophelia's funeral procession arrives at the very same graveyard (what luck!). Hamlet confronts Laertes, Ophelia's brother, who has taken his father's place at the court.

A duel is arranged between Hamlet and Laertes. During the match, Claudius conspires with Laertes to kill Hamlet. They plan that Hamlet will die either on a poisoned rapier or with poisoned wine. The plans go awry when Gertrude unwittingly drinks from the poisoned cup and dies. Then both Laertes and Hamlet are wounded by the poisoned blade, and Laertes dies.

Hamlet, in his death throes, kills Claudius. Hamlet dies, leaving only his friend Horatio to explain the truth to the new king, Fortinbras, as he returns in victory from the Polish wars.
"""

# Extractive Summarization
sentences = sent_tokenize(text)

def compute_word_frequencies(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    freq_table = defaultdict(int)
    for word in words:
        if word not in stop_words:
            freq_table[word] += 1
    return freq_table

freq_table = compute_word_frequencies(text)

def score_sentences(sentences, freq_table):
    sentence_scores = defaultdict(int)
    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        for word in words:
            if word in freq_table:
                sentence_scores[sentence] += freq_table[word]
    return sentence_scores

sentence_scores = score_sentences(sentences, freq_table)

def get_summary(sentences, sentence_scores, top_n=3):
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:top_n]
    return ' '.join(top_sentences)

extractive_summary = get_summary(sentences, sentence_scores)
print("Extractive Summary:")
print(extractive_summary)

# Abstractive Summarization
summarizer = pipeline('summarization')
abstract_summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
print("\nAbstractive Summary:")
print(abstract_summary[0]['summary_text'])

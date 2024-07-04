# kb_suggester.py

from kb_mapping import kb_mapping
import nltk
from difflib import SequenceMatcher

class KBSuggester:
    def __init__(self):
        # Download de recursos necessários do NLTK (se ainda não tiver)
        nltk.download('punkt')
        nltk.download('stopwords')

    def suggest_kb(self, description):
        # Pré-processamento da descrição do problema
        tokens_desc = self.preprocess_text(description)

        best_kb = None
        best_score = 0

        for kb_key, kb_info in kb_mapping.items():
            # Pré-processamento do título e das tarefas do KB
            tokens_kb = self.preprocess_text(kb_info['title'])
            for task in kb_info['tasks']:
                tokens_kb += self.preprocess_text(task)

            # Cálculo da similaridade entre a descrição e o KB
            score = self.calculate_similarity(tokens_desc, tokens_kb)

            # Atualizar o melhor KB encontrado
            if score > best_score:
                best_score = score
                best_kb = kb_info

        return best_kb

    def preprocess_text(self, text):
        # Tokenização e remoção de stopwords
        tokens = nltk.word_tokenize(text.lower())
        stopwords = nltk.corpus.stopwords.words('portuguese')
        tokens = [token for token in tokens if token.isalnum() and token not in stopwords]
        return tokens

    def calculate_similarity(self, tokens1, tokens2):
        # Calcular similaridade usando SequenceMatcher do difflib
        matcher = SequenceMatcher(None, tokens1, tokens2)
        return matcher.ratio()

# Exemplo de uso
if __name__ == "__main__":
    suggester = KBSuggester()
    description = "O cliente está enfrentando problemas para fazer login no sistema."
    suggested_kb = suggester.suggest_kb(description)
    if suggested_kb:
        print(suggested_kb)
    else:
        print("Nenhum KB encontrado para a descrição fornecida.")

import sys
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

class Optimizer():
    def __init__(self, job_text):
        self.job_verbs = self.extract_verbs(job_text)
        self.job_synonyms = self.get_synonyms(self.job_verbs)
        self.optimized = {}

    # optimizer function(s)

    def optimize_text(self, resume_text):
        input_verbs = self.extract_verbs(resume_text)

        for i_verb in input_verbs:
            if i_verb in self.job_synonyms:
                if i_verb not in self.optimized:
                    self.optimized[i_verb] = self.job_synonyms[i_verb]

    # helper functions

    def clean_text(self, text):
        ret = ""
        for ch in text:
            if ch.isalnum() or ch.isspace():
                ret += ch

            else:
                ret += ' '

        return ret

    def lemmatize_text(self, body):
        ret = ""
        lem = WordNetLemmatizer()
        for word in body.split():
            w = word.lower()
            ret += lem.lemmatize(w, 'v') + ' '

        return ret

    def extract_verbs(self, body):
        body = self.clean_text(body)
        body = self.lemmatize_text(body)
        pos_all = {}
        verbs = set()

        for word in body.split():
            w = word.lower()
            pos_l = set()

            for tmp in wn.synsets(w):
                if tmp.name().split('.')[0] == w:
                    if tmp.pos() == 'v':
                        verbs.add(w)

            pos_all[w] = pos_l
            
        return verbs

    def get_synonyms(self, verb_set):
        ret = {}
        for word in verb_set:
            for syn in wn.synsets(word):
                for l in syn.lemmas():
                    term = l.name()
                    if term == word:
                        continue

                    if term not in ret:
                        ret[term] = {word}

                    else:
                        ret[term].add(word)

        return ret

    def display_optimized(self):
        if self.optimized == {}:
            return ""

        else:
            ret = ""
            for key in self.optimized:
                line = f"{key}   →   "
                for syn in self.optimized[key]:
                    line += f"{syn}, "
                
                ret += line[:-2] + "\n"

            return ret

class Optimizer_Demo(Optimizer):
    def __init__(self):
        job_path = "src/demo_job.txt"

        with open(job_path, 'r') as job_file:
            job_text = job_file.read()

        super().__init__(job_text)

    def optimize_text(self):
        resume_path = "src/demo_resume.txt"

        with open(resume_path, 'r') as resume_file:
            resume_text = resume_file.read()

        input_verbs = self.extract_verbs(resume_text)
        self.optimized = {}

        for i_verb in input_verbs:
            if i_verb in self.job_synonyms:
                if i_verb not in self.optimized:
                    self.optimized[i_verb] = self.job_synonyms[i_verb]

def main():
    resume_path = "../src/demo_resume.txt"
    job_path = "../src/demo_job.txt"

    with open(resume_path, 'r') as resume_file:
        resume_text = resume_file.read()

    with open(job_path, 'r') as job_file:
        job_text = job_file.read()

    o = Optimizer(job_text)
    print(o.optimize_text(resume_text))

    return 0

if __name__ == "__main__":
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    main()
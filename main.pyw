import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

def clean_text(text):
    ret = ""
    for ch in text:
        if ch.isalnum() or ch.isspace():
            ret += ch

        else:
            ret += ' '

    return ret

def lemmatize_text(body):
    ret = ""
    lem = WordNetLemmatizer()
    for word in body.split():
        w = word.lower()
        ret += lem.lemmatize(w, 'v') + ' '

    return ret

def extract_verbs(body):
    body = clean_text(body)
    body = lemmatize_text(body)
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

def get_synonyms(verb_set):
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

def optimize_text(resume_text, job_text):
    input_verbs = extract_verbs(resume_text)
    job_verbs = extract_verbs(job_text)
    job_synonyms = get_synonyms(job_verbs)
    
    for i_verb in input_verbs:
        if i_verb in job_synonyms:
            print(f"{i_verb}\t-->   {job_synonyms[i_verb]}".expandtabs(12))

def main():
    resume_path = "src/demo_resume.txt"
    job_path = "src/demo_job.txt"

    with open(resume_path, 'r') as resume_file:
        with open(job_path, 'r') as job_file:
            optimize_text(resume_file.read(), job_file.read())

    return 0

if __name__ == "__main__":
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    main()
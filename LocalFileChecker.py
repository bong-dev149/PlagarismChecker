import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# this file is for checking plagiarism in between local files

# class for local file checking
class LocalFileChecker:

    def __init__(self,working_files,file_contents):
        self.results = None
        print("Initialising local file checker...")
        self.working_files = working_files
        self.file_contents = file_contents

    @classmethod
    #     method for vectorizing
    def vectorizing(self, text):
        return TfidfVectorizer().fit_transform(text).toarray()

    # method for calculating similarity
    def get_similarity(self, doc1, doc2):
        # print(doc1.shape,doc2.shape)
        return cosine_similarity([doc1, doc2])

    #     method for operation
    def check_plagiarism(self):
        plagiarism_results = set()
        vectors = self.vectorizing(self.file_contents)
        file_vectors = list(zip(self.working_files, vectors))
        # print(file_vectors)
        for file_a, text_vector_a in file_vectors:
            # print(file_a)
            new_vectors = file_vectors.copy()
            current_index = new_vectors.index((file_a, text_vector_a))
            del new_vectors[current_index]
            for file_b, text_vector_b in new_vectors:
                sim_score = self.get_similarity(text_vector_a, text_vector_b)[0][1]
                file_pair = sorted((file_a, file_b))
                score = (file_pair[0], file_pair[1], sim_score)
                plagiarism_results.add(score)
        self.results = plagiarism_results

#     method for printing the plagiarism checking
    def show_result(self):
        for result in self.results:
            print(result)

if __name__ == '__main__':
    student_files = [doc for doc in os.listdir() if doc.endswith('.txt')]
    student_notes = [open(File).read() for File in student_files]
    lfchk = LocalFileChecker(student_files,student_notes)
    lfchk.check_plagiarism()
    lfchk.show_result()


